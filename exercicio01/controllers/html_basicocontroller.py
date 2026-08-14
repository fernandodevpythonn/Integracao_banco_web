from flask import render_template
from controllers.basecontroller import BaseController

class htmlbasicocontroller(BaseController):
    def __init__(self,app):
        self.rotas = [
            ('/','home',self.pagina_inicial)
        ]
        super().__init__(app)
        
    def pagina_inicial(self):
        return render_template("basico_html/pagina_inicial.html")