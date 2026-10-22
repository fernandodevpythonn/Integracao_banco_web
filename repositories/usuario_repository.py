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
    def atualizar(self,usuario_id,nome,perfil,senha_hash=None):
        if senha_hash:
            self.db.executar(
                """
                UPDATE usuarios
                SET
                  nome = %s,
                  senha = %s,
                  perfil = %s
                WHERE id = %s
                """,
                (
                    nome,
                    senha_hash,
                    perfil,
                    usuario_id
                )
            )
        else:
            self.db.executar(
                """
                UPDATE usuarios
                SET
                   nome = %s,
                   perfil = %s
                WHERE id = %s
                """,
                (
                    nome,
                    perfil,
                    usuario_id
                )
            )
    def salvar_imagem(self,usuario_id,imagem):
        self.db.executar(
            """
            INSERT INTO imagens
            (
              usuario_id,
              nome,
              tipo,
              formato,
              tamanho_original,
              dados
            )
            VALUES
            (
              %s,
              %s,
              %s,
              %s,
              %s,
              %s
            )
            ON DUPLICATE KEY UPDATE
              nome = VALUES(nome),
              tipo = VALUES(tipo),
              formato = VALUES(formato),
              tamanho_original = VALUES(tamanho_original),
              dados = VALUES(dados),
              data_hora = CURRENT_TIMESTAMP
            """,
            (
                usuario_id,
                imagem["nome"],
                imagem["tipo"],
                imagem["formato"],
                imagem["tamanho_original"],
                imagem["dados"]
            )
        )
    def buscar_imagem(self,usuario_id):
        return self.db.consultar_um(
            """
            SELECT
              nome,
              tipo,
              dados
            FROM imagens
            WHERE usuario_id = %s
            """,(usuario_id,)
        )