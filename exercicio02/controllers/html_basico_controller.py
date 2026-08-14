from controllers.base_controller import BaseController
from flask import render_template
class HTMLbasicocontroller(BaseController):

    def __init__(self,app):
        self.rotas = [
            ('/', 'home', self.pagina_inicial),
            ('/divs','divs', self.pagina_divs)
        ]
        super().__init__(app)
    
    def pagina_inicial(self):
        return render_template("pagina_inicial.html")
    def pagina_divs(self):
        return render_template("pagina_divs_spans.html")