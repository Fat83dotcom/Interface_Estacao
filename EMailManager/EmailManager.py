import smtplib
from pathlib import Path
from string import Template
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from PySide2.QtCore import QObject, Signal, Slot
from email.mime.application import MIMEApplication
from GraphManager.GraphManager import PlotterGraficoPDF
from GlobalFunctions.funcoesGlobais import dataInstantanea
from GlobalFunctions.manipuladoresArquivos import my_recipients
from GlobalFunctions.manipuladoresArquivos import meu_email, minha_senha

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


class WorkerEmailTesteConexao(QObject):
    termino = Signal()
    msgEnvio = Signal(str)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.pathTest = BASE_DIR / 'Templates/emailTeste.html'

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


class WorkerEmail(QObject):
    termino = Signal()
    msgEnvio = Signal(str)

    def __init__(self, inicio, umi, press, t1, t2, t1max,
                 t1min, t2max, t2min, umimax, umimini,
                 pressmax, pressmini, fim, path, parent=None) -> None:
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
        self.pathTemplateHtml = BASE_DIR / 'Templates/template.html'
        self.servicosArquivosPDF = PlotterGraficoPDF(self.inicio, self.path)

    def anexadorPdf(self, enderecoPdf, msg) -> MIMEApplication:
        with open(enderecoPdf, 'rb') as pdf:
            anexo = MIMEApplication(pdf.read(), _subtype='pdf')
            anexo.add_header('Conteudo', enderecoPdf)
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

    @Slot()
    def run(self) -> None:
        msgSubject = 'Monitor Estação Metereologica ©BrainStorm Tecnologia'
        try:
            umidade = self.servicosArquivosPDF.geradorCaminhoArquivoPDF(
                'umi'
            )
            pressao = self.servicosArquivosPDF.geradorCaminhoArquivoPDF(
                'press'
            )
            tmp1 = self.servicosArquivosPDF.geradorCaminhoArquivoPDF(
                'tempInt'
            )
            temp2 = self.servicosArquivosPDF.geradorCaminhoArquivoPDF(
                'tempExt'
            )
            msg = MIMEMultipart()
            msg['from'] = ''.join(meu_email())
            msg['to'] = ','.join(my_recipients())
            msg['subject'] = f'{msgSubject} {dataInstantanea()}'
            corpo = MIMEText(
                self.renderizadorHtml(
                    self.umi, self.press, self.t1, self.t2,
                    self.t1max, self.t1min, self.t2max, self.t2min,
                    self.umimax, self.umimini, self.pressmax, self.pressmini,
                    self.inicio, self.fim, dataInstantanea()
                ), 'html'
            )
            msg.attach(corpo)
            msg.attach(self.anexadorPdf(umidade, msg))
            msg.attach(self.anexadorPdf(pressao, msg))
            msg.attach(self.anexadorPdf(tmp1, msg))
            msg.attach(self.anexadorPdf(temp2, msg))

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
