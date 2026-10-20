from flask import render_template
from controllers.base_controller import BaseController
class basico_controller(BaseController):
    def __init__(self,app):
        self.rotas = [
            ('/','home',self.proteger_rota(self.pagina_inicial))
        ]
        super().__init__(app)

    def pagina_inicial(self):
        return render_template("usuarios_pagina.html")
