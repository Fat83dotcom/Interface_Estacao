'''
Este módulo comporta funções de uso geral, adaptadas às rotinas do programa,
usadas em classes e métodos de classe, portanto, caso haja mudança das
classes para outros módulos .py, é necessário importar este módulo em seus
respectivos escopos.
'''
from datetime import datetime


class DadosError(Exception):
    ...


def dataBancoDados() -> str:
    try:
        return datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    except (ValueError, Exception) as e:
        raise e


def dataInstantanea() -> str:
    try:
        return datetime.now().strftime('%d %b %Y %H:%M:%S')
    except (ValueError, Exception) as e:
        raise e


def dataDoArquivo() -> str:
    try:
        dataA = datetime.now().strftime('%b_%Y_log.csv').lower()
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
