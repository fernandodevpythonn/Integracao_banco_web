from flask import Flask
from controllers.html_basicocontroller import htmlbasicocontroller
from controllers.logincontroller import LoginController
from dotenv import load_dotenv
import os

from database.connection import BancoMySql
from database.tables import BancoTabelas
load_dotenv()
app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY")

htmlbasicocontroller(app)
LoginController(app)




db = BancoMySql()

tabelas = BancoTabelas(db)

tabelas.criar_tabelas()

if __name__ == "__main__":
    app.run(debug=os.getenv("DEBUG","False").lower()=="true")