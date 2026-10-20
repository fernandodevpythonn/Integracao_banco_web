class RateLimitRepository:
    def __init__(self,banco):
        self.db = banco
    
    def registrar_bloqueio(self, usuario_id = None, ip = None, rota = None, metodo = None, limite = None, motivo = None):
        self.db.executar(
            """
            INSERT INTO ratelimit
            (
              usuario_id,
              ip,
              rota,
              metodo,
              limite,
              motivo
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
            """,
            (
                usuario_id,
                ip,
                rota,
                metodo,
                limite,
                motivo
            )
        )