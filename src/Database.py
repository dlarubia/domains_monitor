import psycopg2
from psycopg2 import extensions, sql
# from config import config

class Database:

    def __init__(self, user, password, host, port, db_name, sql_script = 'structure_database.sql'):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.db_name = db_name.lower()
        self.sql_script = sql_script
        self.checkIfDatabaseExists()


    def connect(self):
        conn = psycopg2.connect(user=self.user, password=self.password, host=self.host, port=self.port, database=self.db_name)
        autocommit = extensions.ISOLATION_LEVEL_AUTOCOMMIT
        conn.set_isolation_level(autocommit)
        return conn.cursor(), conn

    def execute_query(self, query, user_input=[]):
        query_result = None
        try:
            cursor, conn = self.connect()
            cursor.execute(query, user_input)
            if cursor.rowcount > 0:
                if cursor.statusmessage != 'UPDATE 1' and cursor.statusmessage != 'INSERT 0 1':  # improve it later 
                    query_result = cursor.fetchall()
            else:
                query_result = None
        except Exception as e:
            # TODO
            print('Exception during query execution: ' + str(e)) # Escrever log em arquivo posteriormente
        finally:
            cursor.close()
            conn.close()
        return query_result

    def checkIfDatabaseExists(self):
        print("Checking if database '" + self.db_name + "' exists...")
        try:
            cursor, conn = self.connect()
            print("Database already exist.")
            conn.close()
            # TODO -> Verificar a necessidade de manter essa chamada de função caso a database já exista
            # self.structure_database()
        except Exception as e:
            # print(e)
            print("Database doesnt exist. Creating...")
            self.createDatabase()
            self.structure_database()

    def createDatabase(self):
        conn = psycopg2.connect(user=self.user, password=self.password, host=self.host, port=self.port)
        autocommit = extensions.ISOLATION_LEVEL_AUTOCOMMIT
        conn.set_isolation_level(autocommit)
        cursor = conn.cursor()
        query = "CREATE DATABASE {}"
        cursor.execute(sql.SQL(query).format(sql.Identifier(self.db_name)))
        cursor.close()
        conn.close()

    # Lê o arquivo que contém a estrutura para criação do banco de dados e executa
    def structure_database(self):
        # print("Creating tables in " + self.db_name + " if doesnt exists...")
        print("Creating tables in " + self.db_name + "...")
        f = open(self.sql_script, 'r')
        query = f.read()
        self.execute_query(query)