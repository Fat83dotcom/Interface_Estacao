import sys
import serial
import os
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import QThread, QObject, pyqtSignal
from interface import Ui_MainWindow
from serial import Serial
from sensor_bme280_term_10K import main, define_arquivo


class Worker(QObject):
    finalizar = pyqtSignal()
    progresso = pyqtSignal()

    def run(self, arduino):
        if os.path.isfile('EMAIL_USER_DATA.txt'):
            print('Arquivo "EMAIL_USER_DATA.txt" já existe.')
        else:
            define_arquivo()
            print('Arquivo "EMAIL_USER_DATA.txt" foi criado, por favor, configure antes de continuar. Tecle enter para continuar...')
        arduino = self.inicializacaoArduino()
        main(arduino)


class InterfaceEstacao(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        super().setupUi(self)
        self.btnInciarEstacao.clicked.connect(self.execucaoMainEstacao)

    def inicializacaoArduino(self):
        set_porta = self.portaArduino.text()

        try:
            arduino = Serial(set_porta, 9600, timeout=1, bytesize=serial.EIGHTBITS)
            # print(arduino)
            arduino.reset_input_buffer()
            return arduino
        except Exception as erro:
            print(erro)
            set_porta = self.portaArduino.text()

    def execucaoMainEstacao(self):
        self.thread = QThread()


if __name__ == '__main__':
    qt = QApplication(sys.argv)
    iuEstacao = InterfaceEstacao()
    iuEstacao.show()
    qt.exec_()
