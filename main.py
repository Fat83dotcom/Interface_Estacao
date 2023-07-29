import sys
from PySide2.QtWidgets import QApplication
from Interface.InterfaceManager import InterfaceEstacao
from DataBaseManager.LogFiles import LogErrorsMixin


if __name__ == '__main__':
    errors = LogErrorsMixin()
    try:
        qt = QApplication(sys.argv)
        iuEstacao = InterfaceEstacao()
        iuEstacao.show()
        qt.exec_()
    except Exception as e:
        className = e.__class__.__name__
        methName = 'iuEstacao'
        errors.registerErrors(className, methName, e)
