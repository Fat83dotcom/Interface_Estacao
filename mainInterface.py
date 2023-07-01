# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'interface.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import icons_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(686, 582)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        palette = QPalette()
        brush = QBrush(QColor(255, 255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.WindowText, brush)
        brush1 = QBrush(QColor(36, 31, 49, 255))
        brush1.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Button, brush1)
        brush2 = QBrush(QColor(54, 46, 73, 255))
        brush2.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Light, brush2)
        brush3 = QBrush(QColor(45, 38, 61, 255))
        brush3.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Midlight, brush3)
        brush4 = QBrush(QColor(18, 15, 24, 255))
        brush4.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Dark, brush4)
        brush5 = QBrush(QColor(24, 21, 33, 255))
        brush5.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Mid, brush5)
        palette.setBrush(QPalette.Active, QPalette.Text, brush)
        palette.setBrush(QPalette.Active, QPalette.BrightText, brush)
        palette.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        brush6 = QBrush(QColor(0, 0, 0, 255))
        brush6.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Base, brush6)
        palette.setBrush(QPalette.Active, QPalette.Window, brush1)
        palette.setBrush(QPalette.Active, QPalette.Shadow, brush6)
        palette.setBrush(QPalette.Active, QPalette.AlternateBase, brush4)
        brush7 = QBrush(QColor(255, 255, 220, 255))
        brush7.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.ToolTipBase, brush7)
        palette.setBrush(QPalette.Active, QPalette.ToolTipText, brush6)
        brush8 = QBrush(QColor(255, 255, 255, 128))
        brush8.setStyle(Qt.SolidPattern)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Active, QPalette.PlaceholderText, brush8)
#endif
        palette.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Button, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Light, brush2)
        palette.setBrush(QPalette.Inactive, QPalette.Midlight, brush3)
        palette.setBrush(QPalette.Inactive, QPalette.Dark, brush4)
        palette.setBrush(QPalette.Inactive, QPalette.Mid, brush5)
        palette.setBrush(QPalette.Inactive, QPalette.Text, brush)
        palette.setBrush(QPalette.Inactive, QPalette.BrightText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush6)
        palette.setBrush(QPalette.Inactive, QPalette.Window, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Shadow, brush6)
        palette.setBrush(QPalette.Inactive, QPalette.AlternateBase, brush4)
        palette.setBrush(QPalette.Inactive, QPalette.ToolTipBase, brush7)
        palette.setBrush(QPalette.Inactive, QPalette.ToolTipText, brush6)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush8)
#endif
        palette.setBrush(QPalette.Disabled, QPalette.WindowText, brush4)
        palette.setBrush(QPalette.Disabled, QPalette.Button, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Light, brush2)
        palette.setBrush(QPalette.Disabled, QPalette.Midlight, brush3)
        palette.setBrush(QPalette.Disabled, QPalette.Dark, brush4)
        palette.setBrush(QPalette.Disabled, QPalette.Mid, brush5)
        palette.setBrush(QPalette.Disabled, QPalette.Text, brush4)
        palette.setBrush(QPalette.Disabled, QPalette.BrightText, brush)
        palette.setBrush(QPalette.Disabled, QPalette.ButtonText, brush4)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Window, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Shadow, brush6)
        palette.setBrush(QPalette.Disabled, QPalette.AlternateBase, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.ToolTipBase, brush7)
        palette.setBrush(QPalette.Disabled, QPalette.ToolTipText, brush6)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush8)
#endif
        MainWindow.setPalette(palette)
        MainWindow.setTabletTracking(False)
        icon = QIcon()
        iconThemeName = u"brainstorm"
        if QIcon.hasThemeIcon(iconThemeName):
            icon = QIcon.fromTheme(iconThemeName)
        else:
            icon.addFile(u"iconebrain.png", QSize(), QIcon.Normal, QIcon.Off)
            icon.addFile(u"iconebrain.png", QSize(), QIcon.Normal, QIcon.On)
            icon.addFile(u"iconebrain.png", QSize(), QIcon.Disabled, QIcon.Off)
            icon.addFile(u"iconebrain.png", QSize(), QIcon.Disabled, QIcon.On)
            icon.addFile(u"iconebrain.png", QSize(), QIcon.Active, QIcon.Off)
            icon.addFile(u"iconebrain.png", QSize(), QIcon.Active, QIcon.On)
            icon.addFile(u"iconebrain.png", QSize(), QIcon.Selected, QIcon.Off)
            icon.addFile(u"iconebrain.png", QSize(), QIcon.Selected, QIcon.On)
        
        MainWindow.setWindowIcon(icon)
        MainWindow.setLayoutDirection(Qt.LeftToRight)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setLayoutDirection(Qt.LeftToRight)
        self.verticalLayout_4 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setLayoutDirection(Qt.LeftToRight)
        self.tabWidget.setTabPosition(QTabWidget.North)
        self.tabWidget.setTabShape(QTabWidget.Rounded)
        self.paginaApresentacao = QWidget()
        self.paginaApresentacao.setObjectName(u"paginaApresentacao")
        self.verticalLayout_59 = QVBoxLayout(self.paginaApresentacao)
        self.verticalLayout_59.setObjectName(u"verticalLayout_59")
        self.frameContainerPrincipal = QFrame(self.paginaApresentacao)
        self.frameContainerPrincipal.setObjectName(u"frameContainerPrincipal")
        self.frameContainerPrincipal.setFrameShape(QFrame.StyledPanel)
        self.frameContainerPrincipal.setFrameShadow(QFrame.Raised)
        self.verticalLayout_31 = QVBoxLayout(self.frameContainerPrincipal)
        self.verticalLayout_31.setObjectName(u"verticalLayout_31")
        self.home = QFrame(self.frameContainerPrincipal)
        self.home.setObjectName(u"home")
        self.home.setFrameShape(QFrame.Panel)
        self.home.setFrameShadow(QFrame.Sunken)
        self.home.setLineWidth(2)
        self.verticalLayout_5 = QVBoxLayout(self.home)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.TituloCabecalho = QLabel(self.home)
        self.TituloCabecalho.setObjectName(u"TituloCabecalho")
        self.TituloCabecalho.setMaximumSize(QSize(16777215, 30))
        font = QFont()
        font.setPointSize(18)
        font.setBold(False)
        font.setWeight(50)
        self.TituloCabecalho.setFont(font)
        self.TituloCabecalho.setAlignment(Qt.AlignCenter)

        self.verticalLayout_5.addWidget(self.TituloCabecalho)


        self.verticalLayout_31.addWidget(self.home)

        self.primeiraParteTexto = QLabel(self.frameContainerPrincipal)
        self.primeiraParteTexto.setObjectName(u"primeiraParteTexto")
        self.primeiraParteTexto.setMinimumSize(QSize(626, 0))
        font1 = QFont()
        font1.setPointSize(14)
        self.primeiraParteTexto.setFont(font1)
        self.primeiraParteTexto.setAlignment(Qt.AlignCenter)

        self.verticalLayout_31.addWidget(self.primeiraParteTexto)

        self.segundaParteTexto = QLabel(self.frameContainerPrincipal)
        self.segundaParteTexto.setObjectName(u"segundaParteTexto")

        self.verticalLayout_31.addWidget(self.segundaParteTexto)

        self.rodaPe = QLabel(self.frameContainerPrincipal)
        self.rodaPe.setObjectName(u"rodaPe")

        self.verticalLayout_31.addWidget(self.rodaPe)


        self.verticalLayout_59.addWidget(self.frameContainerPrincipal)

        self.tabWidget.addTab(self.paginaApresentacao, "")
        self.inicioEstacao = QWidget()
        self.inicioEstacao.setObjectName(u"inicioEstacao")
        self.gridLayout_5 = QGridLayout(self.inicioEstacao)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.frameContainerPincipal = QFrame(self.inicioEstacao)
        self.frameContainerPincipal.setObjectName(u"frameContainerPincipal")
        self.frameContainerPincipal.setFrameShape(QFrame.StyledPanel)
        self.frameContainerPincipal.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frameContainerPincipal)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.frameCabecalhoInicio = QFrame(self.frameContainerPincipal)
        self.frameCabecalhoInicio.setObjectName(u"frameCabecalhoInicio")
        self.frameCabecalhoInicio.setFrameShape(QFrame.Panel)
        self.frameCabecalhoInicio.setFrameShadow(QFrame.Sunken)
        self.frameCabecalhoInicio.setLineWidth(2)
        self.verticalLayout = QVBoxLayout(self.frameCabecalhoInicio)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tituloCabecalho = QLabel(self.frameCabecalhoInicio)
        self.tituloCabecalho.setObjectName(u"tituloCabecalho")
        font2 = QFont()
        font2.setPointSize(18)
        self.tituloCabecalho.setFont(font2)
        self.tituloCabecalho.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.tituloCabecalho)


        self.verticalLayout_3.addWidget(self.frameCabecalhoInicio)

        self.espacador1 = QSpacerItem(228, 37, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_3.addItem(self.espacador1)

        self.frameEntradaEBotoes = QFrame(self.frameContainerPincipal)
        self.frameEntradaEBotoes.setObjectName(u"frameEntradaEBotoes")
        self.frameEntradaEBotoes.setFrameShape(QFrame.NoFrame)
        self.frameEntradaEBotoes.setFrameShadow(QFrame.Raised)
        self.gridLayout_4 = QGridLayout(self.frameEntradaEBotoes)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.tituloPortaUSB = QLabel(self.frameEntradaEBotoes)
        self.tituloPortaUSB.setObjectName(u"tituloPortaUSB")

        self.gridLayout_4.addWidget(self.tituloPortaUSB, 0, 0, 1, 1)

        self.portaArduino = QLineEdit(self.frameEntradaEBotoes)
        self.portaArduino.setObjectName(u"portaArduino")

        self.gridLayout_4.addWidget(self.portaArduino, 0, 1, 1, 1)

        self.tituloTempGrafico = QLabel(self.frameEntradaEBotoes)
        self.tituloTempGrafico.setObjectName(u"tituloTempGrafico")

        self.gridLayout_4.addWidget(self.tituloTempGrafico, 0, 2, 1, 1)

        self.tempoGraficos = QTimeEdit(self.frameEntradaEBotoes)
        self.tempoGraficos.setObjectName(u"tempoGraficos")
        self.tempoGraficos.setMaximumTime(QTime(6, 0, 0))

        self.gridLayout_4.addWidget(self.tempoGraficos, 0, 3, 1, 1)

        self.btnInciarEstacao = QPushButton(self.frameEntradaEBotoes)
        self.btnInciarEstacao.setObjectName(u"btnInciarEstacao")

        self.gridLayout_4.addWidget(self.btnInciarEstacao, 1, 0, 1, 4)

        self.btnPararEstacao = QPushButton(self.frameEntradaEBotoes)
        self.btnPararEstacao.setObjectName(u"btnPararEstacao")

        self.gridLayout_4.addWidget(self.btnPararEstacao, 2, 0, 1, 4)


        self.verticalLayout_3.addWidget(self.frameEntradaEBotoes)

        self.frameBarraELista = QFrame(self.frameContainerPincipal)
        self.frameBarraELista.setObjectName(u"frameBarraELista")
        self.frameBarraELista.setFrameShape(QFrame.NoFrame)
        self.frameBarraELista.setFrameShadow(QFrame.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.frameBarraELista)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.frameContainerBarraProgresso = QFrame(self.frameBarraELista)
        self.frameContainerBarraProgresso.setObjectName(u"frameContainerBarraProgresso")
        self.frameContainerBarraProgresso.setFrameShape(QFrame.Panel)
        self.frameContainerBarraProgresso.setFrameShadow(QFrame.Sunken)
        self.frameContainerBarraProgresso.setLineWidth(2)
        self.horizontalLayout_6 = QHBoxLayout(self.frameContainerBarraProgresso)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.barraProgresso = QProgressBar(self.frameContainerBarraProgresso)
        self.barraProgresso.setObjectName(u"barraProgresso")
        self.barraProgresso.setMaximumSize(QSize(16777215, 16777215))
        self.barraProgresso.setValue(0)

        self.horizontalLayout_6.addWidget(self.barraProgresso)

        self.frameContadorRegressivo = QFrame(self.frameContainerBarraProgresso)
        self.frameContadorRegressivo.setObjectName(u"frameContadorRegressivo")
        self.frameContadorRegressivo.setFrameShape(QFrame.NoFrame)
        self.frameContadorRegressivo.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frameContadorRegressivo)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.visorTempoRestante_2 = QLCDNumber(self.frameContadorRegressivo)
        self.visorTempoRestante_2.setObjectName(u"visorTempoRestante_2")
        self.visorTempoRestante_2.setStyleSheet(u"color: rgb(246, 245, 244);")
        self.visorTempoRestante_2.setFrameShape(QFrame.NoFrame)
        self.visorTempoRestante_2.setDigitCount(5)

        self.gridLayout_2.addWidget(self.visorTempoRestante_2, 0, 0, 1, 1)

        self.barraSeparadora = QLabel(self.frameContadorRegressivo)
        self.barraSeparadora.setObjectName(u"barraSeparadora")
        font3 = QFont()
        font3.setPointSize(15)
        self.barraSeparadora.setFont(font3)
        self.barraSeparadora.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.barraSeparadora, 0, 1, 1, 1)

        self.tempoDefinido_2 = QLCDNumber(self.frameContadorRegressivo)
        self.tempoDefinido_2.setObjectName(u"tempoDefinido_2")
        self.tempoDefinido_2.setStyleSheet(u"color: rgb(246, 245, 244);")
        self.tempoDefinido_2.setFrameShape(QFrame.NoFrame)

        self.gridLayout_2.addWidget(self.tempoDefinido_2, 0, 2, 1, 1)


        self.horizontalLayout_6.addWidget(self.frameContadorRegressivo)


        self.verticalLayout_8.addWidget(self.frameContainerBarraProgresso)

        self.saidaDetalhes = QListView(self.frameBarraELista)
        self.saidaDetalhes.setObjectName(u"saidaDetalhes")
        sizePolicy.setHeightForWidth(self.saidaDetalhes.sizePolicy().hasHeightForWidth())
        self.saidaDetalhes.setSizePolicy(sizePolicy)
        self.saidaDetalhes.setAlternatingRowColors(True)

        self.verticalLayout_8.addWidget(self.saidaDetalhes)


        self.verticalLayout_3.addWidget(self.frameBarraELista)


        self.gridLayout_5.addWidget(self.frameContainerPincipal, 0, 0, 1, 1)

        self.tabWidget.addTab(self.inicioEstacao, "")
        self.mostrarDadosTReal = QWidget()
        self.mostrarDadosTReal.setObjectName(u"mostrarDadosTReal")
        self.mostrarDadosTReal.setEnabled(True)
        self.verticalLayout_2 = QVBoxLayout(self.mostrarDadosTReal)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.frameContainerPrincipalSemLayout = QFrame(self.mostrarDadosTReal)
        self.frameContainerPrincipalSemLayout.setObjectName(u"frameContainerPrincipalSemLayout")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.frameContainerPrincipalSemLayout.sizePolicy().hasHeightForWidth())
        self.frameContainerPrincipalSemLayout.setSizePolicy(sizePolicy1)
        self.frameContainerPrincipalSemLayout.setFrameShape(QFrame.StyledPanel)
        self.frameContainerPrincipalSemLayout.setFrameShadow(QFrame.Raised)
        self.verticalLayout_57 = QVBoxLayout(self.frameContainerPrincipalSemLayout)
        self.verticalLayout_57.setObjectName(u"verticalLayout_57")
        self.cabecalhoExibirDados = QFrame(self.frameContainerPrincipalSemLayout)
        self.cabecalhoExibirDados.setObjectName(u"cabecalhoExibirDados")
        sizePolicy.setHeightForWidth(self.cabecalhoExibirDados.sizePolicy().hasHeightForWidth())
        self.cabecalhoExibirDados.setSizePolicy(sizePolicy)
        self.cabecalhoExibirDados.setFrameShape(QFrame.Panel)
        self.cabecalhoExibirDados.setFrameShadow(QFrame.Sunken)
        self.cabecalhoExibirDados.setLineWidth(2)
        self.verticalLayout_10 = QVBoxLayout(self.cabecalhoExibirDados)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.tituloCabecalho_2 = QLabel(self.cabecalhoExibirDados)
        self.tituloCabecalho_2.setObjectName(u"tituloCabecalho_2")
        self.tituloCabecalho_2.setFont(font2)
        self.tituloCabecalho_2.setAlignment(Qt.AlignCenter)

        self.verticalLayout_10.addWidget(self.tituloCabecalho_2)


        self.verticalLayout_57.addWidget(self.cabecalhoExibirDados)

        self.verticalSpacer = QSpacerItem(18, 4, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_57.addItem(self.verticalSpacer)

        self.frameContainerDados = QFrame(self.frameContainerPrincipalSemLayout)
        self.frameContainerDados.setObjectName(u"frameContainerDados")
        self.frameContainerDados.setFrameShape(QFrame.NoFrame)
        self.frameContainerDados.setFrameShadow(QFrame.Raised)
        self.verticalLayout_11 = QVBoxLayout(self.frameContainerDados)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.frameUmidade = QFrame(self.frameContainerDados)
        self.frameUmidade.setObjectName(u"frameUmidade")
        self.frameUmidade.setFrameShape(QFrame.NoFrame)
        self.frameUmidade.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.frameUmidade)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.frame_14 = QFrame(self.frameUmidade)
        self.frame_14.setObjectName(u"frame_14")
        self.frame_14.setFrameShape(QFrame.Panel)
        self.frame_14.setFrameShadow(QFrame.Sunken)
        self.frame_14.setLineWidth(2)
        self.verticalLayout_9 = QVBoxLayout(self.frame_14)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.label_10 = QLabel(self.frame_14)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setFont(font2)
        self.label_10.setAlignment(Qt.AlignCenter)

        self.verticalLayout_9.addWidget(self.label_10)


        self.horizontalLayout_7.addWidget(self.frame_14)

        self.frame_15 = QFrame(self.frameUmidade)
        self.frame_15.setObjectName(u"frame_15")
        self.frame_15.setFrameShape(QFrame.Panel)
        self.frame_15.setFrameShadow(QFrame.Sunken)
        self.frame_15.setLineWidth(2)
        self.verticalLayout_16 = QVBoxLayout(self.frame_15)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.dadoUmidade = QLCDNumber(self.frame_15)
        self.dadoUmidade.setObjectName(u"dadoUmidade")
        sizePolicy.setHeightForWidth(self.dadoUmidade.sizePolicy().hasHeightForWidth())
        self.dadoUmidade.setSizePolicy(sizePolicy)
        self.dadoUmidade.setFrameShape(QFrame.NoFrame)
        self.dadoUmidade.setSmallDecimalPoint(False)
        self.dadoUmidade.setDigitCount(10)
        self.dadoUmidade.setProperty("value", 0.000000000000000)

        self.verticalLayout_16.addWidget(self.dadoUmidade)


        self.horizontalLayout_7.addWidget(self.frame_15)

        self.frame_16 = QFrame(self.frameUmidade)
        self.frame_16.setObjectName(u"frame_16")
        self.frame_16.setFrameShape(QFrame.Panel)
        self.frame_16.setFrameShadow(QFrame.Sunken)
        self.frame_16.setLineWidth(2)
        self.verticalLayout_21 = QVBoxLayout(self.frame_16)
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")
        self.label_15 = QLabel(self.frame_16)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setAlignment(Qt.AlignCenter)

        self.verticalLayout_21.addWidget(self.label_15)


        self.horizontalLayout_7.addWidget(self.frame_16)


        self.verticalLayout_11.addWidget(self.frameUmidade)

        self.framePressao = QFrame(self.frameContainerDados)
        self.framePressao.setObjectName(u"framePressao")
        self.framePressao.setFrameShape(QFrame.NoFrame)
        self.framePressao.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.framePressao)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.frame_19 = QFrame(self.framePressao)
        self.frame_19.setObjectName(u"frame_19")
        self.frame_19.setFrameShape(QFrame.Panel)
        self.frame_19.setFrameShadow(QFrame.Sunken)
        self.frame_19.setLineWidth(2)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_19)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_11 = QLabel(self.frame_19)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setFont(font2)
        self.label_11.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_5.addWidget(self.label_11)


        self.horizontalLayout_3.addWidget(self.frame_19)

        self.frame_18 = QFrame(self.framePressao)
        self.frame_18.setObjectName(u"frame_18")
        self.frame_18.setFrameShape(QFrame.Panel)
        self.frame_18.setFrameShadow(QFrame.Sunken)
        self.frame_18.setLineWidth(2)
        self.verticalLayout_17 = QVBoxLayout(self.frame_18)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.dadoPressao = QLCDNumber(self.frame_18)
        self.dadoPressao.setObjectName(u"dadoPressao")
        sizePolicy.setHeightForWidth(self.dadoPressao.sizePolicy().hasHeightForWidth())
        self.dadoPressao.setSizePolicy(sizePolicy)
        self.dadoPressao.setFrameShape(QFrame.NoFrame)
        self.dadoPressao.setDigitCount(10)

        self.verticalLayout_17.addWidget(self.dadoPressao)


        self.horizontalLayout_3.addWidget(self.frame_18)

        self.frame_17 = QFrame(self.framePressao)
        self.frame_17.setObjectName(u"frame_17")
        self.frame_17.setFrameShape(QFrame.Panel)
        self.frame_17.setFrameShadow(QFrame.Sunken)
        self.frame_17.setLineWidth(2)
        self.verticalLayout_22 = QVBoxLayout(self.frame_17)
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.label_16 = QLabel(self.frame_17)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setAlignment(Qt.AlignCenter)

        self.verticalLayout_22.addWidget(self.label_16)


        self.horizontalLayout_3.addWidget(self.frame_17)


        self.verticalLayout_11.addWidget(self.framePressao)

        self.frameTempInterna = QFrame(self.frameContainerDados)
        self.frameTempInterna.setObjectName(u"frameTempInterna")
        self.frameTempInterna.setFrameShape(QFrame.NoFrame)
        self.frameTempInterna.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frameTempInterna)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.frame_22 = QFrame(self.frameTempInterna)
        self.frame_22.setObjectName(u"frame_22")
        self.frame_22.setFrameShape(QFrame.Panel)
        self.frame_22.setFrameShadow(QFrame.Sunken)
        self.frame_22.setLineWidth(2)
        self.frame_22.setMidLineWidth(0)
        self.verticalLayout_14 = QVBoxLayout(self.frame_22)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.label_12 = QLabel(self.frame_22)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setFont(font2)
        self.label_12.setAlignment(Qt.AlignCenter)

        self.verticalLayout_14.addWidget(self.label_12)


        self.horizontalLayout_2.addWidget(self.frame_22)

        self.frame_21 = QFrame(self.frameTempInterna)
        self.frame_21.setObjectName(u"frame_21")
        self.frame_21.setFrameShape(QFrame.Panel)
        self.frame_21.setFrameShadow(QFrame.Sunken)
        self.frame_21.setLineWidth(2)
        self.verticalLayout_18 = QVBoxLayout(self.frame_21)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.dadoTempInterna = QLCDNumber(self.frame_21)
        self.dadoTempInterna.setObjectName(u"dadoTempInterna")
        sizePolicy.setHeightForWidth(self.dadoTempInterna.sizePolicy().hasHeightForWidth())
        self.dadoTempInterna.setSizePolicy(sizePolicy)
        self.dadoTempInterna.setFrameShape(QFrame.NoFrame)
        self.dadoTempInterna.setDigitCount(10)

        self.verticalLayout_18.addWidget(self.dadoTempInterna)


        self.horizontalLayout_2.addWidget(self.frame_21)

        self.frame_20 = QFrame(self.frameTempInterna)
        self.frame_20.setObjectName(u"frame_20")
        self.frame_20.setFrameShape(QFrame.Panel)
        self.frame_20.setFrameShadow(QFrame.Sunken)
        self.frame_20.setLineWidth(2)
        self.verticalLayout_23 = QVBoxLayout(self.frame_20)
        self.verticalLayout_23.setObjectName(u"verticalLayout_23")
        self.label_17 = QLabel(self.frame_20)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setAlignment(Qt.AlignCenter)

        self.verticalLayout_23.addWidget(self.label_17)


        self.horizontalLayout_2.addWidget(self.frame_20)


        self.verticalLayout_11.addWidget(self.frameTempInterna)

        self.frameTempExterna = QFrame(self.frameContainerDados)
        self.frameTempExterna.setObjectName(u"frameTempExterna")
        self.frameTempExterna.setFrameShape(QFrame.NoFrame)
        self.frameTempExterna.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frameTempExterna)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.frame_25 = QFrame(self.frameTempExterna)
        self.frame_25.setObjectName(u"frame_25")
        self.frame_25.setFrameShape(QFrame.Panel)
        self.frame_25.setFrameShadow(QFrame.Sunken)
        self.frame_25.setLineWidth(2)
        self.verticalLayout_13 = QVBoxLayout(self.frame_25)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.label_13 = QLabel(self.frame_25)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setFont(font2)
        self.label_13.setAlignment(Qt.AlignCenter)

        self.verticalLayout_13.addWidget(self.label_13)


        self.horizontalLayout.addWidget(self.frame_25)

        self.frame_24 = QFrame(self.frameTempExterna)
        self.frame_24.setObjectName(u"frame_24")
        self.frame_24.setFrameShape(QFrame.Panel)
        self.frame_24.setFrameShadow(QFrame.Sunken)
        self.frame_24.setLineWidth(2)
        self.verticalLayout_19 = QVBoxLayout(self.frame_24)
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.dadoTempExterna = QLCDNumber(self.frame_24)
        self.dadoTempExterna.setObjectName(u"dadoTempExterna")
        sizePolicy.setHeightForWidth(self.dadoTempExterna.sizePolicy().hasHeightForWidth())
        self.dadoTempExterna.setSizePolicy(sizePolicy)
        self.dadoTempExterna.setFrameShape(QFrame.NoFrame)
        self.dadoTempExterna.setDigitCount(10)

        self.verticalLayout_19.addWidget(self.dadoTempExterna)


        self.horizontalLayout.addWidget(self.frame_24)

        self.frame_23 = QFrame(self.frameTempExterna)
        self.frame_23.setObjectName(u"frame_23")
        self.frame_23.setFrameShape(QFrame.Panel)
        self.frame_23.setFrameShadow(QFrame.Sunken)
        self.frame_23.setLineWidth(2)
        self.verticalLayout_24 = QVBoxLayout(self.frame_23)
        self.verticalLayout_24.setObjectName(u"verticalLayout_24")
        self.label_18 = QLabel(self.frame_23)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setAlignment(Qt.AlignCenter)

        self.verticalLayout_24.addWidget(self.label_18)


        self.horizontalLayout.addWidget(self.frame_23)


        self.verticalLayout_11.addWidget(self.frameTempExterna)


        self.verticalLayout_57.addWidget(self.frameContainerDados)

        self.frameInformativos = QFrame(self.frameContainerPrincipalSemLayout)
        self.frameInformativos.setObjectName(u"frameInformativos")
        self.frameInformativos.setFrameShape(QFrame.NoFrame)
        self.frameInformativos.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frameInformativos)
        self.gridLayout.setObjectName(u"gridLayout")
        self.frameDataHora = QFrame(self.frameInformativos)
        self.frameDataHora.setObjectName(u"frameDataHora")
        self.frameDataHora.setFrameShape(QFrame.Panel)
        self.frameDataHora.setFrameShadow(QFrame.Sunken)
        self.frameDataHora.setLineWidth(2)
        self.verticalLayout_28 = QVBoxLayout(self.frameDataHora)
        self.verticalLayout_28.setObjectName(u"verticalLayout_28")
        self.tituloDataHora = QLabel(self.frameDataHora)
        self.tituloDataHora.setObjectName(u"tituloDataHora")

        self.verticalLayout_28.addWidget(self.tituloDataHora)


        self.gridLayout.addWidget(self.frameDataHora, 0, 0, 1, 1)

        self.frameDataHoraCorrente = QFrame(self.frameInformativos)
        self.frameDataHoraCorrente.setObjectName(u"frameDataHoraCorrente")
        self.frameDataHoraCorrente.setFrameShape(QFrame.Panel)
        self.frameDataHoraCorrente.setFrameShadow(QFrame.Sunken)
        self.frameDataHoraCorrente.setLineWidth(2)
        self.verticalLayout_26 = QVBoxLayout(self.frameDataHoraCorrente)
        self.verticalLayout_26.setObjectName(u"verticalLayout_26")
        self.dadosHoraData = QLabel(self.frameDataHoraCorrente)
        self.dadosHoraData.setObjectName(u"dadosHoraData")
        self.dadosHoraData.setAlignment(Qt.AlignCenter)

        self.verticalLayout_26.addWidget(self.dadosHoraData)


        self.gridLayout.addWidget(self.frameDataHoraCorrente, 0, 1, 1, 1)

        self.frameNRegistros = QFrame(self.frameInformativos)
        self.frameNRegistros.setObjectName(u"frameNRegistros")
        self.frameNRegistros.setFrameShape(QFrame.Panel)
        self.frameNRegistros.setFrameShadow(QFrame.Sunken)
        self.frameNRegistros.setLineWidth(2)
        self.verticalLayout_15 = QVBoxLayout(self.frameNRegistros)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.tituloNRegistrosRestante = QLabel(self.frameNRegistros)
        self.tituloNRegistrosRestante.setObjectName(u"tituloNRegistrosRestante")

        self.verticalLayout_15.addWidget(self.tituloNRegistrosRestante)


        self.gridLayout.addWidget(self.frameNRegistros, 1, 0, 1, 1)

        self.frameContadorRestante = QFrame(self.frameInformativos)
        self.frameContadorRestante.setObjectName(u"frameContadorRestante")
        self.frameContadorRestante.setFrameShape(QFrame.Panel)
        self.frameContadorRestante.setFrameShadow(QFrame.Sunken)
        self.frameContadorRestante.setLineWidth(2)
        self.horizontalLayout_4 = QHBoxLayout(self.frameContadorRestante)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.visorTempoRestante = QLCDNumber(self.frameContadorRestante)
        self.visorTempoRestante.setObjectName(u"visorTempoRestante")
        sizePolicy.setHeightForWidth(self.visorTempoRestante.sizePolicy().hasHeightForWidth())
        self.visorTempoRestante.setSizePolicy(sizePolicy)
        self.visorTempoRestante.setStyleSheet(u"color: rgb(246, 245, 244);")
        self.visorTempoRestante.setFrameShape(QFrame.NoFrame)
        self.visorTempoRestante.setDigitCount(5)

        self.horizontalLayout_4.addWidget(self.visorTempoRestante)

        self.label_19 = QLabel(self.frameContadorRestante)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setFont(font2)
        self.label_19.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_4.addWidget(self.label_19)

        self.tempoDefinido = QLCDNumber(self.frameContadorRestante)
        self.tempoDefinido.setObjectName(u"tempoDefinido")
        sizePolicy.setHeightForWidth(self.tempoDefinido.sizePolicy().hasHeightForWidth())
        self.tempoDefinido.setSizePolicy(sizePolicy)
        self.tempoDefinido.setStyleSheet(u"color: rgb(246, 245, 244);")
        self.tempoDefinido.setFrameShape(QFrame.NoFrame)

        self.horizontalLayout_4.addWidget(self.tempoDefinido)


        self.gridLayout.addWidget(self.frameContadorRestante, 1, 1, 1, 1)


        self.verticalLayout_57.addWidget(self.frameInformativos)


        self.verticalLayout_2.addWidget(self.frameContainerPrincipalSemLayout)

        self.tabWidget.addTab(self.mostrarDadosTReal, "")
        self.emailUser = QWidget()
        self.emailUser.setObjectName(u"emailUser")
        self.verticalLayout_6 = QVBoxLayout(self.emailUser)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.frameContainerPrincipal_2 = QFrame(self.emailUser)
        self.frameContainerPrincipal_2.setObjectName(u"frameContainerPrincipal_2")
        self.frameContainerPrincipal_2.setFrameShape(QFrame.StyledPanel)
        self.frameContainerPrincipal_2.setFrameShadow(QFrame.Raised)
        self.verticalLayout_58 = QVBoxLayout(self.frameContainerPrincipal_2)
        self.verticalLayout_58.setObjectName(u"verticalLayout_58")
        self.frameCabecalho = QFrame(self.frameContainerPrincipal_2)
        self.frameCabecalho.setObjectName(u"frameCabecalho")
        self.frameCabecalho.setFrameShape(QFrame.Panel)
        self.frameCabecalho.setFrameShadow(QFrame.Sunken)
        self.frameCabecalho.setLineWidth(2)
        self.verticalLayout_7 = QVBoxLayout(self.frameCabecalho)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.tituloCabecalho_3 = QLabel(self.frameCabecalho)
        self.tituloCabecalho_3.setObjectName(u"tituloCabecalho_3")
        self.tituloCabecalho_3.setMaximumSize(QSize(16777215, 30))
        self.tituloCabecalho_3.setFont(font)
        self.tituloCabecalho_3.setFrameShape(QFrame.NoFrame)
        self.tituloCabecalho_3.setFrameShadow(QFrame.Plain)
        self.tituloCabecalho_3.setLineWidth(1)
        self.tituloCabecalho_3.setAlignment(Qt.AlignCenter)
        self.tituloCabecalho_3.setIndent(0)

        self.verticalLayout_7.addWidget(self.tituloCabecalho_3)


        self.verticalLayout_58.addWidget(self.frameCabecalho)

        self.frameContainerEmailRemetente = QFrame(self.frameContainerPrincipal_2)
        self.frameContainerEmailRemetente.setObjectName(u"frameContainerEmailRemetente")
        self.frameContainerEmailRemetente.setFrameShape(QFrame.NoFrame)
        self.frameContainerEmailRemetente.setFrameShadow(QFrame.Plain)
        self.gridLayout_3 = QGridLayout(self.frameContainerEmailRemetente)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.tituloSenha = QLabel(self.frameContainerEmailRemetente)
        self.tituloSenha.setObjectName(u"tituloSenha")

        self.gridLayout_3.addWidget(self.tituloSenha, 2, 0, 1, 2)

        self.titiloEmailRemetente = QLabel(self.frameContainerEmailRemetente)
        self.titiloEmailRemetente.setObjectName(u"titiloEmailRemetente")

        self.gridLayout_3.addWidget(self.titiloEmailRemetente, 0, 0, 1, 2)

        self.statusRemetenteSenha = QLabel(self.frameContainerEmailRemetente)
        self.statusRemetenteSenha.setObjectName(u"statusRemetenteSenha")
        self.statusRemetenteSenha.setFrameShape(QFrame.Panel)
        self.statusRemetenteSenha.setFrameShadow(QFrame.Sunken)
        self.statusRemetenteSenha.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.statusRemetenteSenha, 5, 0, 1, 2)

        self.emailUsuario = QLineEdit(self.frameContainerEmailRemetente)
        self.emailUsuario.setObjectName(u"emailUsuario")
        sizePolicy.setHeightForWidth(self.emailUsuario.sizePolicy().hasHeightForWidth())
        self.emailUsuario.setSizePolicy(sizePolicy)

        self.gridLayout_3.addWidget(self.emailUsuario, 1, 0, 1, 2)

        self.senhaUsuario = QLineEdit(self.frameContainerEmailRemetente)
        self.senhaUsuario.setObjectName(u"senhaUsuario")
        sizePolicy.setHeightForWidth(self.senhaUsuario.sizePolicy().hasHeightForWidth())
        self.senhaUsuario.setSizePolicy(sizePolicy)
        self.senhaUsuario.setEchoMode(QLineEdit.Password)

        self.gridLayout_3.addWidget(self.senhaUsuario, 3, 0, 1, 2)

        self.btnSalvarUsuarioSenha = QPushButton(self.frameContainerEmailRemetente)
        self.btnSalvarUsuarioSenha.setObjectName(u"btnSalvarUsuarioSenha")
        sizePolicy.setHeightForWidth(self.btnSalvarUsuarioSenha.sizePolicy().hasHeightForWidth())
        self.btnSalvarUsuarioSenha.setSizePolicy(sizePolicy)

        self.gridLayout_3.addWidget(self.btnSalvarUsuarioSenha, 4, 0, 1, 1)

        self.btnTesteConexao = QPushButton(self.frameContainerEmailRemetente)
        self.btnTesteConexao.setObjectName(u"btnTesteConexao")
        sizePolicy.setHeightForWidth(self.btnTesteConexao.sizePolicy().hasHeightForWidth())
        self.btnTesteConexao.setSizePolicy(sizePolicy)

        self.gridLayout_3.addWidget(self.btnTesteConexao, 4, 1, 1, 1)


        self.verticalLayout_58.addWidget(self.frameContainerEmailRemetente)

        self.frameContainerDestinatarios = QFrame(self.frameContainerPrincipal_2)
        self.frameContainerDestinatarios.setObjectName(u"frameContainerDestinatarios")
        self.frameContainerDestinatarios.setFrameShape(QFrame.NoFrame)
        self.frameContainerDestinatarios.setFrameShadow(QFrame.Raised)
        self.verticalLayout_20 = QVBoxLayout(self.frameContainerDestinatarios)
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.label_24 = QLabel(self.frameContainerDestinatarios)
        self.label_24.setObjectName(u"label_24")

        self.verticalLayout_20.addWidget(self.label_24)

        self.adicionarDestinatario = QLineEdit(self.frameContainerDestinatarios)
        self.adicionarDestinatario.setObjectName(u"adicionarDestinatario")
        sizePolicy.setHeightForWidth(self.adicionarDestinatario.sizePolicy().hasHeightForWidth())
        self.adicionarDestinatario.setSizePolicy(sizePolicy)

        self.verticalLayout_20.addWidget(self.adicionarDestinatario)

        self.btnAdicionarDestinatario = QPushButton(self.frameContainerDestinatarios)
        self.btnAdicionarDestinatario.setObjectName(u"btnAdicionarDestinatario")
        sizePolicy.setHeightForWidth(self.btnAdicionarDestinatario.sizePolicy().hasHeightForWidth())
        self.btnAdicionarDestinatario.setSizePolicy(sizePolicy)

        self.verticalLayout_20.addWidget(self.btnAdicionarDestinatario)


        self.verticalLayout_58.addWidget(self.frameContainerDestinatarios)

        self.frameTabela = QFrame(self.frameContainerPrincipal_2)
        self.frameTabela.setObjectName(u"frameTabela")
        self.frameTabela.setFrameShape(QFrame.NoFrame)
        self.frameTabela.setFrameShadow(QFrame.Raised)
        self.verticalLayout_12 = QVBoxLayout(self.frameTabela)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.tabelaDestinatarios = QTableWidget(self.frameTabela)
        if (self.tabelaDestinatarios.columnCount() < 1):
            self.tabelaDestinatarios.setColumnCount(1)
        __qtablewidgetitem = QTableWidgetItem()
        self.tabelaDestinatarios.setHorizontalHeaderItem(0, __qtablewidgetitem)
        self.tabelaDestinatarios.setObjectName(u"tabelaDestinatarios")
        sizePolicy.setHeightForWidth(self.tabelaDestinatarios.sizePolicy().hasHeightForWidth())
        self.tabelaDestinatarios.setSizePolicy(sizePolicy)
        self.tabelaDestinatarios.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.tabelaDestinatarios.setGridStyle(Qt.SolidLine)
        self.tabelaDestinatarios.horizontalHeader().setProperty("showSortIndicator", False)
        self.tabelaDestinatarios.horizontalHeader().setStretchLastSection(True)
        self.tabelaDestinatarios.verticalHeader().setVisible(False)

        self.verticalLayout_12.addWidget(self.tabelaDestinatarios)

        self.btnExcluirDestinatario = QPushButton(self.frameTabela)
        self.btnExcluirDestinatario.setObjectName(u"btnExcluirDestinatario")
        sizePolicy.setHeightForWidth(self.btnExcluirDestinatario.sizePolicy().hasHeightForWidth())
        self.btnExcluirDestinatario.setSizePolicy(sizePolicy)

        self.verticalLayout_12.addWidget(self.btnExcluirDestinatario)


        self.verticalLayout_58.addWidget(self.frameTabela)

        self.statusOperacoes = QLabel(self.frameContainerPrincipal_2)
        self.statusOperacoes.setObjectName(u"statusOperacoes")
        self.statusOperacoes.setFrameShape(QFrame.Panel)
        self.statusOperacoes.setFrameShadow(QFrame.Sunken)
        self.statusOperacoes.setAlignment(Qt.AlignCenter)

        self.verticalLayout_58.addWidget(self.statusOperacoes)


        self.verticalLayout_6.addWidget(self.frameContainerPrincipal_2)

        self.tabWidget.addTab(self.emailUser, "")

        self.verticalLayout_4.addWidget(self.tabWidget)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Esta\u00e7\u00e3o Metereologica \u00a9BrainStorm Tecnologia", None))
#if QT_CONFIG(statustip)
        MainWindow.setStatusTip(QCoreApplication.translate("MainWindow", u"Esta\u00e7\u00e3o", None))
#endif // QT_CONFIG(statustip)
        self.TituloCabecalho.setText(QCoreApplication.translate("MainWindow", u"Esta\u00e7\u00e3o Metereologica \u00a9BrainStorm Tecnologia", None))
        self.primeiraParteTexto.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\">Esta\u00e7\u00e3o Metereologica que registra a umidade </p><p align=\"center\">relativa do ar, press\u00e3o atmosf\u00e9rica e 2 temperaturas,</p><p align=\"center\">uma interna e outra externa.</p><p align=\"center\">Usando uma plataforma de desenvolvimento baseada</p><p align=\"center\">em Ardu\u00edno, um sensor BME280 e outro </p><p align=\"center\">termistor 10k.</p></body></html>", None))
        self.segundaParteTexto.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:14pt;\">Grava os dados em um arquivo CSV a cada</span></p><p align=\"center\"><span style=\" font-size:14pt;\">segundo e ap\u00f3s um tempo determinado pelo</span></p><p align=\"center\"><span style=\" font-size:14pt;\">operador, envia um email contendo uma </span></p><p align=\"center\"><span style=\" font-size:14pt;\">an\u00e1lise dos dados e gr\u00e1ficos.</span></p></body></html>", None))
        self.rodaPe.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\">Desenvolvido com Python e C++</p><p align=\"center\"><img src=\":/icons/imagens/pic.png\"/></p><p align=\"center\"><span style=\" font-family:'Droid Sans Mono','monospace','monospace'; font-size:16px; color:#fcfcfa;\">\u00a9</span>BrainStorm Tecnologia</p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.paginaApresentacao), QCoreApplication.translate("MainWindow", u"Home", None))
        self.tituloCabecalho.setText(QCoreApplication.translate("MainWindow", u"Esta\u00e7\u00e3o Metereologica \u00a9BrainStorm Tecnologia", None))
        self.tituloPortaUSB.setText(QCoreApplication.translate("MainWindow", u"Porta USB:", None))
        self.portaArduino.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Porta Ardu\u00edno", None))
        self.tituloTempGrafico.setText(QCoreApplication.translate("MainWindow", u"Gr\u00e1ficos(M\u00c1X 06:00Hs)", None))
        self.tempoGraficos.setSpecialValueText("")
        self.btnInciarEstacao.setText(QCoreApplication.translate("MainWindow", u"Iniciar Esta\u00e7\u00e3o", None))
        self.btnPararEstacao.setText(QCoreApplication.translate("MainWindow", u"Parar Esta\u00e7\u00e3o", None))
        self.barraSeparadora.setText(QCoreApplication.translate("MainWindow", u"/", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.inicioEstacao), QCoreApplication.translate("MainWindow", u"Iniciar Esta\u00e7\u00e3o", None))
        self.tituloCabecalho_2.setText(QCoreApplication.translate("MainWindow", u"Dados Coletados Tempo Real", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Umidade", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"%", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Press\u00e3o", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"hPa", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Temp. Interna", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"\u00b0C", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"Temp. Externa", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"\u00b0C", None))
        self.tituloDataHora.setText(QCoreApplication.translate("MainWindow", u"Data/Hora da Coleta", None))
        self.dadosHoraData.setText("")
        self.tituloNRegistrosRestante.setText(QCoreApplication.translate("MainWindow", u"N\u00ba De Registros Restantes", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"/", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.mostrarDadosTReal), QCoreApplication.translate("MainWindow", u"Exibir Dados", None))
        self.tituloCabecalho_3.setText(QCoreApplication.translate("MainWindow", u"Configura\u00e7\u00e3o Para Envio Dos E-mails", None))
        self.tituloSenha.setText(QCoreApplication.translate("MainWindow", u"Senha", None))
        self.titiloEmailRemetente.setText(QCoreApplication.translate("MainWindow", u"E-mail Remetente", None))
        self.statusRemetenteSenha.setText("")
        self.emailUsuario.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Digite Seu E-mail (Somente Gmail)", None))
        self.senhaUsuario.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Digite a Senha do E-mail", None))
        self.btnSalvarUsuarioSenha.setText(QCoreApplication.translate("MainWindow", u"Salvar", None))
        self.btnTesteConexao.setText(QCoreApplication.translate("MainWindow", u"Testar Conex\u00e3o", None))
        self.label_24.setText(QCoreApplication.translate("MainWindow", u"Destinat\u00e1rios", None))
        self.adicionarDestinatario.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Adicione os Destinat\u00e1rios Aqui", None))
        self.btnAdicionarDestinatario.setText(QCoreApplication.translate("MainWindow", u"Adicionar", None))
        ___qtablewidgetitem = self.tabelaDestinatarios.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"E-mail Destinat\u00e1rio", None));
        self.btnExcluirDestinatario.setText(QCoreApplication.translate("MainWindow", u"Excluir", None))
        self.statusOperacoes.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.emailUser), QCoreApplication.translate("MainWindow", u"Definir config. E-mail", None))
    # retranslateUi

