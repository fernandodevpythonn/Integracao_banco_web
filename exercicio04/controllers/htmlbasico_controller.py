from controllers.base_controller import BaseController
from flask import render_template

class HTMLbasicoController(BaseController):
  def __init__(self,app):
    self.rotas = [
        ('/','home',self.pagina_inicial),
        ('/tabelas','tabelas',self.pagina_tabelas)
    ]
    super().__init__(app)

  def pagina_inicial(self):
    return render_template("pagina_inicial.html")
  
  def pagina_tabelas(self):
    return render_template("pagina_tabelas.html")