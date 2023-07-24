import csv
import time
import serial
from time import sleep
from serial import Serial
from itertools import count
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from PySide2.QtCore import QObject, Signal, QMutex, Slot
from DataBaseManager.databaseSettings import dbCredentials
from GlobalFunctions.funcoesGlobais import dataInstantanea, dataDoArquivo
from DataBaseManager.OperationalDataBase import DadoHorario, OperationDataBase


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
                self, portaArduino: Serial, tempGraf: int, parent=None
            ) -> None:
        super().__init__(parent)
        self.mutex = QMutex()
        self.paradaPrograma: bool = False
        self.tempoConvertido: int = tempGraf
        self.arduino = portaArduino
        self.dB = OperationDataBase(dbCredentials(3))
        self.dDH = DadoHorario(self.dB)
        self.executor = ThreadPoolExecutor(max_workers=10)

    def porcentagem(self, totalVoltas: int, voltaAtual: int) -> int:
        porcentagem: float = voltaAtual * 100 / totalVoltas
        return int(porcentagem)

    @Slot()
    def parar(self) -> None:
        self.mutex.lock()
        self.paradaPrograma = True
        self.mutex.unlock()

    def carregadorDados(self) -> list:
        cargaDadosArduino: list = []
        self.arduino.reset_input_buffer()
        while len(cargaDadosArduino) < 4:
            self.arduino.write('u'.encode('utf-8'))
            sleep(0.1)
            if self.arduino.in_waiting:
                dado = self.arduino.readline().decode('utf-8')
                cargaDadosArduino.append(dado.strip())
            self.arduino.write('p'.encode('utf-8'))
            sleep(0.1)
            if self.arduino.in_waiting:
                dado = self.arduino.readline().decode('utf-8')
                cargaDadosArduino.append(dado.strip())
            self.arduino.write('1'.encode('utf-8'))
            sleep(0.1)
            if self.arduino.in_waiting:
                dado = self.arduino.readline().decode('utf-8')
                cargaDadosArduino.append(dado.strip())
            self.arduino.write('2'.encode('utf-8'))
            sleep(0.1)
            if self.arduino.in_waiting:
                dado = self.arduino.readline().decode('utf-8')
                cargaDadosArduino.append(dado.strip())
        return cargaDadosArduino

    def enviarDadosTempoRealParaLCD(self, dados: dict) -> None:
        dadosMostradorLcd: list = []
        dadosMostradorLcd.append(dados["u"])
        dadosMostradorLcd.append(dados["p"])
        dadosMostradorLcd.append(dados["1"])
        dadosMostradorLcd.append(dados["2"])
        self.saidaData.emit(dataInstantanea())
        self.saidaDadosLCD.emit(dadosMostradorLcd)

    def atualizarBarraProgresso(self, tempoTotal, tempoCorrente) -> None:
        percentTempoCorrido: int = self.porcentagem(tempoTotal, tempoCorrente)
        self.barraProgresso.emit(percentTempoCorrido)

    def atualizarTempoRestante(self, tempoTotal, tempoCorrente) -> None:
        self.mostradorTempoRestante.emit((tempoTotal - tempoCorrente))

    def registradorDadosArquivo(self, dados: dict) -> None:
        with open(dataDoArquivo(), 'a+', newline='', encoding='utf-8') as log:
            try:
                if float(dados['u']) and float(dados['p']) and \
                     float(dados['1']) and float(dados['2']) != 0:
                    w = csv.writer(log)
                    w.writerow(
                        [
                            dataInstantanea(), dados['u'],
                            dados['p'], dados['1'],
                            dados['2']
                        ]
                    )
            except (ValueError, Exception) as e:
                self.saidaInfoInicio.emit(
                    ' ATENÇÃO: Erro ao registrar dados no arquivo !!!'
                )
                self.saidaInfoInicio.emit(
                    f'ERRO: {e.__class__.__name__} -> {e}'
                )

    def createDailyTable(self, tableName: str, schema: str) -> None:
        try:
            self.dDH.execCreateTable(
                tableName=tableName, schema=schema
            )
        except Exception as e:
            raise e.__class__.__name__

    def insertDataOnBD(self, tableName: str, data: dict) -> None:
        try:
            self.dDH.execInsertTable(
                data,
                table=tableName,
                collumn=(
                    'data_hora', 'umidade', 'pressao', 'temp_int', 'temp_ext'
                ),
                schema='tabelas_horarias'
            )
        except Exception as e:
            raise e.__class__.__name__

    @Slot()
    def run(self) -> None:
        yDadosUmidade: list[float] = []
        yDadosPressao: list[float] = []
        yDadosTempInt: list[float] = []
        yDadosTempExt: list[float] = []
        try:
            cP = count()
            contadorParciais: int = next(cP)

            while not self.paradaPrograma:
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
                        self.executor.submit(
                            self.createDailyTable,
                            tableName,
                            'tabelas_horarias'
                        )

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
                    ) < 1:
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
