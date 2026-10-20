from controllers.html_basico_controller import HTMLbasicocontroller
from flask import Flask
from controllers.login_controller import LoginController
import os

from database.connection import BancoMysql
from database.tables import BancoTabelas

app = Flask(__name__)

db = BancoMysql()
tabelas = BancoTabelas(db)

tabelas.criar_tabelas()

LoginController(app)
HTMLbasicocontroller(app)

app.secret_key = os.getenv("SECRET_KEY")

if __name__ == "__main__":
    app.run(debug=os.getenv("DEBUG","False").lower() == "true")