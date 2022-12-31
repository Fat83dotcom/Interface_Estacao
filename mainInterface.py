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


def leia_me():
    with open('LEIA_ME.txt', 'w') as file:
        texto = '''
                ***
                Para usar corretamente este programa, você deve observar os seguintes procedimentos:
                -> No arquivo "EMAIL_USER_DATA" é o local onde o usuário irá configurar seu login de
                email, respeitando algumas regras simples que, se não seguidas, podem ocasionar
                funcionamento inesperado, erros ou a quebra do programa.
                AS REGRAS SÃO:
                -> NA PRIMEIRA E SEGUNDA LINHA DO ARQUIVO, NOS CAMPOS "MEU EMAIL" E "MINHA SENHA", APÓS ":" COLOQUE UM (1) ESPAÇO E APENAS UM (1)
                ESPAÇO, E CASO ESSA REGRA NÃO SEJA SEGUIDA, O PROGRAMA NÃO LERÁ CORRETAMENTE OS DADOS E NÃO ENVIARÁ OS EMAILS CORRETAMENTE.
                -> NA TERCEIRA LINHA, INSIRA OS EMAILS DOS DESTINATARIOS, SEPARADOS POR VIRGULAS E SEM QUEBRAS DE LINHA.
                SE HOUVER QUEBRA DE LINHA, O PROGRAMA AINDA ENVIARÁ OS EMAILS MAS OCORRERÁ ERROS E OMISSÕES DE DADOS INDESEJADAS.
                -> SEGUINDO ESSAS REGRAS É ESPERADO QUE OS EMAILS SEJAM ENVIADOS SEM PROBLEMAS E, CASO ACONTEÇA ALGUM
                PROBLEMA, POR FAVOR, ENTRAR EM CONTATO COM O DESENVOLVEDOR EXPLICANDO O PROBLEMA.
                OBRIGADO!!!
                ***
        '''
        file.write(texto)


def renderizadorHtml(umidade, pressao, temp1, temp2, temp1max, temp1min,
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


def data() -> str:
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


def plot_umidade(uy, inicio, path):
    try:
        ux = range(len(uy))
        file = f'{path}/Umidade{inicio}.pdf'
        plt.title(f'Gráfico Umidade\n-> Inicio: {inicio} <-|-> Termino: {data()} <-\nMáxima: {maximos(uy)} --- Mínima: {minimos(uy)}')
        plt.xlabel('Tempo em segundos.')
        plt.ylabel('Umidade Relativa do Ar %')
        plt.plot(ux, uy)
        plt.savefig(file)
        plt.clf()
    except (ValueError, Exception) as e:
        raise e


def plot_pressao(py, inicio, path):
    try:
        px = range(len(py))
        file = f'{path}/Pressao{inicio}.pdf'
        plt.title(f'Gráfico Pressão\n-> Inicio: {inicio} <-|-> Termino: {data()} <-\nMáxima: {maximos(py)} --- Mínima: {minimos(py)}')
        plt.xlabel('Tempo em segundos.')
        plt.ylabel('Pressão Atmosferica em hPa')
        plt.plot(px, py)
        plt.savefig(file)
        plt.clf()
    except (ValueError, Exception) as e:
        raise e


def plot_temp1(t1y, inicio, path):
    try:
        t1x = range(len(t1y))
        file = f'{path}/Temperatura_Interna{inicio}.pdf'
        plt.title(f'Gráfico Temp Interna\n-> Inicio: {inicio} <-|-> Termino: {data()} <-\nMáxima: {maximos(t1y)} --- Mínima: {minimos(t1y)}')
        plt.xlabel('Tempo em segundos.')
        plt.ylabel('Temperatura em °C')
        plt.plot(t1x, t1y)
        plt.savefig(file)
        plt.clf()
    except (ValueError, Exception) as e:
        raise e


def plot_temp2(t2y, inicio, path):
    try:
        t2x = range(len(t2y))
        file = f'{path}/Temperatura_Externa{inicio}.pdf'
        plt.title(f'Gráfico Temp Externa\n-> Inicio: {inicio} <-|-> Termino: {data()} <-\nMáxima: {maximos(t2y)} --- Mínima: {minimos(t2y)}')
        plt.xlabel('Tempo em segundos.')
        plt.ylabel('Temperatura em °C')
        plt.plot(t2x, t2y)
        plt.savefig(file)
        plt.clf()
    except (ValueError, Exception) as e:
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
            msg['subject'] = f'Teste de Conexão {data()}'
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

    @staticmethod
    def __anexadorPdf(enderecoPdf, msg):
        with open(enderecoPdf, 'rb') as pdf:
            anexo = MIMEApplication(pdf.read(), _subtype='pdf')
            pdf.close()
            anexo.add_header('Conteudo', enderecoPdf)
            msg.attach(anexo)

    @pyqtSlot()
    def run(self):
        try:
            msg = MIMEMultipart()
            msg['from'] = ''.join(meu_email())
            msg['to'] = ','.join(my_recipients())
            msg['subject'] = f'Monitoramento Estação Metereologica Fat83dotcom {data()}'
            corpo = MIMEText(renderizadorHtml(self.umi, self.press, self.t1, self.t2,
                             self.t1max, self.t1min, self.t2max, self.t2min,
                             self.umimax, self.umimini, self.pressmax, self.pressmini,
                             self.inicio, self.fim, data()), 'html')
            msg.attach(corpo)

            umidade = f'{self.path}/Umidade{self.inicio}.pdf'
            pressao = f'{self.path}/Pressao{self.inicio}.pdf'
            tmp1 = f'{self.path}/Temperatura_Interna{self.inicio}.pdf'
            temp2 = f'{self.path}/Temperatura_Externa{self.inicio}.pdf'

            self.__anexadorPdf(umidade, msg)
            self.__anexadorPdf(pressao, msg)
            self.__anexadorPdf(tmp1, msg)
            self.__anexadorPdf(temp2, msg)
            
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
            os.remove(f'{self.path}/Umidade{self.inicio}.pdf')
            os.remove(f'{self.path}/Pressao{self.inicio}.pdf')
            os.remove(f'{self.path}/Temperatura_Interna{self.inicio}.pdf')
            os.remove(f'{self.path}/Temperatura_Externa{self.inicio}.pdf')
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

    def bufferingDados(self) -> list:
        bufferDadosArduino: list = []
        self.arduino.reset_input_buffer()
        while len(bufferDadosArduino) < 4:
            self.arduino.write('u'.encode('utf-8'))
            sleep(0.1)
            if self.arduino.in_waiting:
                dado = self.arduino.readline().decode('utf-8')
                bufferDadosArduino.append(dado.strip())
            self.arduino.write('p'.encode('utf-8'))
            sleep(0.1)
            if self.arduino.in_waiting:
                dado = self.arduino.readline().decode('utf-8')
                bufferDadosArduino.append(dado.strip())
            self.arduino.write('1'.encode('utf-8'))
            sleep(0.1)
            if self.arduino.in_waiting:
                dado = self.arduino.readline().decode('utf-8')
                bufferDadosArduino.append(dado.strip())
            self.arduino.write('2'.encode('utf-8'))
            sleep(0.1)
            if self.arduino.in_waiting:
                dado = self.arduino.readline().decode('utf-8')
                bufferDadosArduino.append(dado.strip())
        return bufferDadosArduino

    def enviarDadosTempoRealParaLCD(self, dados: dict) -> None:
        dadosMostradorLcd: list = []
        dadosMostradorLcd.append(dados["u"])
        dadosMostradorLcd.append(dados["p"])
        dadosMostradorLcd.append(dados["1"])
        dadosMostradorLcd.append(dados["2"])
        self.saidaData.emit(data())
        self.saidaDadosLCD.emit(dadosMostradorLcd)

    def atualizarBarraProgresso(self, tempoTotal, contadorTempoCorrente) -> None:
        percentualTempoCorrido: int = self.porcentagem(tempoTotal, contadorTempoCorrente)
        self.barraProgresso.emit(percentualTempoCorrido)

    def atualizarTempoRestante(self, tempoTotal, contadorTempoRestante) -> None:
        self.mostradorTempoRestante.emit((tempoTotal - contadorTempoRestante) - 1)

    def registradorDadosArquivo(self, dadosAGravar: dict) -> None:
        with open(dataDoArquivo(), 'a+', newline='', encoding='utf-8') as log:
            try:
                w = csv.writer(log)
                w.writerow([data(), dadosAGravar['u'], dadosAGravar['p'],
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
                    self.saidaInfoInicio.emit(f'Inicio: --> {data()} <--')
                else:
                    self.saidaInfoInicio.emit(f'Parcial {contadorParciais} --> {data()} <--')

                inicioParcial: str = data()

                yDadosUmidade: list = []
                yDadosPressao: list = []
                yDadosTemperaturaInterna: list = []
                yDadosTemperaturaExterna: list = []

                cS = count()
                contadorSegundos: int = next(cS)
                contadorSegundosRestantes: int = 0

                while (contadorSegundos < tempoEmSegundos) and not self.paradaPrograma:
                    inicioDelimitadorDeTempo: float = time.time()
                    dadosRecebidosArduino: dict = {
                        'u': '',
                        'p': '',
                        '1': '',
                        '2': ''
                    }

                    tratamentoBuffer: list = self.bufferingDados()
                    if len(tratamentoBuffer) > 4:
                        for _ in range(len(tratamentoBuffer) - 4):
                            tratamentoBuffer.pop()
                    for dado in tratamentoBuffer:
                        dadosRecebidosArduino[dado[0]] = dado[2:]

                    self.registradorDadosArquivo(dadosRecebidosArduino)

                    yDadosUmidade.append(float(dadosRecebidosArduino['u']))
                    yDadosPressao.append(float(dadosRecebidosArduino['p']))
                    yDadosTemperaturaInterna.append(float(dadosRecebidosArduino['1']))
                    yDadosTemperaturaExterna.append(float(dadosRecebidosArduino['2']))

                    self.enviarDadosTempoRealParaLCD(dadosRecebidosArduino)

                    contadorSegundos = next(cS)
                    self.atualizarBarraProgresso(tempoEmSegundos, contadorSegundos)
                    self.atualizarTempoRestante(tempoEmSegundos, contadorSegundosRestantes)
                    contadorSegundosRestantes += 1

                    terminoDelimitadorDeTempo: float = time.time()
                    while (terminoDelimitadorDeTempo - inicioDelimitadorDeTempo) < 1:
                        terminoDelimitadorDeTempo = time.time()
                contadorParciais = next(cP)
                plot_umidade(yDadosUmidade, inicioParcial, caminhoDiretorio)
                plot_pressao(yDadosPressao, inicioParcial, caminhoDiretorio)
                plot_temp1(yDadosTemperaturaInterna, inicioParcial, caminhoDiretorio)
                plot_temp2(yDadosTemperaturaExterna, inicioParcial, caminhoDiretorio)
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
                                data(),
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
