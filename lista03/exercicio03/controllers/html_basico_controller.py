from controllers.base_controller import BaseController
from flask import render_template

class HTMLbasicoController(BaseController):
    def __init__(self,app):
        self.rotas = [
            ('/','home',self.pagina_inicial),
            ('/listas','listas',self.pagina_listas)
        ]
        super().__init__(app)

    def pagina_inicial(self):
        return render_template("pagina_inicial.html")
    
    def pagina_listas(self):
        return render_template("pagina_listas.html")