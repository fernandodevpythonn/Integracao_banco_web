from flask import render_template, request, redirect,url_for,session
from controllers.basecontroller import BaseController
from repositories.login_repository import LoginRepository
from services.login_service import LoginService
from database.connection import BancoMySql
from services.usuario_service import UsuarioService


class LoginController(BaseController):
    def __init__(self,app):
        self.rotas = [
            ('/login','login',self.pagina_login),
            ('/entrar', 'entrar', self.entrar, ['POST']),
            ('/logout', 'logout', self.logout),
            ('/cadastro','cadastro', self.cadastro),
            ('/registrar','registrar', self.registrar, ['POST'])
        ]
        super().__init__(app)
        self.db = BancoMySql()
        self.usuarios = [{"email":"senac@gmail.com","senha":"12345"}]
        self.login_repository = LoginRepository(self.db)

        self.login_service = LoginService(
            self.login_repository
        )

    def pagina_login(self):
        return render_template("login/pagina_login.html")
    
    def resultados(self):
        nome = request.form.get('nome')
        email = request.form.get('email')

        if not nome or not email:
            return "por favor, preencha os campos"
        
        return render_template("login/pagina_login.html",
                nome = nome,
                email = email)
    
    def login(self):
        if session.get("usuario_logado"):
            return redirect(url_for("home"))
        return render_template("basico_html/pagina_inicial.html")
        
    def entrar(self):
        email = request.form.get("email")
        senha = request.form.get("senha")

        usuario_valido = next((u for u in self.usuarios if u["email"] == email and u["senha"] == senha), None)

        if usuario_valido:
            session["usuario_logado"] = True
            session["usuario_id"] = usuario_valido["id"]
            self.login_service.registrar_login(usuario_valido["id"])
            return redirect(url_for("home"))
        else:
            erro = "usuario ou senha incorretos"
            return render_template("login/pagina_login.html", erro = erro)

    def registrar(self):
        email = request.form.get("email")
        senha = request.form.get("senha")

        if not email or not senha:
            erro = "Todos os campos devem ser preenchidos"
            return render_template("login/cadastro.html", erro = erro)
        
        self.usuarios.append({
            "email":email,
            "senha":senha
        })
        sucesso = "cadastro realizado com sucesso!"
        return render_template("login/pagina_login.html", sucesso = sucesso)


    def cadastro(self):
        return render_template("login/cadastro.html")
    
    def logout(self):
        session.clear()
        return redirect(url_for("login"))