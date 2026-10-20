class AuditoriaRepository:
    def __init__(self,banco):
        self.db = banco

    def registrar(self,usuario_id,acao,entidade,entidade_id=None,descricao=None,ip=None):
        self.db.executar(
            """
            INSERT INTO auditoria
            (
              usuario_id,
              acao,
              entidade,
              entidade_id,
              descricao,
              ip
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
                acao,
                entidade,
                entidade_id,
                descricao,
                ip
            )
        )
    
    def listar(
        self,
        acao=None,
        entidade=None,
        usuario_id=None
    ):

        sql = """
            SELECT
                a.id,
                a.usuario_id,
                u.nome,
                a.acao,
                a.entidade,
                a.entidade_id,
                a.descricao,
                a.ip,
                a.data_hora

            FROM auditoria a

            LEFT JOIN usuarios u
                ON u.id = a.usuario_id

            WHERE 1 = 1
        """

        parametros = []


        if acao:

            sql += """
                AND a.acao = %s
            """

            parametros.append(acao)


        if entidade:

            sql += """
                AND a.entidade = %s
            """

            parametros.append(entidade)


        if usuario_id:

            sql += """
                AND a.usuario_id = %s
            """

            parametros.append(usuario_id)


        sql += """
            ORDER BY a.data_hora DESC
        """


        resultados = self.db.consultar(
            sql,
            tuple(parametros)
        )


        auditorias = []


        for resultado in resultados:

            auditoria = {

                "id": resultado[0],

                "usuario_id": resultado[1],

                "nome": resultado[2],

                "acao": resultado[3],

                "entidade": resultado[4],

                "entidade_id": resultado[5],

                "descricao": resultado[6],

                "ip": resultado[7],

                "data_hora": resultado[8]

            }

            auditorias.append(auditoria)

        return auditorias
