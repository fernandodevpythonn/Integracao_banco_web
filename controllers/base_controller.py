from flask import session,redirect,url_for,abort
from functools import wraps

class BaseController:
    def __init__(self,app):
        self.app = app
        if hasattr(self,'rotas'):
            self.registrar_rotas()
        
    def registrar_rotas(self):
        for rota in self.rotas:
            if len(rota) == 3:
                endereco_url,nome_rota,funcao_resposta = rota
                self.app.add_url_rule(endereco_url,nome_rota,funcao_resposta)
            elif len(rota) == 4:
                endereco_url,nome_rota,funcao_resposta,metodos = rota
                self.app.add_url_rule(endereco_url,nome_rota,funcao_resposta,methods = metodos)
            elif len(rota) == 5:
                endereco_url,nome_rota,funcao_resposta,metodos, perfil = rota
                funcao_protegida = self.proteger_rota(funcao_resposta,perfil)
                self.app.add_url_rule(endereco_url,nome_rota,funcao_protegida,methods = metodos)

    def proteger_rota(self,funcao,perfil = None):
        @wraps(funcao)
        def rota_protegida(*args,**kwargs):
            if not session.get("usuario_logado"):
                return redirect(url_for("paginalogin"))
            if perfil is not None:
                if session.get("perfil_logado") != perfil:abort(403)
            return funcao(*args,**kwargs)
        return rota_protegida