from controllers.base_controller import BaseController
from flask import render_template,session,url_for,request,redirect
from repositories.usuario_repository import UsuarioRepository
from services.usuario_service import UsuarioService
from database.connection import BancoMysql
from mysql.connector import Error
from repositories.auditoria_repository import AuditoriaRepository
from services.auditoria_service import AuditoriaService
from repositories.login_repository import LoginRepository
from services.login_service import LoginService

class LoginController(BaseController):
    def __init__(self,app):
     self.rotas = [
        ('/paginalogin','paginalogin',self.pagina_login),
        ('/paginacadastro','paginacadastro',self.pagina_cadastro),
        ('/entrar','entrar',self.entrar,['POST']),
        ('/registrar','registrar',self.registrar,['POST']),
        ('/logout','logout',self.logout)
     ]

     super().__init__(app)

     self.db = BancoMysql()
     self.usuario_repository = UsuarioRepository(self.db)
     self.usuario_service = UsuarioService(self.usuario_repository)
     self.auditoria_repository = AuditoriaRepository(self.db)
     self.auditoria_service = AuditoriaService(self.auditoria_repository)
     self.login_repository = LoginRepository(self.db)
     self.login_service = LoginService(self.login_repository)

    def pagina_login(self):
       if session.get("usuario_logado"):
          return redirect(url_for("home"))
       
       return render_template("login_pagina.html")
    
    def pagina_cadastro(self):
       return render_template("cadastro_pagina.html")
    
    def entrar(self):
       nome = request.form.get("nome")
       senha = request.form.get("senha")

       if not nome or not senha:
          erro = "preencha o usuario e senha."

          return render_template(
             "login_pagina.html", erro = erro
          )
       
       usuario_valido = self.usuario_service.autenticar(nome,senha)
       if usuario_valido:
         #  adiciona os dados do usuario na sessao, para depois poder consultar
          session["usuario_logado"] = True
          session["usuario_id"] = usuario_valido["id"]
          session["nome"] = usuario_valido["nome"]
          session["perfil_logado"] = usuario_valido["perfil"]
          
          self.login_service.registrar_login(
             usuario_valido["id"]
          )

          self.auditoria_service.registrar(
             usuario_id=usuario_valido["id"],acao="LOGIN_SUCESSO",entidade="LOGIN",descricao="login realizado",ip=request.remote_addr)
             
          return redirect(
             url_for("home")
          )
       else:
          erro = "usuario ou senha incorretos"

          return render_template(
             "login_pagina.html",erro = erro
          )

    def registrar(self):
       nome = request.form.get("nome")
       senha = request.form.get("senha")

       if not nome or not senha:
          erro = "usuário e senha são obrigatórios"

          return render_template("cadastro_pagina.html",erro=erro)
       try:
          self.usuario_service.cadastrar(nome=nome,senha=senha,perfil="usuario")
       except Error as e:
          print(f"Erro:{e}, Usuário não cadastrado.")
       sucesso = "cadastro realizado, faça login."
       
       return render_template("login_pagina.html",sucesso=sucesso)
    

    def logout(self):
       
       usuario_id = session.get("usuario_id")
       self.auditoria_service.registrar(usuario_id=usuario_id,acao="LOGOUT",entidade="LOGIN",descricao="logout realizado",ip=request.remote_addr)

       session.clear()

       return redirect(
          url_for("paginalogin")
       )