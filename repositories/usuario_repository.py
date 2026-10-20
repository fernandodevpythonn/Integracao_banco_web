from database.connection import BancoMysql

class UsuarioRepository:
    def __init__(self,banco):
        self.db = banco
    
    def buscar_por_usuario(self,nome):
        return self.db.consultar_um(
         """
         SELECT 
           id,
           nome,
           senha,
           perfil
         FROM usuarios
         WHERE nome = %s
         """,(nome,)
        )
    
    def buscar_por_id(self,usuario_id):
        return self.db.consultar_um(
        """
          SELECT 
            id,
            nome,
            perfil
          FROM usuarios
          WHERE id = %s
        """, (usuario_id,)
        )
    
    def listar_todos(self):
        return self.db.consultar(
         """
         SELECT 
           id,
           nome,
           senha,
           perfil
         FROM usuarios
         ORDER BY id
         """
        )
    
    def criar(self,nome,senha_hash,perfil):
        self.db.executar(
            """
            INSERT INTO usuarios
            (
               nome,
               senha,
               perfil
            )
            VALUES
            (
              %s,
              %s,
              %s
            )
            """,
            (
                 nome,
                 senha_hash,
                 perfil
            )
        )
        return self.db.cursor.lastrowid
    
    def existe(self,nome):
        resultado = self.db.consultar_um(
            """
            SELECT id
            FROM usuarios
            WHERE nome = %s
            """,(nome,)
        )
        return resultado is not None
  
    def excluir(self,usuario_id):
        self.db.executar(
            """
            DELETE FROM usuarios
            WHERE id = %s
            """,(usuario_id,)
        )