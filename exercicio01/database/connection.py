import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()

class BancoMySql:
    def __init__(self):
        nome_banco = os.getenv("DB_NAME")

        try:
            conexao = mysql.connector.connect(
                user = os.getenv("DB_USER"),
                host = os.getenv("DB_HOST"),
                password = os.getenv("DB_PASSWORD"),
                port = int(os.getenv("DB_PORT"))
            )

            cursor = conexao.cursor()
            cursor.execute("""SELECT COUNT(*) FROM information_schema.SCHEMATA WHERE SCHEMA_NAME = %S""",(nome_banco,))
            num_results = cursor.fetchone()[0]

            if num_results == 0:

                cursor.execute(f"CREATE DATABASE `{nome_banco}`")
                print(f"Banco de dados '{nome_banco}' criado com sucesso.")

            cursor.close()
            conexao.close()

            self.conexao = mysql.connector.connect(
                host = os.getenv("DB_HOST"),
                user = os.getenv("DB_USER"),
                password = os.getenv("DB_PASSWORD"),
                database = nome_banco,
                port = int(os.getenv("DB_PORT")))
            self.cursor = self.conexao.cursor()

        except Error as e:
            print(f"Erro ao conectar ao banco {e}")
            raise

    
    