import sys
import serial
import os
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import QThread, QObject, pyqtSignal, QMutex, pyqtSlot
from interface import Ui_MainWindow
from serial import Serial
import time
import csv
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from manipuladoresArquivos import meu_email, minha_senha, my_recipients
from statistics import mean
from string import Template
from itertools import count
from time import sleep


def dataInstantanea() -> str:
    try:
        data = time.strftime('%d %b %Y %H:%M:%S', time.localtime())
        return data
    except (ValueError, Exception) as e:
        raise e


def dataDoArquivo() -> str:
    try:
        dataA = time.strftime('%b_%Y_log.csv').lower()
        return dataA
    except (ValueError, Exception) as e:
        raise e


def maximos(dados) -> float:
    try:
        return round(max(dados), 2)
    except (ValueError, Exception) as e:
        raise DadosError(f'{e.__class__.__name__} -> função: {maximos.__name__}: Não há dados a serem processados.')


def minimos(dados) -> float:
    try:
        return round(min(dados), 2)
    except (ValueError, Exception) as e:
        raise DadosError(f'{e.__class__.__name__} -> função: {minimos.__name__}: Não há dados a serem processados.')


class PlotterGraficoPDF:
    def __init__(self, dataInicio: str, caminhoDiretorioPrograma: str) -> None:
        self.dtInicio = dataInicio
        self.caminhoDiretorioPrograma = caminhoDiretorioPrograma
        self.tipoGrafico = {
            'umi': 'Umidade',
            'press': 'Pressao',
            'tempInt': 'Temperatura_Interna',
            'tempExt': 'Temperatura_Externa',
        }
        self.grandeza = {
            'temp': 'Temperatura em °C',
            'press': 'Pressão Atmosférica em hPa',
            'umi': 'Umidade Relativa do Ar %',
        }

    def geradorCaminhoArquivoPDF(self, tipoGrafico: str) -> str:
        """
            Argumentos que devem ser passados para cada situação:
            Tipos de Gráfico -> 'umi', 'press', 'tempInt', 'tempExt'
        """
        arquivoPDF = f'{self.caminhoDiretorioPrograma}/{self.tipoGrafico[tipoGrafico]}{self.dtInicio}.pdf'
        return arquivoPDF

    def plotadorPDF(self, dadosEixo_Y: list, tipoGrafico: str, grandezaEixo_Y: str) -> None:
        """
            Argumentos que devem ser passados para cada situação:
            tipoGrafico -> 'umi', 'press', 'tempInt', 'tempExt'
            Grandezas -> 'temp', 'press', 'umi'
        """
        try:
            tempoEixo_X = range(len(dadosEixo_Y))
            arquivoPDF = self.geradorCaminhoArquivoPDF(tipoGrafico)
            plt.title(f'{self.tipoGrafico[tipoGrafico]}\n-> Inicio: {self.dtInicio} <-|-> Termino: {dataInstantanea()} '
                      f' <-\nMáxima: {maximos(dadosEixo_Y)} --- Mínima: {minimos(dadosEixo_Y)}')
            plt.xlabel('Tempo em segundos.')
            plt.ylabel(self.grandeza[grandezaEixo_Y])
            plt.plot(tempoEixo_X, dadosEixo_Y)
            plt.savefig(arquivoPDF)
            plt.clf()
        except (ValueError, Exception) as e:
            raise e

    def apagadorArquivosPDF(self, tipoGrafico: str) -> None:
        """
            Argumentos que devem ser passados para cada situação:
            Tipos de Gráfico -> 'umi', 'press', 'tempInt', 'tempExt'
        """
        try:
            os.remove(self.geradorCaminhoArquivoPDF(tipoGrafico))
        except Exception as e:
            raise e


class TransSegundos:
    def __init__(self, horas) -> None:
        self.horas = horas

    def conversorHorasSegundo(self) -> int:
        horas = self.horas[:2]
        minutos = self.horas[3:]
        segundos = int(int(horas) * 3600 + int(minutos) * 60)
        return segundos


class WorkerEmailTesteConexao(QObject):
    termino = pyqtSignal()
    msgEnvio = pyqtSignal(str)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

    def run(self):
        try:
            usuario = ''.join(meu_email())
            msg = MIMEMultipart()
            msg['from'] = usuario
            msg['to'] = usuario
            msg['subject'] = f'Teste de Conexão {dataInstantanea()}'
            with open('emailTeste.html', 'r') as page:
                email = page.read()
                template = Template(email)
                htmlEmail = template.safe_substitute(usuario=usuario)
            corpo = MIMEText(htmlEmail, 'html')
            msg.attach(corpo)
            try:
                with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
                    smtp.ehlo()
                    smtp.starttls()
                    smtp.login(''.join(meu_email()), ''.join(minha_senha()))
                    smtp.send_message(msg)
                    self.msgEnvio.emit('Email enviado com sucesso.')
            except Exception as e:
                self.msgEnvio.emit(f'Não foi possivel enviar o email. Motivo: {e.__class__.__name__}: {e}')
                self.termino.emit()
        except Exception as e:
            self.msgEnvio.emit(f'Não foi possivel enviar o email. Motivo: {e.__class__.__name__}: {e}')
            self.termino.emit()
        self.termino.emit()


class WorkerEmail(QObject):
    termino = pyqtSignal()
    msgEnvio = pyqtSignal(str)

    def __init__(self, inicio, umi, press, t1, t2, t1max,
                 t1min, t2max, t2min, umimax, umimini,
                 pressmax, pressmini, fim, path, parent=None):
        super().__init__(parent)
        self.inicio = inicio
        self.path = path
        self.umi = umi
        self.press = press
        self.t1 = t1
        self.t2 = t2
        self.t1max = t1max
        self.t1min = t1min
        self.t2max = t2max
        self.t2min = t2min
        self.umimax = umimax
        self.umimini = umimini
        self.pressmax = pressmax
        self.pressmini = pressmini
        self.fim = fim
        self.servicosArquivosPDF = PlotterGraficoPDF(self.inicio, self.path)

    def anexadorPdf(self, enderecoPdf, msg):
        with open(enderecoPdf, 'rb') as pdf:
            anexo = MIMEApplication(pdf.read(), _subtype='pdf')
            anexo.add_header('Conteudo', enderecoPdf)
            msg.attach(anexo)

    def renderizadorHtml(self, umidade, pressao, temp1, temp2, temp1max, temp1min,
                         temp2max, temp2min, umima, umimi, pressma, pressmi,
                         inicio, fim, data):
        with open('template.html', 'r') as doc:
            template = Template(doc.read())
            corpo_msg = template.safe_substitute(umi=umidade, press=pressao, t1=temp1, t2=temp2,
                                                 t1max=temp1max, t1min=temp1min, t2max=temp2max,
                                                 t2min=temp2min, umimax=umima, umimini=umimi,
                                                 pressmax=pressma, pressmini=pressmi, ini=inicio,
                                                 fim=fim, dat=data)
        return corpo_msg

    @pyqtSlot()
    def run(self):
        try:
            msg = MIMEMultipart()
            msg['from'] = ''.join(meu_email())
            msg['to'] = ','.join(my_recipients())
            msg['subject'] = f'Monitoramento Estação Metereologica Fat83dotcom {dataInstantanea()}'
            corpo = MIMEText(self.renderizadorHtml(self.umi, self.press, self.t1, self.t2,
                             self.t1max, self.t1min, self.t2max, self.t2min,
                             self.umimax, self.umimini, self.pressmax, self.pressmini,
                             self.inicio, self.fim, dataInstantanea()), 'html')
            msg.attach(corpo)

            umidade = self.servicosArquivosPDF.geradorCaminhoArquivoPDF('umi')
            pressao = self.servicosArquivosPDF.geradorCaminhoArquivoPDF('press')
            tmp1 = self.servicosArquivosPDF.geradorCaminhoArquivoPDF('tempInt')
            temp2 = self.servicosArquivosPDF.geradorCaminhoArquivoPDF('tempExt')

            self.anexadorPdf(umidade, msg)
            self.anexadorPdf(pressao, msg)
            self.anexadorPdf(tmp1, msg)
            self.anexadorPdf(temp2, msg)

            with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.login(''.join(meu_email()), ''.join(minha_senha()))
                smtp.send_message(msg)
                self.msgEnvio.emit('Email enviado com sucesso.')
        except Exception as e:
            self.msgEnvio.emit('Não foi possivel enviar o email.')
            self.msgEnvio.emit(f'Motivo: {e.__class__.__name__}: {e}')
        finally:
            self.servicosArquivosPDF.apagadorArquivosPDF('umi')
            self.servicosArquivosPDF.apagadorArquivosPDF('press')
            self.servicosArquivosPDF.apagadorArquivosPDF('tempInt')
            self.servicosArquivosPDF.apagadorArquivosPDF('tempExt')
        self.termino.emit()


class WorkerEstacao(QObject):
    finalizar = pyqtSignal()
    barraProgresso = pyqtSignal(int)
    saidaInfoInicio = pyqtSignal(str)
    saidaDadosLCD = pyqtSignal(list)
    saidaData = pyqtSignal(str)
    saidaDadosEmail = pyqtSignal(str, float, float, float, float, float, float,
                                 float, float, float, float, float, float, str, str)
    mostradorTempoRestante = pyqtSignal(int)

    def __init__(self, portaArduino: Serial, tempoGrafico: int, parent=None) -> None:
        super().__init__(parent)
        self.mutex = QMutex()
        self.porta: Serial = portaArduino
        self.paradaPrograma: bool = False
        self.tempoConvertido: int = tempoGrafico
        self.arduino = portaArduino

    def porcentagem(self, totalVoltas: int, voltaAtual: int) -> int:
        porcentagem: float = voltaAtual * 100 / totalVoltas
        return int(porcentagem)

    @pyqtSlot()
    def parar(self):
        self.mutex.lock()
        self.paradaPrograma: bool = True
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
        percentualTempoCorrido: int = self.porcentagem(tempoTotal, tempoCorrente)
        self.barraProgresso.emit(percentualTempoCorrido)

    def atualizarTempoRestante(self, tempoTotal, tempoCorrente) -> None:
        self.mostradorTempoRestante.emit((tempoTotal - tempoCorrente))

    def registradorDadosArquivo(self, dadosAGravar: dict) -> None:
        with open(dataDoArquivo(), 'a+', newline='', encoding='utf-8') as log:
            try:
                w = csv.writer(log)
                w.writerow([dataInstantanea(), dadosAGravar['u'], dadosAGravar['p'],
                            dadosAGravar['1'], dadosAGravar['2']])
            except (ValueError, Exception) as e:
                self.saidaInfoInicio.emit(' ATENÇÃO: Erro ao registrar dados no arquivo !!!')
                self.saidaInfoInicio.emit(f'ERRO: {e.__class__.__name__} -> {e}')

    @pyqtSlot()
    def run(self):
        try:
            caminhoDiretorio: str = os.path.dirname(os.path.realpath(__file__))
            cP = count()
            contadorParciais: int = next(cP)

            while not self.paradaPrograma:
                if contadorParciais == 0:
                    tempoEmSegundos = self.tempoConvertido
                    self.saidaInfoInicio.emit(f'Inicio: --> {dataInstantanea()} <--')
                else:
                    self.saidaInfoInicio.emit(f'Parcial {contadorParciais} --> {dataInstantanea()} <--')

                inicioParcial: str = dataInstantanea()

                plotGrafico = PlotterGraficoPDF(inicioParcial, caminhoDiretorio)

                yDadosUmidade: list = []
                yDadosPressao: list = []
                yDadosTemperaturaInterna: list = []
                yDadosTemperaturaExterna: list = []

                cS = count()
                contadorSegundos: int = next(cS)

                while (contadorSegundos < tempoEmSegundos) and not self.paradaPrograma:
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

                    yDadosUmidade.append(float(dadosCarregadosArduino['u']))
                    yDadosPressao.append(float(dadosCarregadosArduino['p']))
                    yDadosTemperaturaInterna.append(float(dadosCarregadosArduino['1']))
                    yDadosTemperaturaExterna.append(float(dadosCarregadosArduino['2']))

                    self.registradorDadosArquivo(dadosCarregadosArduino)

                    self.enviarDadosTempoRealParaLCD(dadosCarregadosArduino)

                    contadorSegundos = next(cS)
                    self.atualizarBarraProgresso(tempoEmSegundos, contadorSegundos)
                    self.atualizarTempoRestante(tempoEmSegundos, contadorSegundos)

                    terminoDelimitadorDeTempo: float = time.time()
                    while (terminoDelimitadorDeTempo - inicioDelimitadorDeTempo) < 1:
                        terminoDelimitadorDeTempo = time.time()

                contadorParciais = next(cP)
                plotGrafico.plotadorPDF(yDadosUmidade, 'umi', 'umi')
                plotGrafico.plotadorPDF(yDadosPressao, 'press', 'press')
                plotGrafico.plotadorPDF(yDadosTemperaturaInterna, 'tempInt', 'temp')
                plotGrafico.plotadorPDF(yDadosTemperaturaExterna, 'tempExt', 'temp')

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
                                caminhoDiretorio)

            self.saidaInfoInicio.emit('Programa Parado !!!')
            self.barraProgresso.emit(0)
            self.finalizar.emit()
        except (ValueError, Exception) as e:
            self.saidaInfoInicio.emit(f'{e.__class__.__name__}: {e}')
            self.saidaInfoInicio.emit('Programa Parado !!!')
            self.barraProgresso.emit(0)
            self.finalizar.emit()


class EntradaError(Exception):
    ...


class DadosError(Exception):
    ...


class ConexaoUSB():
    def __init__(self, caminhoPorta: str) -> None:
        self.caminho: str = caminhoPorta
        self.conexaoArduino: Serial = Serial(self.caminho, 9600, timeout=2, bytesize=serial.EIGHTBITS)

    def conectPortaUSB(self) -> Serial:
        try:
            self.conexaoArduino.reset_input_buffer()
            return self.conexaoArduino
        except Exception as e:
            raise e

    def desconectarPortaUSB(self):
        self.conexaoArduino.close()


class InterfaceEstacao(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        super().setupUi(self)
        self.btnInciarEstacao.clicked.connect(self.executarMainEstacao)
        self.btnPararEstacao.clicked.connect(self.pararWorker)
        self.btnSalvarUsuarioSenha.clicked.connect(self.adicionarEmailRemetenteSenha)
        self.btnAdicionarDestinatario.clicked.connect(self.adicionarEmailDestinatarios)
        self.btnExcluirDestinatario.clicked.connect(self.deletarEmailDestinatario)
        self.btnTesteConexao.clicked.connect(self.executarEmailTeste)
        self.btnPararEstacao.setEnabled(False)
        self.modeloInfo = QStandardItemModel()
        self.saidaDetalhes.setModel(self.modeloInfo)
        self.manipuladorRemetenteSenha()
        self.manipuladorDestinatarios()

    def mostrardorDisplayBarraProgresso(self, percent):
        self.barraProgresso.setValue(percent)

    def mostradorDisplayInfo(self, info):
        self.modeloInfo.appendRow(QStandardItem(info))

    def mostradorDisplayLCDTempoRestante(self, valor):
        self.visorTempoRestante.display(valor)
        self.visorTempoRestante_2.display(valor)

    def mostradorDisplayLCDTempoDefinido(self, valor):
        self.tempoDefinido.display(valor)
        self.tempoDefinido_2.display(valor)

    def mostradorDisplayLCDDados(self, dados: list):
        self.dadoUmidade.display(dados[0])
        self.dadoPressao.display(dados[1])
        self.dadoTempInterna.display(dados[2])
        self.dadoTempExterna.display(dados[3])

    def mostradorLabelDataHora(self, dt_hr):
        self.dadosHoraData.setText(dt_hr)

    def retornarBotoesInicio(self):
        self.btnInciarEstacao.setEnabled(True)
        self.btnPararEstacao.setEnabled(False)

    def executarMainEstacao(self):
        self.btnInciarEstacao.setEnabled(False)
        self.btnPararEstacao.setEnabled(True)
        self.porta = self.portaArduino.text()
        if self.porta == '':
            self.mostradorDisplayInfo('Entre com uma porta válida.')
            self.retornarBotoesInicio()
            return
        try:
            self.receptorTempoGraficos = self.tempoGraficos.text()
            t = TransSegundos(self.receptorTempoGraficos)
            self.receptorTempoGraficos = t.conversorHorasSegundo()
            self.mostradorDisplayLCDTempoDefinido(self.receptorTempoGraficos)
            if self.receptorTempoGraficos <= 0:
                self.retornarBotoesInicio()
                raise EntradaError('Tempo não pode ser menor ou igual a Zero.')
        except Exception as e:
            self.mostradorDisplayInfo(f'{e.__class__.__name__}: {e}')
            return
        try:
            portaArduino: ConexaoUSB = ConexaoUSB(self.porta)
            pA: Serial = portaArduino.conectPortaUSB()
            self.estacaoThread = QThread(parent=self)
            self.estacaoWorker = WorkerEstacao(portaArduino=pA, tempoGrafico=self.receptorTempoGraficos)
            self.estacaoWorker.moveToThread(self.estacaoThread)
            self.estacaoWorker.finalizar.connect(self.estacaoThread.quit)
            self.estacaoWorker.finalizar.connect(self.estacaoWorker.deleteLater)
            self.estacaoWorker.finalizar.connect(self.estacaoThread.deleteLater)
            self.estacaoWorker.finalizar.connect(portaArduino.desconectarPortaUSB)
            self.estacaoThread.started.connect(self.estacaoWorker.run)
            self.estacaoThread.start()
            self.estacaoWorker.barraProgresso.connect(self.mostrardorDisplayBarraProgresso)
            self.estacaoWorker.saidaInfoInicio.connect(self.mostradorDisplayInfo)
            self.estacaoWorker.saidaDadosLCD.connect(self.mostradorDisplayLCDDados)
            self.estacaoWorker.saidaData.connect(self.mostradorLabelDataHora)
            self.estacaoWorker.saidaDadosEmail.connect(self.executarEmail)
            self.estacaoWorker.mostradorTempoRestante.connect(self.mostradorDisplayLCDTempoRestante)
            self.estacaoThread.finished.connect(lambda: self.btnInciarEstacao.setEnabled(True))
            self.portaArduino.setEnabled(False)
            self.tempoGraficos.setEnabled(False)
        except Exception as e:
            self.mostradorDisplayInfo(f'{e.__class__.__name__}: {e}')
            self.retornarBotoesInicio()
            return

    def pararWorker(self):
        self.estacaoWorker.parar()
        self.estacaoThread.quit()
        self.estacaoThread.wait()
        self.btnPararEstacao.setEnabled(False)
        self.portaArduino.setEnabled(True)
        self.tempoGraficos.setEnabled(True)

    def executarEmail(self, inicio, umi, press, t1, t2, t1max,
                      t1min, t2max, t2min, umimax, umimini,
                      pressmax, pressmini, fim, path):
        try:
            self.emailThread = QThread(parent=None)
            self.emailWorker = WorkerEmail(inicio=inicio, umi=umi, press=press, t1=t1,
                                           t2=t2, t1max=t1max, t1min=t1min, t2max=t2max,
                                           t2min=t2min, umimax=umimax, umimini=umimini,
                                           pressmax=pressmax, pressmini=pressmini,
                                           fim=fim, path=path)
            self.emailWorker.moveToThread(self.emailThread)
            self.emailThread.started.connect(self.emailWorker.run)
            self.emailThread.start()
            self.emailWorker.msgEnvio.connect(self.mostradorDisplayInfo)
            self.emailWorker.termino.connect(self.emailThread.quit)
            self.emailWorker.termino.connect(self.emailThread.wait)
            self.emailWorker.termino.connect(self.emailThread.deleteLater)
            self.emailWorker.termino.connect(self.emailWorker.deleteLater)
        except Exception as e:
            self.mostradorDisplayInfo(f'{e.__class__.__name__}: {e}')
            return

    def defineArquivoEmail(self, dadoUsuario: str):
        with open('.EMAIL_USER_DATA.txt', 'w') as file:
            file.write(dadoUsuario)

    def defineArquivoSenha(self, dadoUsuario: str):
        with open('.PASSWORD_USER_DATA.txt', 'w') as file:
            file.write(dadoUsuario)

    def defineArquivoDestinatarios(self, dadoUsuario: str):
        with open('.RECIPIENTS_USER_DATA.txt', 'a') as file:
            file.write(f'{dadoUsuario}\n')

    def apagadorArquivo(self, caminhoArquivo: str):
        with open(caminhoArquivo, 'w') as file:
            file.write('')

    def manipuladorRemetenteSenha(self):
        try:
            if len(meu_email()) == 1 and len(minha_senha()) == 1:
                email = ''.join(meu_email())
                senha = ''.join(minha_senha())
                self.statusRemetenteSenha.setText(f'Dados Atuais: Email: {email} | '
                                                  f'Senha: {"".join([letra.replace(letra, "*") for letra in senha])}')
            else:
                self.statusRemetenteSenha.setText('Os dados de e-mail e/ou a \
                    senha do remetente não estão definidos')
        except Exception as e:
            self.statusOperacoes.setText(f'{e.__class__.__name__}: {e}')

    def adicionarEmailRemetenteSenha(self):
        try:
            self.statusOperacoes.setText('')
            emailRemetente = self.emailUsuario.text()
            senhaRemetente = self.senhaUsuario.text()
            if emailRemetente == '' or senhaRemetente == '':
                self.statusOperacoes.setText('Entre com o e-mail e senha ! ')
                return
            else:
                self.adicionarEmailRemetente(emailRemetente)
                self.adicionarSenhaRemetente(senhaRemetente)
                self.emailUsuario.clear()
                self.senhaUsuario.clear()
                self.manipuladorRemetenteSenha()
        except Exception as e:
            self.statusOperacoes.setText(f'{e.__class__.__name__}: {e}')

    def adicionarEmailRemetente(self, email: str):
        try:
            self.defineArquivoEmail(email)
        except Exception as e:
            self.statusOperacoes.setText(f'{e.__class__.__name__}: {e}')

    def adicionarSenhaRemetente(self, senha: str):
        try:
            self.defineArquivoSenha(senha)
        except Exception as e:
            self.statusOperacoes.setText(f'{e.__class__.__name__}: {e}')

    def manipuladorDestinatarios(self) -> None:
        try:
            emailDestinatarios = my_recipients()
            self.tabelaDestinatarios.setRowCount(len(emailDestinatarios))
            for linha, email in enumerate(emailDestinatarios):
                self.tabelaDestinatarios.setItem(linha, 0, QTableWidgetItem(email))
        except Exception:
            self.statusOperacoes.setText('Defina as configurações de e-mail.')

    def obterEmailDestinatario(self) -> str:
        try:
            emailDeletado: str = self.tabelaDestinatarios.currentItem().text().strip()
            return emailDeletado
        except Exception:
            return None

    def deletarEmailDestinatario(self):
        try:
            emailDestinatarios: list = my_recipients()
            emailDeletado = self.obterEmailDestinatario()
            if emailDeletado:
                emailDestinatarios.remove(emailDeletado)
                self.apagadorArquivo('.RECIPIENTS_USER_DATA.txt')
                for email in emailDestinatarios:
                    self.defineArquivoDestinatarios(email)
                self.manipuladorDestinatarios()
            else:
                if len(emailDestinatarios) == 0:
                    self.statusOperacoes.setText('Não há itens para mostrar.')
                else:
                    self.statusOperacoes.setText('Selecione um email na tabela.')
        except Exception as e:
            self.statusOperacoes.setText(f'{e.__class__.__name__}: {e}')

    def adicionarEmailDestinatarios(self):
        try:
            emailDestinatario: str = self.adicionarDestinatario.text().strip()
            if emailDestinatario:
                self.defineArquivoDestinatarios(emailDestinatario)
                self.statusOperacoes.setText(f'{emailDestinatario}: Dado gravado com sucesso.')
                self.manipuladorDestinatarios()
                self.adicionarDestinatario.clear()
            else:
                self.statusOperacoes.setText('Digite um e-mail')
        except Exception as e:
            self.statusOperacoes.setText(f'{e.__class__.__name__}: {e}')

    def executarEmailTeste(self):
        try:
            self.emailTesteThread = QThread(parent=None)
            self.emailTesteWorker = WorkerEmailTesteConexao()
            self.emailTesteWorker.moveToThread(self.emailTesteThread)
            self.emailTesteThread.started.connect(self.emailTesteWorker.run)
            self.emailTesteThread.start()
            self.emailTesteWorker.msgEnvio.connect(lambda msg: self.statusOperacoes.setText(msg))
            self.emailTesteWorker.termino.connect(self.emailTesteThread.quit)
            self.emailTesteWorker.termino.connect(self.emailTesteThread.wait)
            self.emailTesteWorker.termino.connect(self.emailTesteThread.deleteLater)
            self.emailTesteWorker.termino.connect(self.emailTesteWorker.deleteLater)
        except Exception as e:
            self.statusOperacoes.setText(f'{e.__class__.__name__}: {e}')


if __name__ == '__main__':
    qt = QApplication(sys.argv)
    iuEstacao = InterfaceEstacao()
    iuEstacao.show()
    qt.exec_()
