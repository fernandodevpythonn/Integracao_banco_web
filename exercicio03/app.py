from flask import Flask
from controllers.html_basico_controller import HTMLbasicoController
from controllers.login_controller import LoginController
import os
from dotenv import load_dotenv
from database.connection import BancoMysql
from database.tabelas import BancoTabelas

load_dotenv()

app = Flask(__name__)

HTMLbasicoController(app)
LoginController(app)
app.secret_key = os.getenv("SECRET_KEY")

db = BancoMysql()
tabelas = BancoTabelas(db)

tabelas.criar_tabelas()

if __name__ == "__main__":
    app.run(debug=os.getenv("DEBUG", "False").lower() == "true")

