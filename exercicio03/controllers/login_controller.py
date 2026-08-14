from controllers.base_controller import BaseController
from flask import render_template,session,url_for,request,redirect
class LoginController(BaseController):
    def __init__(self,app):
        self.rotas = [
            ('/cadastro','cadastro',self.pagina_cadastro),
            ('/login','login',self.login),
            ('/loginpagina','loginpagina',self.pagina_login),
            ('/entrar','entrar',self.entrar,['POST']),
            ('/logout','logout',self.logout),
            ('/cadastrar','cadastrar',self.cadastrar,['POST'])
        ]
        super().__init__(app)
        self.usuarios = [{"email":"fernando@gmail.com","senha":"12345"}]

    def pagina_cadastro(self):
        return render_template("pagina_cadastro.html")
    def pagina_login(self):
        return render_template("pagina_login.html")
    
    def entrar(self):
        email = request.form.get("email")
        senha = request.form.get("senha")
        usuario_valido = next((u for u in self.usuarios if u["email"] == email and u["senha"] == senha ), None)

        if usuario_valido:
            session["usuario_logado"] = True
            return redirect(url_for("home"))
        else:
            erro = "email ou senha inválidos"
            return render_template("pagina_login.html",erro = erro)
        
    def login(self):
        if session.get("usuario_logado"):
            return redirect(url_for("home"))
        return render_template("pagina_login.html")
    
    def logout(self):
        session.clear()
        return redirect(url_for("login"))
    
    def cadastrar(self):
        email = request.form.get("email")
        senha = request.form.get("senha")

        if not email or not senha:
            erro = "erro, preencha todos os dados"
            return render_template("/cadastro", erro = erro)
        
        self.usuarios.append({
            "email": email,
            "senha":senha
        })

        sucesso = "cadastro realizado! faça o login"
        return render_template("pagina_login.html", sucesso = sucesso)