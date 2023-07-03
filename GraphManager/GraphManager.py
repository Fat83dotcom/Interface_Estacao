import io
import matplotlib.backends.backend_pdf
from GlobalFunctions.funcoesGlobais import maximos, minimos, dataInstantanea
import matplotlib
matplotlib.use('QtAgg')
import matplotlib.pyplot as plt


class PlotterGraficoPDF:
    def __init__(self, dataInicio: str) -> None:
        self.dtInicio = dataInicio
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

    def geradorCaminhoArquivoPDF(self, tipoGrafico: str) -> str:
        """
            Argumentos que devem ser passados para cada situação:
            Tipos de Gráfico -> 'umi', 'press', 'tempInt', 'tempExt'
        """
        arquivoPDF = f'{self.caminhoDiretorioPrograma}/{self.tipoGrafico[tipoGrafico]}{self.dtInicio}.pdf'
        return arquivoPDF

    def plotadorPDF(
        self, dadosEixo_Y: list, tipoGrafico: str, grandezaEixo_Y: str
    ) -> None:
        """
            Argumentos que devem ser passados para cada situação:
            tipoGrafico -> 'umi', 'press', 'tempInt', 'tempExt'
            Grandezas -> 'temp', 'press', 'umi'
        """
        tituloGrafico1 = f'{self.tipoGrafico[tipoGrafico]}\n-> Inicio: {self.dtInicio} <-|-> Termino: {dataInstantanea()} '
        tituloGrafico2 = f' <-\nMáxima: {maximos(dadosEixo_Y)} --- Mínima: {minimos(dadosEixo_Y)}'
        try:
            tempoEixo_X = range(len(dadosEixo_Y))
            arquivoPDF = self.geradorCaminhoArquivoPDF(tipoGrafico)
            plt.title(
                f'{tituloGrafico1}{tituloGrafico2}'
            )
            plt.xlabel('Tempo em segundos.')
            plt.ylabel(self.grandeza[grandezaEixo_Y])
            plt.plot(tempoEixo_X, dadosEixo_Y)
            plt.savefig(arquivoPDF)
            plt.clf()
        except (ValueError, Exception) as e:
            raise e

    def apagadorArquivosPDF(self, tipoGrafico: str) -> None:
        """
            Argumentos que devem ser passados para cada situação:
            Tipos de Gráfico -> 'umi', 'press', 'tempInt', 'tempExt'
        """
        try:
            os.remove(self.geradorCaminhoArquivoPDF(tipoGrafico))
        except Exception as e:
            raise e
