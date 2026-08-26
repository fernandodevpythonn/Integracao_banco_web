import bcrypt

class BancoTabelas:
    def __init__(self,banco):
        self.banco = banco

    def criar_tabelas(self):
        self.criar_tabela_usuarios()
        self.criar_tabela_ratelimit()
    
    def criar_tabela_usuarios(self):
        self.banco.executar("""
           CREATE TABLE IF NOT EXISTS usuarios (
             id INT AUTO_INCREMENT PRIMARY KEY,
             email VARCHAR(255) NOT NULL,
             senha VARCHAR(255) NOT NULL,
             perfil VARCHAR(50) NOT NULL DEFAULT 'usuario'            
        )
    """)
        
    def criar_tabela_ratelimit(self):
        self.banco.executar("""
         CREATE TABLE IF NOT EXISTS ratelimit (
           id INT AUTO_INCREMENT PRIMARY KEY,
           usuario_id INT NULL,
           ip VARCHAR(45) NOT NULL,
           rota VARCHAR(10) NOT NULL,
           metodo VARCHAR(10) NOT NULL,
           limite VARCHAR(50) NOT NULL,
           data_hora DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
           motivo VARCHAR(255) NOT NULL,
           FOREIGN KEY (usuario_id)
              REFERENCES usuarios(id)               
              ON DELETE SET NULL
        )
    """)