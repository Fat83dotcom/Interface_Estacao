import smtplib
from io import BytesIO
from statistics import mean
from string import Template
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from PySide2.QtCore import QObject, Signal, Slot
from email.mime.application import MIMEApplication
from GraphManager.GraphManager import PlotterGraficoPDF
from GlobalFunctions.GlobalFunctions import dataInstantanea
from GlobalFunctions.GlobalFunctions import maximos, minimos
from GlobalFunctions.UserEmailHandler import ManipuladorDadosEmailRemetDest
from GlobalFunctions.UserEmailHandler import ManipuladorEmailDestinatario
from Interface.InterfaceManager import DBInterfaceConfig


class WorkerGraphEmail(QObject):
    erro = Signal(str)
    confirma = Signal(str)
    termino = Signal()

    def __init__(
        self,
        inicioParcial: str,
        terminoParcial: str,
        yDadosUmidade: list,
        yDadosPressao: list,
        yDadosTempInt: list,
        yDadosTempExt: list,
        parent=None,
    ) -> None:
        super().__init__(parent)
        self.inicioParcial = inicioParcial
        self.terminoParcial = terminoParcial
        self.yDadosUmidade = yDadosUmidade
        self.yDadosPressao = yDadosPressao
        self.yDadosTempInt = yDadosTempInt
        self.yDadosTempExt = yDadosTempExt
        self.email = WorkerEmail(self.terminoParcial)
        self.plotGrafico = PlotterGraficoPDF(
            self.inicioParcial, self.terminoParcial
        )

    @Slot()
    def run(self) -> None:
        try:
            pdfDadosUmidade = self.plotGrafico.plotadorPDF(
                self.yDadosUmidade, 'umi', 'umi'
            )
            pdfDadosPressao = self.plotGrafico.plotadorPDF(
                self.yDadosPressao, 'press', 'press'
            )
            pdfDadosTemperaturaInterna = self.plotGrafico.plotadorPDF(
                self.yDadosTempInt, 'tempInt', 'temp'
            )
            pdfDadosTemperaturaExterna = self.plotGrafico.plotadorPDF(
                self.yDadosTempExt, 'tempExt', 'temp'
            )

            self.email.run(
                self.inicioParcial,
                round(mean(self.yDadosUmidade), 2),
                round(mean(self.yDadosPressao), 2),
                round(mean(self.yDadosTempInt), 2),
                round(mean(self.yDadosTempExt), 2),
                maximos(self.yDadosTempInt),
                minimos(self.yDadosTempInt),
                maximos(self.yDadosTempExt),
                minimos(self.yDadosTempExt),
                maximos(self.yDadosUmidade),
                minimos(self.yDadosUmidade),
                maximos(self.yDadosPressao),
                minimos(self.yDadosPressao),
                self.terminoParcial,
                pdfDadosUmidade,
                pdfDadosPressao,
                pdfDadosTemperaturaInterna,
                pdfDadosTemperaturaExterna
            )
            self.confirma.emit('Email enviado com sucesso!')
        except Exception as e:
            self.erro.emit(f'Email não enviado: {e.__class__.__name__}')
        self.termino.emit()


class WorkerEmailTesteConexao(QObject):
    termino = Signal()
    msgEnvio = Signal(str)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.pathTest = 'Templates/emailTeste.html'

    def run(self) -> None:
        try:
            msgErro = 'Não foi possivel enviar o email. Motivo:'
            usuario = ''.join(meu_email())
            msg = MIMEMultipart()
            msg['from'] = usuario
            msg['to'] = usuario
            msg['subject'] = f'Teste de Conexão {dataInstantanea()}'
            with open(self.pathTest, 'r') as page:
                email = page.read()
                template = Template(email)
                htmlEmail = template.safe_substitute(usuario=usuario)
            corpo = MIMEText(htmlEmail, 'html')
            msg.attach(corpo)
            try:
                with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
                    smtp.ehlo()
                    smtp.starttls()
                    smtp.login(usuario, ''.join(minha_senha()))
                    smtp.send_message(msg)
                    self.msgEnvio.emit('Email enviado com sucesso.')
            except Exception as e:
                self.msgEnvio.emit(
                    f'{msgErro} {e.__class__.__name__}: {e}'
                )
                self.termino.emit()
        except Exception as e:
            self.msgEnvio.emit(
                f'{msgErro} {e.__class__.__name__}: {e}')
            self.termino.emit()
        self.termino.emit()


class WorkerEmail:
    def __init__(self, dataTermino: str) -> None:
        self.pathTemplateHtml = 'Templates/template.html'
        self.dtTermino = dataTermino

    def anexadorPdf(self, buffer: BytesIO, msg) -> MIMEApplication:
        anexo = MIMEApplication(buffer.getvalue(), _subtype='pdf')
        anexo.add_header('pdf', 'Conteudo')
        return anexo

    def renderizadorHtml(self, umidade, pressao, temp1, temp2, temp1max,
                         temp1min,
                         temp2max, temp2min, umima, umimi, pressma, pressmi,
                         inicio, fim, data
                         ) -> str:
        with open(self.pathTemplateHtml, 'r') as doc:
            template = Template(doc.read())
            corpo_msg = template.safe_substitute(
                umi=umidade, press=pressao, t1=temp1, t2=temp2,
                t1max=temp1max, t1min=temp1min, t2max=temp2max,
                t2min=temp2min, umimax=umima, umimini=umimi,
                pressmax=pressma, pressmini=pressmi, ini=inicio,
                fim=fim, dat=data
            )
        return corpo_msg

    def run(
        self,
        inicio, umi, press, t1, t2, t1max,
        t1min, t2max, t2min, umimax, umimini,
        pressmax, pressmini, fim,
        pdfDadosUmidade,
        pdfDadosPressao,
        pdfDadosTempInt,
        pdfDadostempExt,
    ) -> None:
        msgSubject = 'Monitor Estação Metereologica ©BrainStorm Tecnologia'
        try:
            msg = MIMEMultipart()
            msg['from'] = ''.join(meu_email())
            msg['to'] = ','.join(my_recipients())
            msg['subject'] = f'{msgSubject} {self.dtTermino}'
            corpo = MIMEText(
                self.renderizadorHtml(
                    umi, press, t1, t2,
                    t1max, t1min, t2max, t2min,
                    umimax, umimini, pressmax, pressmini,
                    inicio, fim, self.dtTermino
                ), 'html'
            )
            msg.attach(corpo)
            msg.attach(self.anexadorPdf(pdfDadosUmidade, msg))
            msg.attach(self.anexadorPdf(pdfDadosPressao, msg))
            msg.attach(self.anexadorPdf(pdfDadosTempInt, msg))
            msg.attach(self.anexadorPdf(pdfDadostempExt, msg))

            with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.login(''.join(meu_email()), ''.join(minha_senha()))
                smtp.send_message(msg)
        except Exception as e:
            raise e
