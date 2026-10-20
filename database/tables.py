import bcrypt

class BancoTabelas:
    def __init__(self,banco):
        self.banco = banco

    def criar_tabelas(self):
        self.criar_tabela_usuarios()
        self.criar_tabela_auditoria()
        self.usuario_admin()
        self.criar_tabela_logins()

    def criar_tabela_usuarios(self):
        self.banco.executar("""
           CREATE TABLE IF NOT EXISTS usuarios (
             id INT AUTO_INCREMENT PRIMARY KEY,
             nome VARCHAR(255) NOT NULL,
             senha VARCHAR(255) NOT NULL,
             perfil VARCHAR(50) NOT NULL DEFAULT 'usuario'
           )
        """)

    def criar_tabela_auditoria(self):
        self.banco.executar("""
            CREATE TABLE IF NOT EXISTS auditoria (
             id INT AUTO_INCREMENT PRIMARY KEY,
             usuario_id INT NULL,
             acao VARCHAR(50) NOT NULL,
             entidade VARCHAR(50) NOT NULL,
             entidade_id INT NULL,
             descricao VARCHAR(255),
             ip VARCHAR(45),
             data_hora DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
             FOREIGN KEY (usuario_id)          
                REFERENCES usuarios(id)
                ON DELETE SET NULL
            )
        """)

    def usuario_admin(self):
        resultado = self.banco.consultar_um(
            """SELECT id FROM usuarios WHERE perfil = %s""",
            ("administrador",)
        )

        if not resultado:
            senha_hash = bcrypt.hashpw("12345".encode(),bcrypt.gensalt()).decode()

            self.banco.executar(
                """
                INSERT INTO usuarios(
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
                    "admin@gmail.com",
                    senha_hash,
                    "administrador"
                )
            )

    def criar_tabela_logins(self):
        self.banco.executar("""
          CREATE TABLE IF NOT EXISTS logins (
                            
            id INT AUTO_INCREMENT PRIMARY KEY,
            usuario_id INT NOT NULL,
            data_hora TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (usuario_id)
                REFERENCES usuarios(id)
                ON DELETE CASCADE
          )
    
    """)