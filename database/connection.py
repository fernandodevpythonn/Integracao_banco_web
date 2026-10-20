from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error
import os
load_dotenv()


class BancoMysql:
    def __init__(self):
      nome_banco = os.getenv("DB_NAME")

      try:
        conexao = mysql.connector.connect(
            host = os.getenv("DB_HOST"),
            user = os.getenv("DB_USER"),
            password = os.getenv("DB_PASSWORD"),
            port = int(os.getenv("DB_PORT"))
        )
        cursor = conexao.cursor()
        cursor.execute("""SELECT COUNT(*) FROM information_schema.SCHEMATA WHERE SCHEMA_NAME = %s""",(nome_banco,))
        num_results = cursor.fetchone()[0]

        if num_results == 0:
           cursor.execute(f"CREATE DATABASE `{nome_banco}`")
           print(f"Banco {nome_banco} criado com sucesso")
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
         print(f"Erro ao conectar no banco {e}")
         raise
      
    def executar(self,sql,parametros = None):
       self.cursor.execute(sql,parametros or ())
       self.conexao.commit()

    def consultar_um(self,sql,parametros=None):
       self.cursor.execute(sql,parametros or ())
       return self.cursor.fetchone()
   
    def consultar(self, sql, parametros=None):
       self.conexao.commit()
       self.cursor.execute(sql,parametros or ())
       return self.cursor.fetchall()

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
        