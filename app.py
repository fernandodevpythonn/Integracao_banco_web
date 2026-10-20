from dotenv import load_dotenv
from flask import Flask
from database.conexao import BancoMySql
from database.tabelas import Tabelas
import os
load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY")

#zzz
db = BancoMySql()

tabelas = Tabelas(db)

tabelas.criar_tabelas()


if __name__ == "__main__":
    app.run(debug=os.getenv("DEBUG", "False").lower() == "true")