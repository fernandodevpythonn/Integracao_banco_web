from flask import render_template,request,url_for,session,redirect
from controllers.base_controller import BaseController

class LoginController(BaseController):
    def __init__(self,app):
        self.rotas = [
            ('/loginpagina','loginpagina',self.pagina_login),
            ('/cadastropagina','cadastropagina',self.pagina_cadastro),
        ]
        super().__init__(app)
        self.usuarios = [{"email":"fernando@gmail.com","senha":"12345"}]

    def pagina_login(self):
        return render_template("pagina_login.html")
    def pagina_cadastro(self):
        return render_template("pagina_cadastro.html")
    
    def login(self):
        if session.get("usuario_logado"):
            return redirect(url_for("home"))
        return render_template("pagina_login.html")
    
    def entrar(self):
        email = request.form.get("email")
        senha = request.form.get("senha")
        usuario_valido = next((u for u in self.usuarios if u["email"] == email and u["senha"] == senha), None)

        if usuario_valido:
            session["usuario_logado"] = True
            return redirect(url_for("home"))
        else:
            erro = "usuario ou senha inválidos"
            return render_template("pagina_login.html", erro = erro)