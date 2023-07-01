'''
Este módulo comporta funções de uso geral, adaptadas às rotinas do programa,
usadas em classes e métodos de classe, portanto, caso haja mudança das
classes para outros módulos .py, é necessário importar este módulo em seus
respectivos escopos.
'''
import time


class DadosError(Exception):
    ...


def dataInstantanea() -> str:
    try:
        data = time.strftime('%d %b %Y %H:%M:%S', time.localtime())
        return data
    except (ValueError, Exception) as e:
        raise e


def dataDoArquivo() -> str:
    try:
        dataA = time.strftime('%b_%Y_log.csv').lower()
        return dataA
    except (ValueError, Exception) as e:
        raise e


def maximos(dados) -> float:
    try:
        return round(max(dados), 2)
    except (ValueError, Exception) as e:
        raise DadosError(f'{e.__class__.__name__} -> função: {maximos.__name__}: Não há dados a serem processados.')


def minimos(dados) -> float:
    try:
        return round(min(dados), 2)
    except (ValueError, Exception) as e:
        raise DadosError(f'{e.__class__.__name__} -> função: {minimos.__name__}: Não há dados a serem processados.')
