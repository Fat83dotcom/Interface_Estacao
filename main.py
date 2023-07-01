import sys
from PySide2.QtWidgets import QApplication
from Interface.InterfaceManager import InterfaceEstacao


if __name__ == '__main__':
    qt = QApplication(sys.argv)
    iuEstacao = InterfaceEstacao()
    iuEstacao.show()
    qt.exec_()
