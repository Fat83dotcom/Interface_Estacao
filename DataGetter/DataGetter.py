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
                tempoEmSegundos: int = self.tempoConvertido
                yDadosUmidade: list[float] = []
                yDadosPressao: list[float] = []
                yDadosTempInt: list[float] = []
                yDadosTempExt: list[float] = []
                inicioParcial: str = dataInstantanea()
                cS = count()
                contadorSegundos: int = next(cS)

                if contadorParciais == 0:
                    self.dbutils.inicializadorTabelasHorarias()
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

                    tratamentoCarga: list = self.ardutils.carregadorDados()
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
                    self.fileUtils.registradorDadosArquivo(
                        dadosCarregadosArduino
                    )

                    self.dbutils.verificaHorarioCriacaoTabelaHoraria()

                    dadosCarregadosArduino['dt'] = dataBancoDados()
                    self.dbutils.insereBancoDados(dadosCarregadosArduino)

                    self.interfaceutil.enviarDadosTempoRealParaLCD(
                        dadosCarregadosArduino
                    )

                    contadorSegundos = next(cS)
                    self.interfaceutil.atualizarBarraProgresso(
                        tempoEmSegundos, contadorSegundos
                    )
                    self.interfaceutil.atualizarTempoRestante(
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

            self.interfaceutil.atualizarFinalizacao()
        except (ValueError, Exception) as e:
            self.saidaInfoInicio.emit(f'{e.__class__.__name__}: {e}')
            self.interfaceutil.atualizarFinalizacao()


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


class InterfaceUtils:
    def __init__(
        self, saidaData: Signal, saidaDadosLCD: Signal,
        barraProgresso: Signal, mostradorTempoRestante: Signal,
        saidaInfoInicio: Signal, finalizar: Signal
    ) -> None:
        self.saidaData = saidaData
        self.saidaDadosLCD = saidaDadosLCD
        self.barraProgresso = barraProgresso
        self.mostradorTempoRestante = mostradorTempoRestante
        self.saidaInfoInicio = saidaInfoInicio
        self.finalizar = finalizar

    def porcentagem(self, totalVoltas: int, voltaAtual: int) -> int:
        porcentagem: float = voltaAtual * 100 / totalVoltas
        return int(porcentagem)

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

    def atualizarFinalizacao(self) -> None:
        self.saidaInfoInicio.emit('Programa Parado !!!')
        self.barraProgresso.emit(0)
        self.finalizar.emit()


class FileUtils:
    def __init__(self, saidaInfoInicio: Signal, ) -> None:
        self.saidaInfoInicio = saidaInfoInicio

    def registradorDadosArquivo(self, dados: dict) -> None:
        with open(dataDoArquivo(), 'a+', newline='', encoding='utf-8') as log:
            try:
                if float(dados['u']) and float(dados['p']) and \
                     float(dados['1']) and float(dados['2']) != 0:
                    w = csv.writer(log)
                    w.writerow(
                        [
                            dados['dt'], dados['u'],
                            dados['p'], dados['1'],
                            dados['2']
                        ]
                    )
            except (ValueError, Exception) as e:
                self.saidaInfoInicio.emit(
                    f''' ATENÇÃO: Erro ao registrar dados no arquivo !!!
                         ERRO: {e.__class__.__name__} -> {e}'''
                )


class DBUtils:
    def __init__(self, dadosBD: dict, executor: ThreadPoolExecutor) -> None:
        self.dadosBD = dadosBD
        self.executor = executor
        self.dB = OperationDataBase(self.dadosBD)
        self.dDH = DadoHorario(self.dB)
        self.dGT = GerenciadorTabelas(self.dB)

    def inicializadorTabelasHorarias(self) -> None:
        try:
            tableName = self.dGT.nameTableGenerator()
            self.dGT.execInsertTable(
                (tableName,),
                table='gerenciador_tabelas_horarias',
                collumn=('data_tabela', )
            )
            fKey: int = self.dGT.getForeignKey()
            self.executor.submit(
                self.dDH.execCreateTable,
                fKey, tableName=tableName, schema='tabelas_horarias'
            )
        except Exception:
            ...

    def verificaHorarioCriacaoTabelaHoraria(self) -> None:
        now = datetime.now()
        if now.hour == 0 and now.minute == 0 and now.second == 0:
            self.inicializadorTabelasHorarias()

    def insereBancoDados(self, dadosCarregadosArduino: dict) -> None:
        tableName = self.dGT.nameTableGenerator()
        self.executor.submit(
            self.dDH.execInsertTable,
            dadosCarregadosArduino,
            table=tableName,
            collumn=(
                'data_hora', 'umidade', 'pressao', 'temp_int', 'temp_ext'
            ),
            schema='tabelas_horarias'
        )


class ArduinoUtils:
    def __init__(self, portaArduino: Serial,) -> None:
        self.arduino = portaArduino

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
