import csv
import time
import serial
from time import sleep
from serial import Serial
from itertools import count
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from PySide2.QtCore import QObject, Signal, QMutex, Slot
from GlobalFunctions.GlobalFunctions import dataInstantanea, dataDoArquivo
from GlobalFunctions.GlobalFunctions import dataBancoDados
from DataBaseManager.OperationalDataBase import DadoHorario, OperationDataBase
from DataBaseManager.OperationalDataBase import GerenciadorTabelas


class WorkerEstacao(QObject):
    finalizar = Signal()
    saidaData = Signal(str)
    saidaDadosLCD = Signal(list)
    barraProgresso = Signal(int)
    saidaInfoInicio = Signal(str)
    mostradorTempoRestante = Signal(int)
    saidaDadosEmail = Signal(
        str, str, list, list, list, list
    )

    def __init__(
        self, portaArduino: Serial, tempGraf: int, dadosBD: dict, parent=None
    ) -> None:
        super().__init__(parent)
        self.arduino = portaArduino
        self.tempoConvertido: int = tempGraf
        self.dadosBD = dadosBD
        self.paradaPrograma: bool = False
        self.mutex = QMutex()
        self.executor = ThreadPoolExecutor(max_workers=2)
        self.ardutils = ArduinoUtils(self.arduino)
        self.fileUtils = FileUtils(self.saidaInfoInicio)
        self.dbutils = DBUtils(self.dadosBD, self.executor)
        self.interfaceutil = InterfaceUtils(
            self.saidaData, self.saidaDadosLCD,
            self.barraProgresso, self.mostradorTempoRestante,
            self.saidaInfoInicio, self.finalizar
        )

    @Slot()
    def parar(self) -> None:
        self.mutex.lock()
        self.paradaPrograma = True
        self.mutex.unlock()

    @Slot()
    def run(self) -> None:
        try:
            cP = count()
            contadorParciais: int = next(cP)

            while not self.paradaPrograma:
                yDadosUmidade: list[float] = []
                yDadosPressao: list[float] = []
                yDadosTempInt: list[float] = []
                yDadosTempExt: list[float] = []
                inicioParcial: str = dataInstantanea()
                cS = count()
                contadorSegundos: int = next(cS)

                if contadorParciais == 0:
                    tempoEmSegundos = self.tempoConvertido
                    tableName = datetime.now().strftime('%d-%m-%Y')
                    self.executor.submit(
                        self.createDailyTable, tableName, 'tabelas_horarias'
                    )
                    self.saidaInfoInicio.emit(
                        f'Inicio: --> {inicioParcial} <--'
                    )
                else:
                    self.saidaInfoInicio.emit(
                        f'Parcial {contadorParciais} -> {inicioParcial} <-'
                    )

                while (
                    contadorSegundos < tempoEmSegundos
                ) and not self.paradaPrograma:
                    inicioDelimitadorDeTempo: float = time.time()
                    dadosCarregadosArduino: dict = {
                        'dt': '',
                        'u': '',
                        'p': '',
                        '1': '',
                        '2': ''
                    }

                    tratamentoCarga: list = self.carregadorDados()
                    if len(tratamentoCarga) > 4:
                        for _ in range(len(tratamentoCarga) - 4):
                            tratamentoCarga.pop()
                    for dado in tratamentoCarga:
                        dadosCarregadosArduino[dado[0]] = dado[2:]

                    if float(dadosCarregadosArduino['u']) > 0:
                        yDadosUmidade.append(
                            float(dadosCarregadosArduino['u'])
                        )
                    if float(dadosCarregadosArduino['p']) > 0:
                        yDadosPressao.append(
                            float(dadosCarregadosArduino['p'])
                        )
                    if float(dadosCarregadosArduino['1']) > 0:
                        yDadosTempInt.append(
                            float(dadosCarregadosArduino['1'])
                        )
                    if float(dadosCarregadosArduino['2']) > 0:
                        yDadosTempExt.append(
                            float(dadosCarregadosArduino['2'])
                        )

                    dadosCarregadosArduino['dt'] = dataInstantanea()
                    tableName = datetime.now().strftime('%d-%m-%Y')
                    now = datetime.now()

                    if now.hour == 0 and now.minute == 0 and now.second == 0:
                        self.createDailyTable(tableName, 'tabelas_horarias')

                    self.executor.submit(
                        self.insertDataOnBD,
                        tableName=tableName,
                        data=dadosCarregadosArduino
                    )

                    self.registradorDadosArquivo(dadosCarregadosArduino)

                    self.enviarDadosTempoRealParaLCD(dadosCarregadosArduino)

                    contadorSegundos = next(cS)
                    self.atualizarBarraProgresso(
                        tempoEmSegundos, contadorSegundos
                    )
                    self.atualizarTempoRestante(
                        tempoEmSegundos, contadorSegundos
                    )

                    terminoDelimitadorDeTempo: float = time.time()
                    while (
                        terminoDelimitadorDeTempo - inicioDelimitadorDeTempo
                    ) < 1.0:
                        terminoDelimitadorDeTempo = time.time()

                contadorParciais = next(cP)
                terminoParcial: str = dataInstantanea()
                self.saidaDadosEmail.emit(
                    inicioParcial, terminoParcial, yDadosUmidade,
                    yDadosPressao, yDadosTempInt, yDadosTempExt
                )

            self.saidaInfoInicio.emit('Programa Parado !!!')
            self.barraProgresso.emit(0)
            self.finalizar.emit()
        except (ValueError, Exception) as e:
            self.saidaInfoInicio.emit(f'{e.__class__.__name__}: {e}')
            self.saidaInfoInicio.emit('Programa Parado !!!')
            self.barraProgresso.emit(0)
            self.finalizar.emit()


class ConexaoUSB():
    def __init__(self, caminhoPorta: str) -> None:
        self.caminho: str = caminhoPorta
        self.conexaoArduino: Serial = Serial(
            self.caminho, 9600, timeout=1, bytesize=serial.EIGHTBITS
        )

    def conectPortaUSB(self) -> Serial:
        try:
            self.conexaoArduino.reset_input_buffer()
            return self.conexaoArduino
        except Exception as e:
            raise e

    def desconectarPortaUSB(self) -> None:
        self.conexaoArduino.close()
