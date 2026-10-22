import bcrypt

class UsuarioService:
    def __init__(self,repository):
        self.repository = repository

    def autenticar(self, nome, senha):
        resultado = self.repository.buscar_por_usuario(
            nome
        )

        if not resultado:
            return None
        
        usuario_id = resultado[0]
        nome_usuario = resultado[1]
        senha_hash = resultado[2]
        perfil = resultado[3]

        senha_valida = bcrypt.checkpw(senha.encode(),senha_hash.encode())
        
        if not senha_valida:
            return None
        
        return {
            "id": usuario_id,
            "nome": nome_usuario,
            "perfil": perfil
        }
    
    def gerar_senha_hash(self,senha):
        self.validar_senha(senha)

        return bcrypt.hashpw(senha.encode(),bcrypt.gensalt()).decode()

    def cadastrar(self,nome,senha,perfil="usuario"):
        if self.repository.existe(nome):
            raise ValueError("usuário já existe")
         
        senha_hash = self.gerar_senha_hash(senha)
        
        return self.repository.criar(
            nome = nome,
            senha_hash = senha_hash,
            perfil = perfil
        )
    def validar_senha(self, senha):

        if len(senha) < 8:

            raise ValueError(
                "A senha deve ter no mínimo 8 caracteres."
            )


        if not any(
            caractere.isupper()
            for caractere in senha
        ):

            raise ValueError(
                "A senha deve conter pelo menos uma letra maiúscula."
            )


        if not any(
            caractere.isdigit()
            for caractere in senha
        ):

            raise ValueError(
                "A senha deve conter pelo menos um número."
            )


        if not any(
            not caractere.isalnum()
            for caractere in senha
        ):

            raise ValueError(
                "A senha deve conter pelo menos um caractere especial."
            )
    def listar_todos(self):
        return self.repository.listar_todos()
    
    def excluir(self,usuario_id):
        usuario = self.repository.buscar_por_id(usuario_id)
        if not usuario:
            raise ValueError("Usuário não encontrado.")
        
        self.repository.excluir( usuario_id)

    def buscar_por_id(self,usuario_id):
         return self.repository.buscar_por_id(usuario_id)

    def atualizar(self,usuario_id,nome,perfil,senha=None,imagem=None):
        senha_hash = None

        if senha:
            senha_hash = self.gerar_senha_hash(senha)

        self.repository.atualizar(
            usuario_id=usuario_id,
            nome = nome,
            perfil = perfil,
            senha_hash = senha_hash,
        )

        if imagem:
            self.repository.salvar_imagem(
                usuario_id=usuario_id,
                imagem=imagem
            )
    