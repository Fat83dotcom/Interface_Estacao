import io
import matplotlib.backends.backend_pdf
from GlobalFunctions.funcoesGlobais import maximos, minimos, dataInstantanea
import matplotlib
matplotlib.use('QtAgg')
import matplotlib.pyplot as plt


class PlotterGraficoPDF:
    def __init__(self, dataInicio: str, dataTermino: str) -> None:
        self.dtInicio = dataInicio
        self.dtTermino = dataTermino
        self.tipoGrafico = {
            'umi': 'Umidade',
            'press': 'Pressao',
            'tempInt': 'Temperatura_Interna',
            'tempExt': 'Temperatura_Externa',
        }
        self.grandeza = {
            'temp': 'Temperatura em °C',
            'press': 'Pressão Atmosférica em hPa',
            'umi': 'Umidade Relativa do Ar %',
        }

    def plotadorPDF(
        self, dadosEixo_Y: list, tipoGrafico: str, grandezaEixo_Y: str
    ) -> None:
        """
            Argumentos que devem ser passados para cada situação:
            tipoGrafico -> 'umi', 'press', 'tempInt', 'tempExt'
            Grandezas -> 'temp', 'press', 'umi'
        """
        buffer = io.BytesIO()
        tituloGrafico1 = f'{self.tipoGrafico[tipoGrafico]}\n-> Inicio: {self.dtInicio} <-|-> Termino: {self.dtTermino} '
        tituloGrafico2 = f' <-\nMáxima: {maximos(dadosEixo_Y)} --- Mínima: {minimos(dadosEixo_Y)}'
        try:
            tempoEixo_X = range(len(dadosEixo_Y))
            plt.title(
                f'{tituloGrafico1}{tituloGrafico2}'
            )
            plt.xlabel('Tempo em segundos.')
            plt.ylabel(self.grandeza[grandezaEixo_Y])
            plt.plot(tempoEixo_X, dadosEixo_Y)
            plt.savefig(buffer, format='pdf')
            plt.clf()
            return buffer
        except (ValueError, Exception) as e:
            raise e
