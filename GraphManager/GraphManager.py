import io
from datetime import datetime
import matplotlib.backends.backend_pdf
from dateutil.relativedelta import relativedelta
from GlobalFunctions.funcoesGlobais import maximos, minimos
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('QtAgg')


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

    def manipuladorDatas(self, dataInicio: str) -> datetime:
        formato = '%d %b %Y %H:%M:%S'
        resultado: datetime = datetime.strptime(dataInicio, formato)
        return resultado

    def plotadorPDF(
        self, dadosEixo_Y: list, tipoGrafico: str, grandezaEixo_Y: str
    ) -> None:
        """
            Argumentos que devem ser passados para cada situação:
            tipoGrafico -> 'umi', 'press', 'tempInt', 'tempExt'
            Grandezas -> 'temp', 'press', 'umi'
        """
        tituloGrafico1 = f'-> Inicio: {self.dtInicio} | Termino: {self.dtTermino} '
        tituloGrafico2 = f' <-\nMáxima: {maximos(dadosEixo_Y)} --- Mínima: {minimos(dadosEixo_Y)}'
        try:
            buffer = io.BytesIO()
            inicioSerie = self.manipuladorDatas(self.dtInicio)
            tempoEixo_X = [
                inicioSerie + relativedelta(seconds=i) for i in range(
                    len(dadosEixo_Y)
                )
            ]
            plt.figure(figsize=(10, 6))
            plt.title(
                f'{tituloGrafico1}{tituloGrafico2}'
            )
            plt.xlabel('Hora.')
            plt.ylabel(self.grandeza[grandezaEixo_Y])
            plt.plot(
                tempoEixo_X, dadosEixo_Y,
                marker='.', linestyle='--',
                color='red', label=self.tipoGrafico[tipoGrafico]
            )
            plt.legend()
            plt.grid(True)
            plt.grid(color='gray', linestyle='dashed', linewidth=0.5)
            plt.xticks(rotation=40)
            plt.savefig(buffer, format='pdf')
            plt.clf()
            return buffer
        except (ValueError, Exception) as e:
            raise e
