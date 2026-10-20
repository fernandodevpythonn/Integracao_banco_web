from flask import Flask
from controllers.html_basicocontroller import htmlbasicocontroller
from controllers.logincontroller import LoginController
from dotenv import load_dotenv
import os

from database.connection import BancoMySql
from database.tables import BancoTabelas
from flask import session, render_template,request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from services.ratelimit_service import RateLimitService
from repositories.ratelimit_repo import RateLimitRepository

load_dotenv()
app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY")

htmlbasicocontroller(app)
LoginController(app)

quantidade_requisicoes = 5

periodo = "minute"

# "second"
# "minute"
# "hour"
# "day"
# "month"



# limiter = Limiter(
#     key_func=get_remote_address,
#     default_limits=[
#         f"{quantidade_requisicoes} per {periodo}"
#     ]
# )




limiter = Limiter(key_func=get_remote_address,default_limits=[f"{quantidade_requisicoes} per {periodo}"],storage_uri="memory://")


limiter.init_app(app)


db = BancoMySql()

tabelas = BancoTabelas(db)

tabelas.criar_tabelas()

ratelimit_repository = RateLimitRepository(db)

ratelimit_service = RateLimitService(ratelimit_repository)

@app.errorhandler(429)
def limite_excedido(e):
    ratelimit_service.registrar_bloqueio(
        usuario_id=session.get("usuario_id"),
        ip=request.remote_addr,
        rota = request.path,
        metodo=request.method,
        limite=str(e.description),
        motivo="limite de tentativas de login excedido"
    )
    return render_template("/login/pagina_login.html",erro="muitas tentativas. Aguarde um momento e tente novamente."),429

if __name__ == "__main__":
    app.run(debug=os.getenv("DEBUG","False").lower()=="true")