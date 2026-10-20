from datetime import datetime

class AuditoriaService:
    def __init__(self,repository):
        self.repository = repository

    def registrar(self,usuario_id,acao,entidade,entidade_id=None,descricao=None,ip=None):
        self.repository.registrar(
            usuario_id=usuario_id,
            acao=acao,
            entidade=entidade,
            entidade_id=entidade_id,
            descricao=descricao,
            ip=ip
        )

    def listar(
            self,
            acao=None,
            entidade=None,
            usuario_id=None
    ):
        return self.repository.listar(
            acao=acao,
            entidade=entidade,
            usuario_id=usuario_id
        )
    
    def listar_para_relatorio(
              self,
              acao=None,
              entidade=None,
              usuario_id=None
        ):
         return self.repository.listar(acao,entidade,usuario_id)

