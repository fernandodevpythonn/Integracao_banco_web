from controllers.base_controller import BaseController
from flask import render_template,request,redirect,url_for,session
class LoginController(BaseController):
    def __init__(self,app):
        self.rotas = [
            ('/cadastro','cadastro',self.pagina_cadastro),
            ('/login','login', self.pagina_login),
            ('/entrar','entrar', self.entrar,['POST']),
            ('/registrar','registrar', self.registrar,['POST']),
            ('/logout','logout',self.logout),

        ]
        super().__init__(app)

        self.usuarios = [{"email":"fernando@gmail.com","senha":"12345"}]

    def pagina_cadastro(self):
        return render_template("pagina_cadastro.html")
    def pagina_inicial(self):
        return render_template("pagina_inicial.html")
    def registrar(self):
        email = request.form.get("email")
        senha = request.form.get("senha")

        if not email or not senha:
            erro = "todos os campos devem ser preenchidos"
            return render_template("pagina_login.html", erro = erro)
        self.usuarios.append({
            "email":email,
            "senha":senha
        })
        sucesso = "cadastro realizado com sucesso"
        return render_template("pagina_login.html", sucesso = sucesso)
    
    def entrar(self):
        email = request.form.get("email")
        senha = request.form.get("senha")
        usuario_correto = next((u for u in self.usuarios if u["email"] == email and u["senha"] == senha), None)

        if usuario_correto:
            session["usuario_logado"]= True
            return redirect(url_for("home"))
        else:
            erro = "email ou senha incorretos"
            return render_template("pagina_login.html", erro = erro)
    
    def pagina_login(self):
        return render_template("pagina_login.html")

    def login(self):
        if session.get("usuario_logado"):
            return redirect(url_for("home"))
        return render_template("pagina_login.html")
    
    def logout(self):
        session.clear()
        return redirect(url_for("login"))