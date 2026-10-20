

class BancoTabelas:
    def __init__(self,banco):
        self.banco = banco

    def criar_tabelas(self):
        self.criar_tabela_usuarios()
    
    def criar_tabela_usuarios(self):
        self.banco.executar("""
          CREATE TABLE IF NOT EXISTS usuarios (
         id INT AUTO_INCREMENT PRIMARY KEY,
         email VARCHAR(255) NOT NULL,
         senha VARCHAR(255) NOT NULL,
         perfil VARCHAR(50) NOT NULL DEFAULT 'usuario'
           )
       """)