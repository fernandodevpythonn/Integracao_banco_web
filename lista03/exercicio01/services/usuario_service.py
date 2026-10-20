import bcrypt

class UsuarioService:
    def __init__(self,repository):
        def autenticar(self, usuario, senha):
            resultado = self.repository.buscar_por_usuario(
                usuario
            )

            if not resultado:
                return None
            
            usuario_id = resultado[0]
            nome_uruario = resultado[1]
            senha_hash = resultado[2]
            data_nascimento = resultado[3]
            perfil = resultado[4]

            senha_valida = bcrypt.checkpw(
                senha.encode(),
                senha_hash.encode()
            )

            if not senha_valida:
                return None
            
            return {
                "id":usuario_id,
                "usuario": nome_uruario,
                "data_nascimento": data_nascimento,
                "perfil": perfil
            }
        