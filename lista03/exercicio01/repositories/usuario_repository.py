from database.connection import BancoMySql

class UsuarioRepository:
    def __init__(self,banco):
        self.db = banco
    
    def buscar_por_usuario(self,usuario):
        return self.db.consultar_um(
         """
           SELECT
              id,
              usuario,
              perfil,
              email,
              senha
           FROM usuarios
           WHERE usuarios = %s
         """,
         (usuario,)
        )
    
    def buscar_por_id(self,usuario_id):
        return self.db.consultar_um(
            """
            SELECT 
              id,
              usuario,
              perfil,
              email,
              senha
            FROM usuarios
            WHERE id = %s
            """,
            (usuario_id,)
        )
    
    def listar_todos(self):
        return self.db.consultar(
            """
            SELECT 
              id,
              usuario,
              email,
              senha,
              perfil
            FROM usuarios
            ORDER BY id
            """
        )
    
    def criar(
            self,
            usuario,
            senha_hash,
            email,
            perfil = "usuario"
    ):
        self.db.executar(
            """
            INSERT INTO usuarios
            (
              usuario,
              senha,
              email,
              perfil
            )
            VALUES
            (
              %s,
              %s,
              %s,
              %s
            )
            """,
            (
                usuario,
                senha_hash,
                email,
                perfil
            )
        )