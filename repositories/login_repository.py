class LoginRepository:
    def __init__(self,banco):
        self.db = banco
    
    def registrar_login(self,usuario_id):
        self.db.executar(
            """
             INSERT INTO logins (usuario_id) VALUES (%s)
            """,(usuario_id,)
        )