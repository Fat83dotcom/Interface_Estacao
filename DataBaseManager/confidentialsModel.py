'''
    ##########  ATENÇÃO    ##########
    Este modulo deve ser ocultado por .gitignore, pois após
    o preenchimento haverá dados que não devem ser divulgados.
'''


def bataBaseChoice(database: int) -> dict:
    if database == 1:
        id1: dict = {
            'dbname': '',
            'user': '',
            'host': '',
            'port': '',
            'password': '',
        }
        return id1
    if database == 2:
        id2: dict = {
            'dbname': '',
            'user': '',
            'host': '',
            'port': '',
            'password': '',
        }
        return id2
    return {
        'dbname': 'postgres',
        'user': 'postegres',
        'host': 'localhost',
    }
