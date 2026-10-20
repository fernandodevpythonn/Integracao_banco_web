class LoginService:
    def __init__(self,repository):
        self.repository = repository
    
    def registrar_login(self,usuario_id):
        if not usuario_id:
            raise ValueError(
                "id é obrigatório"
            )
        
        self.repository.registrar_login(usuario_id)