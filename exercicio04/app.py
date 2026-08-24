from flask import Flask
from controllers.htmlbasico_controller import HTMLbasicoController
from controllers.login_controller import LoginController
from database.connection import Mysql
from database.tables import BancoTabelas
import os
from dotenv import load_dotenv

load_dotenv()

banco = Mysql()
tabelas = BancoTabelas(banco)
tabelas.criar_tabelas()
app = Flask(__name__)
HTMLbasicoController(app)
LoginController(app)

app.secret_key = os.getenv("SECRET_KEY")
if __name__ == "__main__":
    app.run(debug= os.getenv("DEBUG","False").lower() == "true")