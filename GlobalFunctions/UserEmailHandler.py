'''
Este modulo faz a leitura do email, senha e destinatários de um arquivo
externo, que deve estar na mesma pasta que o executável Python.
'''
import sqlite3


class DBInterfaceConfig:
    def __init__(self, dbName: str) -> None:
        self.dbName = dbName

    def executeSQL(self, sql: str, *args) -> None:
        data = args
        con = sqlite3.connect(self.dbName)
        try:
            with con:
                con.execute(sql, *data)
        except Exception as e:
            raise e
        finally:
            con.close()

    def createTableEmailRemetente(self) -> None:
        sql = '''
        CREATE TABLE IF NOT EXISTS email_remetente
        (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email_remetente TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL
        )'''
        self.executeSQL(sql)

    def createTableEmailDestinatario(self) -> None:
        sql = '''
        CREATE TABLE IF NOT EXISTS email_destinatario
        (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email_destinatario TEXT NOT NULL UNIQUE
        )'''
        self.executeSQL(sql)

    def createTableDataBase(self) -> None:
        sql = '''
        CREATE TABLE IF NOT EXISTS data_base
        (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_cadastro TEXT NOT NULL UNIQUE,
        db_name TEXT NOT NULL,
        user TEXT NOT NULL,
        host TEXT NOT NULL,
        port TEXT NOT NULL,
        password TEXT NOT NULL
        )'''
        self.executeSQL(sql)

    def select(self, sql: str) -> list:
        con = sqlite3.connect(self.dbName)
        try:
            with con:
                cur = con.cursor()
                result = cur.execute(sql)
                return list(result)
        except Exception as e:
            print(e)
            raise e
        finally:
            con.close()

    def delete(self, table: str, collumn: str, *args) -> None:
        sql = f'DELETE FROM {table} WHERE {collumn}=?'
        data = args
        con = sqlite3.connect(self.dbName)
        try:
            with con:
                con.execute(sql, data)
        except Exception as e:
            raise e
        finally:
            con.close()


class ManipuladorDadosEmailRemetDest:
    def __init__(self, instanciadDB: DBInterfaceConfig) -> None:
        self.db = instanciadDB
        self.emailRemetente = 'Sem Remetente !'
        self.senha = 'Sem Senha !'

    def __setAttr(self) -> None:
        try:
            sql = 'SELECT "email_remetente", "senha" FROM email_remetente'
            dados: list = self.db.select(sql)
            if len(dados) == 0:
                self.emailRemetente = 'Sem Remetente !'
                self.senha = 'Sem Senha !'
            else:
                self.emailRemetente = dados[0][0]
                self.senha = dados[0][1]
        except Exception as e:
            raise e

    def meu_email(self) -> list[str]:
        try:
            self.__setAttr()
            return [self.emailRemetente]
        except Exception as e:
            raise e

    def minha_senha(self) -> list[str]:
        try:
            self.__setAttr()
            return [self.senha]
        except Exception as e:
            raise e


class ManipuladorEmailDestinatario:
    def __init__(self, instanciadDB: DBInterfaceConfig) -> None:
        self.db = instanciadDB

    def my_recipients(self) -> list[str]:
        try:
            sql = 'SELECT "email_destinatario" FROM email_destinatario'
            dados: list = self.db.select(sql)
            if len(dados) == 0:
                destinatario: list = ['Sem Destinatário !']
            else:
                destinatario: list = [email[0] for email in dados]

            return destinatario
        except Exception as e:
            raise e


if __name__ == '__main__':
    pass
