import psycopg
from abc import ABC
from psycopg import sql
from LogFiles import LogErrorsMixin
from databaseSettings import dbCredentials
from psycopg import Error


class DataBase(ABC, LogErrorsMixin):
    '''Classe abstrata que fornece os serviços básicos
    para as operações do banco de dados'''
    def __init__(self, dBConfig: dict) -> None:
        self.host: str = dBConfig['host']
        self.port: str = dBConfig['port']
        self.dbname: str = dBConfig['dbname']
        self.user: str = dBConfig['user']
        self.password: str = dBConfig['password']

    def toExecute(self, query: tuple):
        '''
            Abre e fecha conexões, executa transações
            com segurança mesmo em casos de falha.
        '''
        try:
            with psycopg.connect(
                host=self.host,
                dbname=self.dbname,
                user=self.user,
                port=self.port,
                password=self.password
            ) as con:
                with con.cursor() as cursor:
                    sQL, data = query
                    cursor.execute(sQL, data)
        except (Error, Exception) as e:
            className = self.__class__.__name__
            methName = self.toExecute.__name__
            self.registerErrors(className, methName, e)
            raise e

    def toExecuteSelect(self, query) -> list:
        '''
            Abre e fecha conexões, executa transações de select
            com segurança mesmo em casos de falha.
        '''
        try:
            with psycopg.connect(
                host=self.host,
                dbname=self.dbname,
                user=self.user,
                port=self.port,
                password=self.password
            ) as con:
                with con.cursor() as cursor:
                    sQL, data = query
                    cursor.execute(sQL, data)
                    dataRecovery: list = [x for x in cursor.fetchall()]
                    return dataRecovery
        except (Error, Exception) as e:
            className = self.__class__.__name__
            methName = self.toExecute.__name__
            self.registerErrors(className, methName, e)
            raise e

    def placeHolderSQLGenerator(self, values) -> str | None:
        try:
            placeHolders: str = ''
            sizeValues = len(values)
            for n, _ in enumerate(values):
                if sizeValues == 1 or n == (sizeValues - 1):
                    placeHolders += '%s'
                else:
                    placeHolders += '%s, '
            return placeHolders
        except (Error, Exception) as e:
            className = self.__class__.__name__
            methName = self.placeHolderSQLGenerator.__name__
            self.registerErrors(className, methName, e)
            raise e

    def SQLInsertGenerator(
        self, *args,
        collumn: tuple,
        table: str,
        schema: str
    ) -> tuple | None:
        try:
            values = args[0]
            query: tuple | None = sql.SQL(
                "INSERT INTO {table} ({collumn}) VALUES ({pHolders})"
            ).format(
                table=sql.Identifier(schema, table),
                collumn=sql.SQL(', ').join(map(sql.Identifier, collumn)),
                pHolders=sql.SQL(', ').join(sql.Placeholder() * len(collumn))
            ), values
            return query
        except (Error, Exception) as e:
            className = self.__class__.__name__
            methName = self.SQLInsertGenerator.__name__
            self.registerErrors(className, methName, e)
            raise e

    def SQLUpdateGenerator(
            self, *args,
            collumnUpdate: str,
            collumnCondicional: str,
            table: str,
            schema: str,
            update: str,
            conditionalValue: str
            ):
        try:
            query = sql.SQL(
                "UPDATE {table} SET {colUp}=%s WHERE {colCon}=%s"
            ).format(
                table=sql.Identifier(schema, table),
                colUp=sql.Identifier(collumnUpdate),
                colCon=sql.Identifier(collumnCondicional)
            ), (update, conditionalValue)
            return query
        except (Error, Exception) as e:
            className = self.__class__.__name__
            methName = self.SQLUpdateGenerator.__name__
            self.registerErrors(className, methName, e)
            raise e

    def SQLDeleteGenerator(self) -> tuple | None:
        pass

    def SQLSelectGenerator(self) -> tuple | None:
        pass


class OperationDataBase(DataBase, LogErrorsMixin):
    '''Realiza as operações com o PostgreSQL'''
    def __init__(self, dBConfig: dict) -> None:
        super().__init__(dBConfig)

    def updateTable(
        self,
        table: str,
        collumnUpdate: str,
        collumnCondicional: str,
        update: str,
        conditionalValue: str,
        schema='public',
    ):
        '''
            Atualiza colunas.
            Parametros: collumn -> Nome da coluna
            condition -> Condição de atualização
            update -> Valor da modificação
        '''
        try:
            query = self.SQLUpdateGenerator(
                table=table,
                collumnUpdate=collumnUpdate,
                collumnCondicional=collumnCondicional,
                schema=schema,
                update=update,
                conditionalValue=conditionalValue
            )
            self.toExecute(query)
        except (Error, Exception) as e:
            className = self.__class__.__name__
            methName = self.updateTable.__name__
            self.registerErrors(className, methName, e)
            raise e

    def insertTable(
        self, *args, table: str, collumn: tuple, schema='public'
    ):
        '''
            Insere dados na tabela.
            Parametros:
            *args -> tupla com os valores, em ordem com a coluna
            collumn -> Nome das colunas, na ordem de inserção.
        '''
        try:
            query = self.SQLInsertGenerator(
                *args, table=table, collumn=collumn, schema=schema
            )
            self.toExecute(query)
        except (Error, Exception) as e:
            className = self.__class__.__name__
            methName = self.insertTable.__name__
            self.registerErrors(className, methName, e)
            raise e

    def deleteOnTable(self) -> None:
        pass

    def selectOnTable(self, method):
        pass


class DataModel(LogErrorsMixin):
    '''
        Implementa uma interface para receber os dados e realiza as
        transações para cada tabela do banco.
    '''
    def __init__(self, dB: OperationDataBase) -> None:
        self.DBInstance = dB

    def execInsertTable(self, table: str, iterable: list) -> None:
        '''
            Implementa uma estrutura pra inserir dados em tabelas.
            Retorna -> None
        '''
        raise NotImplementedError('Implemente o metodo em uma subclasse'
                                  ' relativa a tabela trabalhada.')

    def execCreateTable(self, tableName: str) -> None:
        '''
            Implementa uma estrutura para criar tabelas.
            Retorna -> None
        '''
        raise NotImplementedError('Implemente o metodo em uma subclasse'
                                  ' relativa a tabela trabalhada.')

    def execUpdateTable(self, table: str, iterable: list) -> None:
        '''
            Implementa uma estrutura para atualizar tabelas.
            Retorna -> None
        '''
        raise NotImplementedError('Implemente o metodo em uma subclasse'
                                  ' relativa a tabela trabalhada.')

    def execDeleteOnTable(self, table: str, key: str) -> None:
        '''
            Implementa uma estrutura para deletar linhas em tabelas.
            Retorna -> None
        '''
        raise NotImplementedError('Implemente o metodo em uma subclasse'
                                  ' relativa a tabela trabalhada.')

    def execSelectOnTable(self, table: str, *args) -> list:
        '''
            Implementa uma estrutura para criar buscar dados em tabelas.
            Retorna -> None
        '''
        raise NotImplementedError('Implemente o metodo em uma subclasse'
                                  ' relativa a tabela trabalhada.')


class DadoHorario(DataModel):
    def __init__(self, dB: OperationDataBase) -> None:
        super().__init__(dB)

    def execCreateTable(self, tableName: str, schema='public', fk=0) -> None:
        query: tuple = f"""
        CREATE TABLE IF NOT EXISTS "{schema}"."{tableName}"
        (codigo serial not null PRIMARY KEY,
        codigo_d_d bigint not null DEFAULT {fk},
        data_hora timestamp not null UNIQUE,
        umidade double precision null,
        pressao double precision null,
        temp_int double precision null,
        temp_ext double precision null,
        FOREIGN KEY(codigo_d_d) REFERENCES dado_diario(codigo))""", ()
        self.DBInstance.toExecute(query)

    def execInsertTable(self, table: str, iterable: list) -> None:
        pass

    def execSelectOnTable(self, table: str, *args) -> list:
        pass


if __name__ == '__main__':
    # m = ConverterMonths()
    # print(m.getMonths('05'))

    bd = OperationDataBase(dbCredentials(4))
    # bd.insertCollumn(
    # ('J.Pereira porcalhus',), table='teste', collumn=('nome', )
    # )
    bd.updateTable(
        table='teste',
        collumnUpdate='nome',
        collumnCondicional='codigo',
        update='Jãozin',
        conditionalValue='6'
    )
    data = bd.toExecuteSelect(('select * from teste', ()))
