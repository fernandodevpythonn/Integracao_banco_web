from flask import render_template, request, redirect, url_for, session, Response

from controllers.base_controller import BaseController

from database.connection import BancoMysql

from repositories.usuario_repository import UsuarioRepository
from services.usuario_service import UsuarioService
from repositories.auditoria_repository import AuditoriaRepository
from services.auditoria_service import AuditoriaService
from services.imagem_service import ImagemService

import base64

class UsuarioController(BaseController):
    def __init__(self,app):
        self.rotas = [
            ('/usuarios','usuarios', self.listar,['GET'],'administrador'),
            ('/usuarios/cadastrar', 'cadastrar_usuario',self.cadastrar,['GET', 'POST'], 'administrador'),
            ('/usuarios/editar/<int:usuario_id>','editar_usuario',self.atualizar,['GET','POST'],'administrador'),
            ('/usuarios/excluir/<int:usuario_id>','excluir_usuario',self.excluir,['POST'],'administrador'),
            ('/usuarios/excluir/<int:usuario_id>','confirmar_exclusao_usuario',self.confirmar_exclusao,['GET'],'administrador'),
            ('/perfil','perfil',self.editar_perfil,['GET','POST'],'autenticado'),
            ('/perfil/imagem','imagem_perfil', self.proteger_rota(self.imagem_perfil),['GET'],'autenticado'),
            ('/usuarios/<int:usuario_id>/imagem','imagem_usuario',self.proteger_rota(self.imagem_usuario),['GET'], 'administrador')
        ]

        super().__init__(app)

        self.db = BancoMysql()
        self.repository_usuario = UsuarioRepository(self.db)
        self.usuario_service = UsuarioService(self.repository_usuario)
        self.auditoria_repository = AuditoriaRepository(self.db)
        self.auditoria_service = AuditoriaService(self.auditoria_repository)
        self.imagem_service = ImagemService()
    def listar(self):
            usuarios = self.usuario_service.listar_todos()
            return render_template("html_usuarios/usuarios.html", usuarios=usuarios)
     
    def cadastrar(self):
            if request.method == 'POST':

             nome_usuario = request.form.get("nome")
             senha = request.form.get("senha")
             confirmar_senha = request.form.get("confirmar_senha")
             perfil = request.form.get("perfil")


             if (
                not nome_usuario
                or not senha
                or not confirmar_senha
                or not perfil
             ):

                return render_template(
                    "html_usuarios/cadastrar.html",
                    erro="Preencha todos os campos.",
                    dados=request.form
                )


             if senha != confirmar_senha:

                return render_template(
                    "html_usuarios/cadastrar.html",
                    erro="As senhas não coincidem.",
                    dados=request.form
                )


             try:

                usuario_id = self.usuario_service.cadastrar(

                    nome=nome_usuario,

                    senha=senha,

                    perfil=perfil
                )


                self.auditoria_service.registrar(

                    usuario_id=session.get("usuario_id"),

                    acao="CADASTRO",

                    entidade="USUARIO",

                    entidade_id=usuario_id,

                    descricao="Usuário cadastrado pelo administrador",

                    ip=request.remote_addr
                )


             except ValueError as e:

                return render_template(
                    "html_usuarios/cadastrar.html",
                    erro=str(e),
                    dados=request.form
                )


             return redirect(
                url_for("usuarios")
              )


            return render_template(
            "html_usuarios/cadastrar.html"
           )
    def atualizar(self,usuario_id):
         usuario = self.usuario_service.buscar_por_id(usuario_id)
    
         if not usuario:
             return "usuário não encontrado", 404
         
         if request.method == 'POST':
             nome_usuario = request.form.get("nome")
             perfil = request.form.get("perfil")
             senha = request.form.get("senha")
             confirmar_senha = request.form.get("confirmar_senha")
             imagem = request.files.get("imagem")
             if (
                 not nome_usuario or not perfil or not senha
             ):
                 return render_template(
                     "html_usuarios/editar.html", usuario=usuario,erro="preencha todos os campos"
                 )
             if senha or confirmar_senha:
               if senha != confirmar_senha:
                 return render_template(
                     "html_usuarios/editar.html",
                     usuario=usuario,
                     erro = "as senhas não coincidem"
                 )
             try:
                 dados_imagem = None
                 if imagem and imagem.filename:
                    dados_imagem = self.imagem_service.validar(imagem)
                 self.usuario_service.atualizar(
                  usuario_id=usuario_id,
                  nome=nome_usuario,
                  perfil=perfil,
                  senha=senha,
                  imagem=dados_imagem
             )
             except ValueError as e:
                 return render_template("html_usuarios/editar.html",usuario=usuario,erro=str(e))
             return  redirect(url_for("usuarios"))
         return render_template(
             "html_usuarios/editar.html",usuario=usuario
         )
    
    def excluir(self,usuario_id):
        try:
            self.usuario_service.excluir(usuario_id)
        except ValueError as e:
            return str(e), 404
        
        return redirect(url_for("usuarios"))
    
    def confirmar_exclusao(self):
         pass
    def editar_perfil(self):
        usuario_id = session.get("usuario_id")
        usuario = self.usuario_service.buscar_por_id(
            usuario_id
        )


        if not usuario:

            return "Usuário não encontrado", 404


        if request.method == "POST":

            nome_usuario = request.form.get("nome")

            senha = request.form.get("senha")

            confirmar_senha = request.form.get(
                "confirmar_senha"
            )


            if not nome_usuario:

                return render_template(
                    "html_usuarios/editar_perfil.html",
                    usuario=usuario,
                    erro="Preencha todos os campos."
                )


            if senha or confirmar_senha:

                if senha != confirmar_senha:

                    return render_template(
                        "html_usuarios/editar_perfil.html",
                        usuario=usuario,
                        erro="As senhas não coincidem."
                    )
            # 06/10/2026
            imagem = request.files.get("imagem")
           
            try:
                dados_imagem = None

                if imagem and imagem.filename:

                    dados_imagem = self.imagem_service.validar(imagem)

                self.usuario_service.atualizar_perfil(
                    usuario_id=usuario_id,
                    usuario=nome_usuario,
                    senha=senha,
                    #06/10/2026
                    imagem=dados_imagem
                    
                )


                alteracoes = []


                if usuario[1] != nome_usuario:

                    alteracoes.append(
                        f"Usuário alterado de "
                        f"'{usuario[1]}' para "
                        f"'{nome_usuario}'"
                    )


                if senha:

                    alteracoes.append(
                        "Senha alterada"
                    )

                #06/10/2026
                if dados_imagem:
                    alteracoes.append(f"Imagem alterada para '{dados_imagem['nome']}'")
               
                if alteracoes:

                    descricao = "; ".join(
                        alteracoes
                    )


                    self.auditoria_service.registrar(

                        usuario_id=session.get(
                            "usuario_id"
                        ),

                        acao="ALTERACAO",

                        entidade="USUARIO",

                        entidade_id=usuario_id,

                        descricao=descricao,

                        ip=request.remote_addr
                    )


            except ValueError as e:

                return render_template(
                    "html_usuarios/editar_perfil.html",
                    usuario=usuario,
                   
                    erro=str(e)
                )


            return redirect("/")

        usuario = list(usuario)
        usuario[2] = usuario[2].strftime("%Y-%m-%d")
        return render_template("html_usuarios/editar_perfil.html", usuario=usuario,)
    def imagem_perfil(self):
        usuario_id = session.get("usuario_id")

        if not usuario_id:
            return "usuario não autenticado", 401
        
        imagem = self.usuario_service.buscar_imagem(
            usuario_id
        )

        if not imagem:
            return "imagem não encontrada", 404
        
        nome = imagem[0]
        tipo = imagem[1]
        dados_base64 = imagem[2]

        try:
            dados = base64.b64decode(
                dados_base64
            )
        except Exception:
            return "imagem inválida", 500
        
        return Response(
            dados,
            mimetype = tipo,
            headers={
                "content-Disposition":
                 f'inline; filename="{nome}"'
            }
        )
    def imagem_usuario(self,usuario_id):
        imagem = self.usuario_service.buscar_imagem(usuario_id)

        if not imagem:
            return "imagem não encontrada", 404
        
        nome = imagem[0]
        tipo = imagem[1]
        dados_base64 = imagem[2]

        if not dados_base64:
            return "imagem não encontrada", 404
        
        try:
            if isinstance(dados_base64, str): dados = base64.b64decode(dados_base64, validate=True)
            else:
                dados = dados_base64
        except Exception:
            return "imagem inválida", 500
        
        return Response(
            dados,
            mimetype=tipo,
            headers={
                "content-disposition":
                 f'inline; filename="{nome}"'
            }
        )