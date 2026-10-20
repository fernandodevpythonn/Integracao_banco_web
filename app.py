from controllers.basico_controller import basico_controller
from controllers.login_controller import LoginController
from database.connection import BancoMysql
from database.tables import BancoTabelas
from dotenv import load_dotenv
from repositories.auditoria_repository import AuditoriaRepository
from controllers.auditoria_controller import AuditoriaController
from controllers.usuario_controller import UsuarioController
from security.waf import configurar_waf

import os
from flask import Flask
banco = BancoMysql()
tabelas = BancoTabelas(banco)
tabelas.criar_tabelas()
load_dotenv()

auditoria_repository = AuditoriaRepository(banco)
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE-SECURE"]=True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

configurar_waf(app)

@app.after_request

def adicionar_headers_seguranca(response):
    response.headers["X-Content-Type-Options"] = "nosiff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = ("geolocation=(),microphone(),camera=()")
    response.headers["Content-Security-Policy"] = (
        "default-src 'self';"
        "script-src 'self'"
        "style-src 'self';"
        "img-src 'self' data:;"
        "font-src 'none';"
        "base-uri 'self';"
        "form-action 'self';"
        "frame-ancestors 'self';"
    )
    return response

AuditoriaController(app)
basico_controller(app)
LoginController(app)
UsuarioController(app)

if __name__ == "__main__":
    app.run(debug=os.getenv("DEBUG","False").lower()=="true")