from serial import Serial
from Interface.mainInterface import Ui_MainWindow
from DataGetter.DataGetter import WorkerEstacao, ConexaoUSB
from GlobalFunctions.UserEmailHandler import ManipuladorDadosEmailRemetDest
from GlobalFunctions.UserEmailHandler import ManipuladorEmailDestinatario
from GlobalFunctions.UserEmailHandler import DBInterfaceConfig
from EMailManager.EmailManager import WorkerEmailTesteConexao, WorkerGraphEmail
from PySide2.QtCore import QThread
from PySide2.QtGui import QStandardItemModel, QStandardItem
from PySide2.QtWidgets import QMainWindow, QTableWidgetItem


class EntradaError(Exception):
    ...


class TransSegundos:
    def __init__(self, horas) -> None:
        self.horas = horas

    def conversorHorasSegundo(self) -> int:
        horas = self.horas[:2]
        minutos = self.horas[3:]
        segundos = int(int(horas) * 3600 + int(minutos) * 60)
        return segundos


class InterfaceEstacao(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        super().setupUi(self)
        self.btnInciarEstacao.clicked.connect(self.executarMainEstacao)
        self.btnPararEstacao.clicked.connect(self.pararWorker)
        self.btnSalvarUsuarioSenha.clicked.connect(
            self.adicionarEmailRemetenteSenha
        )
        self.btnAdicionarDestinatario.clicked.connect(
            self.adicionarEmailDestinatarios
        )
        self.btnExcluirDestinatario.clicked.connect(
            self.deletarEmailDestinatario
        )
        self.btnTesteConexao.clicked.connect(
            self.executarEmailTeste
        )
        self.btnCadastrarBD.clicked.connect(
            self.cadastrarBD
        )
        self.btnDeletarBD.clicked.connect(
            self.deletarBDCadastrado
        )
        self.btnPararEstacao.setEnabled(False)
        self.modeloInfo = QStandardItemModel()
        self.saidaDetalhes.setModel(self.modeloInfo)
        try:
            baseDados = 'Sqlite3.db'
            self.bd = DBInterfaceConfig(baseDados)
            self.bd.createTableDataBase()
            self.bd.createTableEmailRemetente()
            self.bd.createTableEmailDestinatario()
            self.bdRemet = ManipuladorDadosEmailRemetDest(self.bd)
            self.bdDest = ManipuladorEmailDestinatario(self.bd)
            self.selecionarBDDelete.activated.connect(self.selecionarBDDeletar)
            self.escolherBD.activated.connect(self.iniciarBD)
            self.setarComboBox(self.escolherBD)
            self.setarComboBox(self.selecionarBDDelete)
            self.manipuladorRemetenteSenha()
            self.manipuladorDestinatarios()
            self.bdDelete = None
            self.bdEscolha = None
        except Exception as e:
            raise e

    def mostrardorDisplayBarraProgresso(self, percent) -> None:
        self.barraProgresso.setValue(percent)

    def mostradorDisplayInfo(self, info) -> None:
        self.modeloInfo.appendRow(QStandardItem(info))

    def mostradorDisplayLCDTempoRestante(self, valor) -> None:
        self.visorTempoRestante.display(valor)
        self.visorTempoRestante_2.display(valor)

    def mostradorDisplayLCDTempoDefinido(self, valor) -> None:
        self.tempoDefinido.display(valor)
        self.tempoDefinido_2.display(valor)

    def mostradorDisplayLCDDados(self, dados: list) -> None:
        self.dadoUmidade.display(dados[0])
        self.dadoPressao.display(dados[1])
        self.dadoTempInterna.display(dados[2])
        self.dadoTempExterna.display(dados[3])

    def mostradorLabelDataHora(self, dt_hr) -> None:
        self.dadosHoraData.setText(dt_hr)

    def retornarBotoesInicio(self) -> None:
        self.btnInciarEstacao.setEnabled(True)
        self.btnPararEstacao.setEnabled(False)
        self.escolherBD.setEnabled(True)
        self.portaArduino.setEnabled(True)
        self.tempoGraficos.setEnabled(True)

    def executarMainEstacao(self) -> None:
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
            self.estacaoWorker = WorkerEstacao(
                portaArduino=pA, tempGraf=self.receptorTempoGraficos
            )
            self.estacaoWorker.moveToThread(self.estacaoThread)
            self.estacaoWorker.finalizar.connect(
                self.estacaoThread.quit
            )
            self.estacaoWorker.finalizar.connect(
                self.estacaoWorker.deleteLater
            )
            self.estacaoWorker.finalizar.connect(
                self.estacaoThread.deleteLater
            )
            self.estacaoWorker.finalizar.connect(
                portaArduino.desconectarPortaUSB
            )
            self.estacaoThread.started.connect(self.estacaoWorker.run)
            self.estacaoThread.start()
            self.estacaoWorker.barraProgresso.connect(
                self.mostrardorDisplayBarraProgresso
            )
            self.estacaoWorker.saidaInfoInicio.connect(
                self.mostradorDisplayInfo
            )
            self.estacaoWorker.saidaDadosLCD.connect(
                self.mostradorDisplayLCDDados
            )
            self.estacaoWorker.saidaData.connect(self.mostradorLabelDataHora)
            self.estacaoWorker.saidaDadosEmail.connect(self.executarEmail)
            self.estacaoWorker.mostradorTempoRestante.connect(
                self.mostradorDisplayLCDTempoRestante
            )
            self.estacaoThread.finished.connect(
                lambda: self.btnInciarEstacao.setEnabled(True)
            )
            self.portaArduino.setEnabled(False)
            self.tempoGraficos.setEnabled(False)
        except Exception as e:
            self.mostradorDisplayInfo(f'{e.__class__.__name__}: {e}')
            self.retornarBotoesInicio()
            return

    def pararWorker(self) -> None:
        self.estacaoWorker.parar()
        self.estacaoThread.quit()
        self.estacaoThread.wait()
        self.btnPararEstacao.setEnabled(False)
        self.portaArduino.setEnabled(True)
        self.tempoGraficos.setEnabled(True)

    def executarEmail(
        self,
        inicioParcial,
        terminoParcial,
        yDadosUmidade,
        yDadosPressao,
        yDadosTempInt,
        yDadosTempExt
    ) -> None:
        try:
            self.emailThread = QThread(parent=None)
            self.emailWorker = WorkerGraphEmail(
                inicioParcial,
                terminoParcial,
                yDadosUmidade,
                yDadosPressao,
                yDadosTempInt,
                yDadosTempExt
            )
            self.emailWorker.moveToThread(self.emailThread)
            self.emailThread.started.connect(self.emailWorker.run)
            self.emailWorker.termino.connect(self.emailThread.quit)
            self.emailWorker.termino.connect(self.emailThread.wait)
            self.emailWorker.termino.connect(self.emailThread.deleteLater)
            self.emailWorker.termino.connect(self.emailWorker.deleteLater)
            self.emailWorker.confirma.connect(self.mostradorDisplayInfo)
            self.emailWorker.erro.connect(self.mostradorDisplayInfo)
            self.emailThread.start()
        except Exception as e:
            self.mostradorDisplayInfo(f'{e.__class__.__name__}: {e}')
            return

    def defineArquivoEmail(self, dadoUsuario: str) -> None:
        with open('.EMAIL_USER_DATA.txt', 'w') as file:
            file.write(dadoUsuario)

    def defineArquivoSenha(self, dadoUsuario: str) -> None:
        with open('.PASSWORD_USER_DATA.txt', 'w') as file:
            file.write(dadoUsuario)

    def defineArquivoDestinatarios(self, dadoUsuario: str) -> None:
        with open('.RECIPIENTS_USER_DATA.txt', 'a') as file:
            file.write(f'{dadoUsuario}\n')

    def apagadorArquivo(self, caminhoArquivo: str) -> None:
        with open(caminhoArquivo, 'w') as file:
            file.write('')

    def manipuladorRemetenteSenha(self) -> None:
        try:
            if len(meu_email()) == 1 and len(minha_senha()) == 1:
                email = ''.join(meu_email())
                senha = ''.join(minha_senha())
                senhaOculta = "".join(
                    [caractere.replace(caractere, "*") for caractere in senha]
                )
                self.statusRemetenteSenha.setText(
                    f'Dados Atuais: Email: {email} | '
                    f'Senha: {senhaOculta}'
                )
            else:
                self.statusRemetenteSenha.setText('Os dados de e-mail e/ou a \
                    senha do remetente não estão definidos')
        except Exception as e:
            self.statusOperacoes.setText(f'{e.__class__.__name__}: {e}')

    def adicionarEmailRemetenteSenha(self) -> None:
        try:
            self.statusOperacoes.setText('')
            emailRemetente = self.emailUsuario.text()
            senhaRemetente = self.senhaUsuario.text()
            if emailRemetente == '' or senhaRemetente == '':
                self.statusOperacoes.setText('Entre com o e-mail e senha ! ')
                return None
            else:
                self.adicionarEmailRemetente(emailRemetente)
                self.adicionarSenhaRemetente(senhaRemetente)
                self.emailUsuario.clear()
                self.senhaUsuario.clear()
                self.manipuladorRemetenteSenha()
        except Exception as e:
            self.statusOperacoes.setText(f'{e.__class__.__name__}: {e}')

    def adicionarEmailRemetente(self, email: str) -> None:
        try:
            self.defineArquivoEmail(email)
        except Exception as e:
            self.statusOperacoes.setText(f'{e.__class__.__name__}: {e}')

    def adicionarSenhaRemetente(self, senha: str) -> None:
        try:
            self.defineArquivoSenha(senha)
        except Exception as e:
            self.statusOperacoes.setText(f'{e.__class__.__name__}: {e}')

    def manipuladorDestinatarios(self) -> None:
        try:
            emailDestinatarios = my_recipients()
            self.tabelaDestinatarios.setRowCount(len(emailDestinatarios))
            for linha, email in enumerate(emailDestinatarios):
                self.tabelaDestinatarios.setItem(
                    linha, 0, QTableWidgetItem(email)
                )
        except Exception:
            self.statusOperacoes.setText('Defina as configurações de e-mail.')

    def obterEmailDestinatario(self) -> str:
        try:
            emailSelecionado: str = self.tabelaDestinatarios.currentItem().text().strip()
            return emailSelecionado
        except Exception:
            return ''

    def deletarEmailDestinatario(self) -> None:
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
                    self.statusOperacoes.setText(
                        'Selecione um email na tabela.'
                    )
        except Exception as e:
            self.statusOperacoes.setText(f'{e.__class__.__name__}: {e}')

    def adicionarEmailDestinatarios(self) -> None:
        try:
            emailDestinatario: str = self.adicionarDestinatario.text().strip()
            if emailDestinatario:
                self.defineArquivoDestinatarios(emailDestinatario)
                self.statusOperacoes.setText(
                    f'{emailDestinatario}: Dado gravado com sucesso.'
                )
                self.manipuladorDestinatarios()
                self.adicionarDestinatario.clear()
            else:
                self.statusOperacoes.setText('Digite um e-mail')
        except Exception as e:
            self.statusOperacoes.setText(f'{e.__class__.__name__}: {e}')

    def executarEmailTeste(self) -> None:
        try:
            self.emailTesteThread = QThread(parent=None)
            self.emailTesteWorker = WorkerEmailTesteConexao()
            self.emailTesteWorker.moveToThread(self.emailTesteThread)
            self.emailTesteThread.started.connect(self.emailTesteWorker.run)
            self.emailTesteThread.start()
            self.emailTesteWorker.msgEnvio.connect(
                lambda msg: self.statusOperacoes.setText(msg)
            )
            self.emailTesteWorker.termino.connect(self.emailTesteThread.quit)
            self.emailTesteWorker.termino.connect(self.emailTesteThread.wait)
            self.emailTesteWorker.termino.connect(
                self.emailTesteThread.deleteLater
            )
            self.emailTesteWorker.termino.connect(
                self.emailTesteWorker.deleteLater
            )
        except Exception as e:
            self.statusOperacoes.setText(f'{e.__class__.__name__}: {e}')

    def cadastrarBD(self) -> None:
        try:
            bd = DBInterfaceConfig('Sqlite3.db')
            bd.createTableDataBase()
            nomeCadastro: str = self.nomeCadastroBD.text()
            db_name = self.db_name.text()
            user = self.user.text()
            host = self.host.text()
            port = self.port.text()
            password = self.password.text()
            if nomeCadastro != '' and db_name != '' and user != ''\
               and host != '' and port != '' and password != '':
                sql = '''INSERT INTO data_base
                (nome_cadastro, db_name, user, host, port, password)
                VALUES (?, ?, ?, ?, ?, ?)'''
                data: tuple = (
                    nomeCadastro, db_name, user, host, port, password
                )
                bd.executeSQL(sql, data)
                self.setarComboBox(self.escolherBD)
                self.setarComboBox(self.selecionarBDDelete)
                self.statusCadastroBD.setText(
                    'Banco cadastrado com sucesso !'
                )
            else:
                self.statusCadastroBD.setText(
                    'Verifique suas entradas !'
                )
        except Exception as e:
            self.mostradorDisplayInfo(f'{e.__class__.__name__}: {e}')
            return

    def setarComboBox(self, comboBox) -> None:
        try:
            bd = DBInterfaceConfig('Sqlite3.db')
            sql = 'SELECT nome_cadastro FROM data_base'
            bdCadastrados: list = bd.select(sql)
            comboBox.clear()
            for tupla in bdCadastrados:
                for b in tupla:
                    comboBox.addItem(b)
        except Exception as e:
            self.mostradorDisplayInfo(f'{e.__class__.__name__}: {e}')
            return

    def deletarBDCadastrado(self) -> None:
        if self.bdDelete is not None:
            bd = DBInterfaceConfig('Sqlite3.db')
            bd.delete('data_base', 'nome_cadastro', self.bdDelete)
            self.setarComboBox(self.escolherBD)
            self.setarComboBox(self.selecionarBDDelete)
            self.statusCadastroBD.setText(
                'Banco deletar com sucesso !'
            )
            self.bdDelete = None
        else:
            self.statusCadastroBD.setText(
                'Selecione um Banco de Dados !'
            )

    def selecionarBDDeletar(self) -> None:
        self.bdDelete = self.selecionarBDDelete.currentText()
