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