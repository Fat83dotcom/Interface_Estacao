import DataBaseManager.confidentials


def dbCredentials(database: int) -> dict:
    CONFIG = DataBaseManager.confidentials.bataBaseChoice(database)
    return CONFIG
