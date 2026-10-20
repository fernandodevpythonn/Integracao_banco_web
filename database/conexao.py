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
                host = os.getenv("DB_HOST"),
                user = os.getenv("DB_USER"),
                password = os.getenv("DB_PASS"),
                port = int(os.getenv("DB_PORT"))
            )

            cursor = conexao.cursor()
            cursor.execute("""SELECT COUNT(*) FROM information_schema.SCHEMATA WHERE SCHEMA_NAME = %s""",(nome_banco,))
            num_resultado = cursor.fetchone()[0]

            if num_resultado == 0:
                cursor.execute(f"CREATE DATABASE `{nome_banco}`")
                print(f"banco de dados '{nome_banco}' criado com sucesso")
            
            cursor.close()
            conexao.close()

            self.conexao = mysql.connector.connect(
                host = os.getenv("DB_HOST"),
                user = os.getenv("DB_USER"),
                password = os.getenv("DB_PASS"),
                database = nome_banco,
                port = int(os.getenv("DB_PORT")))
            self.cursor = self.conexao.cursor()
        except Error as e:
            print(f"Erro ao conectar ao mysql: {e}")
            raise

    def executar(self,sql,parametros=None):
        self.cursor.execute(sql,parametros or ())
        self.conexao.commit()

    def fechar(self):
        if self.cursor:
            self.cursor.close()
        if self.conexao:
            self.conexao.close()

    def __del__(self):
        try:
            self.fechar()
        except Exception:
            pass