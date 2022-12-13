import sys
import serial
import os
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import QThread, QObject, pyqtSignal
from interface import Ui_MainWindow
from serial import Serial
from confidentials import define_arquivo
import time
import csv
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf
import smtplib
from threading import Thread
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from confidentials import meu_email, minha_senha, my_recipients
from statistics import mean
from string import Template
from itertools import count
from math import nan


class Worker(QObject):
    finalizar = pyqtSignal()
    barraProgresso = pyqtSignal(int)
    saidaInfo = pyqtSignal(str)

    def __init__(self, portaArduino, tempoGrafico, parent=None) -> None:
        super().__init__(parent)
        self.porta = portaArduino
        self.tempoGraf = tempoGrafico
        self.tempoConvertido = TransSegundos(self.tempoGraf)
        self.paradaPrograma = False

    def porcentagem(self, totalVoltas, voltaAtual) -> int:
        porcentagem = voltaAtual * 100 / totalVoltas
        return int(porcentagem)

    def run(self):
        caminhoDiretorio = os.path.dirname(os.path.realpath(__file__))
        try:
            arduino = Serial(self.porta, 9600, timeout=1, bytesize=serial.EIGHTBITS)
            arduino.reset_input_buffer()
            self.saidaInfo.emit(f'O Arduíno foi conectado na porta: {self.porta}')
        except Exception as e:
            self.saidaInfo.emit(f'{e.__class__.__name__}: {e}')
            self.saidaInfo.emit('Entre com uma porta USB ou verifique a entrada USB.')
            self.finalizar.emit()

        if os.path.isfile('EMAIL_USER_DATA.txt'):
            self.saidaInfo.emit('Arquivo "EMAIL_USER_DATA.txt" já existe.')
        else:
            define_arquivo()
            self.saidaInfo.emit('Arquivo "EMAIL_USER_DATA.txt" foi criado, por favor, configure antes de continuar.')
        c3 = count()
        contador3 = next(c3)
        while not self.paradaPrograma:
            if contador3 == 0:
                tempo_graf = self.tempoConvertido.conversorHorasSegundo()
                if tempo_graf == 0:
                    self.saidaInfo.emit('Entre com um tempo maior que zero !!!')
                    self.finalizar.emit()
                arduino.reset_input_buffer()
                self.saidaInfo.emit(f'Inicio: --> {data()} <--')
            else:
                self.saidaInfo.emit(f'Parcial {contador3} --> {data()} <--')

            inicio = data()

            yDadosUmidade = []
            yDadosPressao = []
            yDadosTemperaturaInterna = []
            yDadosTemperaturaExterna = []

            dadosRecebidosArduino = {
                'u': '',
                'p': '',
                '1': '',
                '2': ''
            }
            c2 = count()
            contador2 = next(c2)
            while (contador2 < tempo_graf) and not self.paradaPrograma:
                tempoInicial = time.time()
                c1 = count()
                contador1 = next(c1)
                while contador1 < 4:
                    try:
                        dado = str(arduino.readline())
                        dado = dado[2:-5]
                        if float(dado[1:].strip()) == nan:
                            continue
                        else:
                            if dado[0] == 'u':
                                dadosRecebidosArduino['u'] = float(dado[1:].strip())
                            if dado[0] == 'p':
                                dadosRecebidosArduino['p'] = float(dado[1:].strip())
                            if dado[0] == '1':
                                dadosRecebidosArduino['1'] = float(dado[1:].strip())
                            if dado[0] == '2':
                                dadosRecebidosArduino['2'] = float(dado[1:].strip())
                    except (ValueError, IndexError, Exception):
                        ...
                    contador1 = next(c1)

                with open(dataDoArquivo(), 'a+', newline='', encoding='utf-8') as log:
                    try:
                        w = csv.writer(log)
                        w.writerow([data(), dadosRecebidosArduino['u'], dadosRecebidosArduino['p'],
                                    dadosRecebidosArduino['1'], dadosRecebidosArduino['2']])
                        yDadosUmidade.append(float(dadosRecebidosArduino['u']))
                        yDadosPressao.append(float(dadosRecebidosArduino['p']))
                        yDadosTemperaturaInterna.append(float(dadosRecebidosArduino['1']))
                        yDadosTemperaturaExterna.append(float(dadosRecebidosArduino['2']))
                        contador2 = next(c2)
                        percent: int = self.porcentagem(tempo_graf, contador2)
                        self.barraProgresso.emit(percent)
                    except ValueError:
                        ...

                tempoFinal = time.time()
                while tempoFinal - tempoInicial < 1:
                    tempoFinal = time.time()
            plot_umidade(yDadosUmidade, inicio, caminhoDiretorio)
            plot_pressao(yDadosPressao, inicio, caminhoDiretorio)
            plot_temp1(yDadosTemperaturaInterna, inicio, caminhoDiretorio)
            plot_temp2(yDadosTemperaturaExterna, inicio, caminhoDiretorio)
            contador3 = next(c3)
            emaail = EmailThread(
                                inicio=inicio,
                                umi=round(mean(yDadosUmidade), 2),
                                press=round(mean(yDadosPressao), 2),
                                t1=round(mean(yDadosTemperaturaInterna), 2),
                                t2=round(mean(yDadosTemperaturaExterna), 2),
                                t1max=maximos(yDadosTemperaturaInterna),
                                t1min=minimos(yDadosTemperaturaInterna),
                                t2max=maximos(yDadosTemperaturaExterna),
                                t2min=minimos(yDadosTemperaturaExterna),
                                umimax=maximos(yDadosUmidade),
                                umimini=minimos(yDadosUmidade),
                                pressmax=maximos(yDadosPressao),
                                pressmini=minimos(yDadosPressao),
                                ini=inicio,
                                fim=data(),
                                path=caminhoDiretorio)
            emaail.start()
            self.saidaInfo.emit('Email Enviado')
        self.saidaInfo.emit('Programa Parado !!!')
        self.finalizar.emit()
        self.barraProgresso.emit(0)


class EmailThread(Thread):
    def __init__(self, inicio, umi, press, t1, t2, t1max,
                 t1min, t2max, t2min, umimax, umimini,
                 pressmax, pressmini, ini, fim, path):
        super().__init__()
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
        self.ini = ini
        self.fim = fim

    @staticmethod
    def __anexadorPdf(enderecoPdf, msg):
        with open(enderecoPdf, 'rb') as pdf:
            anexo = MIMEApplication(pdf.read(), _subtype='pdf')
            pdf.close()
            anexo.add_header('Conteudo', enderecoPdf)
            msg.attach(anexo)

    def run(self):
        msg = MIMEMultipart()
        msg['from'] = 'Fernando Mendes'
        msg['to'] = ','.join(my_recipients())
        msg['subject'] = f'Monitoramento Estação Metereologica Fat83dotcom {data()}'
        corpo = MIMEText(renderizadorHtml(self.umi, self.press, self.t1, self.t2,
                         self.t1max, self.t1min, self.t2max, self.t2min,
                         self.umimax, self.umimini, self.pressmax, self.pressmini,
                         self.ini, self.fim, data()), 'html')
        msg.attach(corpo)

        umidade = f'{self.path}/Umidade{self.inicio}.pdf'
        pressao = f'{self.path}/Pressao{self.inicio}.pdf'
        tmp1 = f'{self.path}/Temperatura_Interna{self.inicio}.pdf'
        temp2 = f'{self.path}/Temperatura_Externa{self.inicio}.pdf'

        self.__anexadorPdf(umidade, msg)
        self.__anexadorPdf(pressao, msg)
        self.__anexadorPdf(tmp1, msg)
        self.__anexadorPdf(temp2, msg)
        try:
            with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.login(''.join(meu_email()), ''.join(minha_senha()))
                smtp.send_message(msg)
        except Exception:
            print('\nE-mail não enviado, sem conexão.\n\nVerifique a rede.\n')

        os.remove(f'{self.path}/Umidade{self.inicio}.pdf')
        os.remove(f'{self.path}/Pressao{self.inicio}.pdf')
        os.remove(f'{self.path}/Temperatura_Interna{self.inicio}.pdf')
        os.remove(f'{self.path}/Temperatura_Externa{self.inicio}.pdf')


class TransSegundos:
    def __init__(self, horas) -> None:
        self.horas = horas

    def conversorHorasSegundo(self) -> int:
        horas = self.horas[:2]
        minutos = self.horas[3:]
        segundos = int(int(horas) * 3600 + int(minutos) * 60)
        return segundos


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


def data():
    data = time.strftime('%d %b %Y %H:%M:%S', time.localtime())
    return data


def dataDoArquivo():
    dataA = time.strftime('%b_%Y_log.csv').lower()
    return dataA


def maximos(dados):
    return round(max(dados), 2)


def minimos(dados):
    return round(min(dados), 2)


def plot_umidade(uy, inicio, path):
    ux = range(len(uy))
    file = f'{path}/Umidade{inicio}.pdf'
    plt.title(f'Gráfico Umidade\n-> Inicio: {inicio} <-|-> Termino: {data()} <-\nMáxima: {maximos(uy)} --- Mínima: {minimos(uy)}')
    plt.xlabel('Tempo em segundos.')
    plt.ylabel('Umidade Relativa do Ar %')
    plt.plot(ux, uy)
    plt.savefig(file)
    plt.clf()


def plot_pressao(py, inicio, path):
    px = range(len(py))
    file = f'{path}/Pressao{inicio}.pdf'
    plt.title(f'Gráfico Pressão\n-> Inicio: {inicio} <-|-> Termino: {data()} <-\nMáxima: {maximos(py)} --- Mínima: {minimos(py)}')
    plt.xlabel('Tempo em segundos.')
    plt.ylabel('Pressão Atmosferica em hPa')
    plt.plot(px, py)
    plt.savefig(file)
    plt.clf()


def plot_temp1(t1y, inicio, path):
    t1x = range(len(t1y))
    file = f'{path}/Temperatura_Interna{inicio}.pdf'
    plt.title(f'Gráfico Temp Interna\n-> Inicio: {inicio} <-|-> Termino: {data()} <-\nMáxima: {maximos(t1y)} --- Mínima: {minimos(t1y)}')
    plt.xlabel('Tempo em segundos.')
    plt.ylabel('Temperatura em °C')
    plt.plot(t1x, t1y)
    plt.savefig(file)
    plt.clf()


def plot_temp2(t2y, inicio, path):
    t2x = range(len(t2y))
    file = f'{path}/Temperatura_Externa{inicio}.pdf'
    plt.title(f'Gráfico Temp Externa\n-> Inicio: {inicio} <-|-> Termino: {data()} <-\nMáxima: {maximos(t2y)} --- Mínima: {minimos(t2y)}')
    plt.xlabel('Tempo em segundos.')
    plt.ylabel('Temperatura em °C')
    plt.plot(t2x, t2y)
    plt.savefig(file)
    plt.clf()


class InterfaceEstacao(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        super().setupUi(self)
        self.btnInciarEstacao.clicked.connect(self.execucaoMainEstacao)
        self.btnPararEstacao.setEnabled(False)
        self.modelo = QStandardItemModel()
        self.saidaDetalhes.setModel(self.modelo)

    def mostradorDisplayInfo(self, info):
        self.modelo.appendRow(QStandardItem(info))

    def mostrardorDisplayBarraProgresso(self, percent):
        self.barraProgresso.setValue(percent)

    def execucaoMainEstacao(self):
        self.porta = self.portaArduino.text()
        self.tempoGrafico = self.tempoGraficos.text()
        self.thread = QThread()
        self.worker = Worker(portaArduino=self.porta, tempoGrafico=self.tempoGrafico)
        self.worker.moveToThread(self.thread)
        self.worker.finalizar.connect(self.thread.quit)
        self.worker.finalizar.connect(self.worker.deleteLater)
        self.worker.finalizar.connect(self.thread.deleteLater)
        self.worker.saidaInfo.connect(self.mostradorDisplayInfo)
        self.thread.started.connect(self.worker.run)
        self.thread.start()
        self.worker.barraProgresso.connect(self.mostrardorDisplayBarraProgresso)
        self.btnInciarEstacao.setEnabled(False)
        self.btnPararEstacao.setEnabled(True)
        self.thread.finished.connect(
            lambda: self.btnInciarEstacao.setEnabled(True)
        )

        def pararThread():
            self.worker.paradaPrograma = True
            self.btnPararEstacao.setEnabled(False)

        self.btnPararEstacao.clicked.connect(pararThread)


if __name__ == '__main__':
    qt = QApplication(sys.argv)
    iuEstacao = InterfaceEstacao()
    iuEstacao.show()
    qt.exec_()
