from io import BytesIO
import csv
import time
import serial
from serial import Serial
from time import sleep
from itertools import count
from statistics import mean
from GraphManager.GraphManager import PlotterGraficoPDF
from PySide2.QtCore import QObject, Signal, QMutex, Slot
from GlobalFunctions.funcoesGlobais import maximos, minimos
from GlobalFunctions.funcoesGlobais import dataInstantanea, dataDoArquivo


class WorkerEstacao(QObject):
    finalizar = Signal()
    saidaData = Signal(str)
    saidaDadosLCD = Signal(list)
    barraProgresso = Signal(int)
    saidaInfoInicio = Signal(str)
    mostradorTempoRestante = Signal(int)
    saidaDadosEmail = Signal(
        str, float, float, float, float, float, float,
        float, float, float, float, float, float, str,
        BytesIO, BytesIO, BytesIO, BytesIO
    )

    def __init__(
                self, portaArduino: Serial, tempGraf: int, parent=None
            ) -> None:
        super().__init__(parent)
        self.mutex = QMutex()
        self.paradaPrograma: bool = False
        self.tempoConvertido: int = tempGraf
        self.arduino = portaArduino

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

    def registradorDadosArquivo(self, dadosAGravar: dict) -> None:
        with open(dataDoArquivo(), 'a+', newline='', encoding='utf-8') as log:
            try:
                if float(dadosAGravar['u']) and float(dadosAGravar['p']) and \
                     float(dadosAGravar['1']) and float(dadosAGravar['2']) != 0:
                    w = csv.writer(log)
                    w.writerow(
                        [
                            dataInstantanea(), dadosAGravar['u'],
                            dadosAGravar['p'], dadosAGravar['1'],
                            dadosAGravar['2']
                        ]
                    )
            except (ValueError, Exception) as e:
                self.saidaInfoInicio.emit(
                    ' ATENÇÃO: Erro ao registrar dados no arquivo !!!'
                )
                self.saidaInfoInicio.emit(
                    f'ERRO: {e.__class__.__name__} -> {e}'
                )

    @Slot()
    def run(self) -> None:
        yDadosUmidade: list[float] = []
        yDadosPressao: list[float] = []
        yDadosTemperaturaInterna: list[float] = []
        yDadosTemperaturaExterna: list[float] = []
        try:
            cP = count()
            contadorParciais: int = next(cP)

            while not self.paradaPrograma:
                inicioParcial: str = dataInstantanea()
                plotGrafico = PlotterGraficoPDF(inicioParcial)
                cS = count()
                contadorSegundos: int = next(cS)

                if contadorParciais == 0:
                    tempoEmSegundos = self.tempoConvertido
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
                        yDadosTemperaturaInterna.append(
                            float(dadosCarregadosArduino['1'])
                        )
                    if float(dadosCarregadosArduino['2']) > 0:
                        yDadosTemperaturaExterna.append(
                            float(dadosCarregadosArduino['2'])
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
                pdfDadosUmidade = plotGrafico.plotadorPDF(
                    yDadosUmidade, 'umi', 'umi'
                )
                pdfDadosPressao = plotGrafico.plotadorPDF(
                    yDadosPressao, 'press', 'press'
                )
                pdfDadosTemperaturaInterna = plotGrafico.plotadorPDF(
                    yDadosTemperaturaInterna, 'tempInt', 'temp'
                )
                pdfDadosTemperaturaExterna = plotGrafico.plotadorPDF(
                    yDadosTemperaturaExterna, 'tempExt', 'temp'
                    )

                self.saidaDadosEmail.emit(
                                inicioParcial,
                                round(mean(yDadosUmidade), 2),
                                round(mean(yDadosPressao), 2),
                                round(mean(yDadosTemperaturaInterna), 2),
                                round(mean(yDadosTemperaturaExterna), 2),
                                maximos(yDadosTemperaturaInterna),
                                minimos(yDadosTemperaturaInterna),
                                maximos(yDadosTemperaturaExterna),
                                minimos(yDadosTemperaturaExterna),
                                maximos(yDadosUmidade),
                                minimos(yDadosUmidade),
                                maximos(yDadosPressao),
                                minimos(yDadosPressao),
                                dataInstantanea(),
                                pdfDadosUmidade,
                                pdfDadosPressao,
                                pdfDadosTemperaturaInterna,
                                pdfDadosTemperaturaExterna
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
