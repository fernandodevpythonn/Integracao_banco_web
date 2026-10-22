from flask import render_template
from controllers.base_controller import BaseController
class basico_controller(BaseController):
    def __init__(self,app):
        self.rotas = [
            ('/','home',self.proteger_rota(self.pagina_inicial)),
            ('/ex0301',self.proteger_rota(self.pagina_ex0301)),
            ('/ex0302',self.proteger_rota(self.pagina_ex0302)),
            ('/ex0303',self.proteger_rota(self.pagina_ex0303)),
            ('/ex0304',self.proteger_rota(self.pagina_ex0304))
        ]
        super().__init__(app)

    def pagina_inicial(self):
        return render_template("home.html")
    def pagina_ex0301(self):
        return render_template("ex0301.html")
    def pagina_ex0302(self):
        return render_template("ex0302.html")
    def pagina_ex0303(self):
        return render_template("ex0303.html")
    def pagina_ex0304(self):
         return render_template("ex0304.html")