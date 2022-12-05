import sys
from interface import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QApplication
import os
import serial
from serial import Serial
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import QThread
from sensor_bme280_term_10K import main, define_arquivo


class InterfaceEstacao(QMainWindow, Ui_MainWindow):
    
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        super().setupUi(self)
        
    def inicializacaoArduino(self):
        set_porta = '/dev/ttyUSB0'

        while set_porta:
            try:
                arduino = Serial(set_porta, 9600, timeout=1, bytesize=serial.EIGHTBITS)
                arduino.reset_input_buffer()
                return arduino
            except Exception as erro:
                print(erro)
                set_porta = self.portaArduino.text()
    
    def execucaoMainEstacao(self):
        if os.path.isfile('EMAIL_USER_DATA.txt'):
            print('Arquivo "EMAIL_USER_DATA.txt" já existe.')
        else:
            define_arquivo()
            print('Arquivo "EMAIL_USER_DATA.txt" foi criado, por favor, configure antes de continuar. Tecle enter para continuar...')
        arduino = self.inicializacaoArduino()
        main(arduino)


if __name__ == '__main__':
    qt = QApplication(sys.argv)
    iuEstacao = InterfaceEstacao()
    iuEstacao.show()
    qt.exec_()
