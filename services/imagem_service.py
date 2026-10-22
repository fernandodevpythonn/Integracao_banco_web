from PIL import Image
import os
import base64

class ImagemService:
    TIPOS_PERMITIDOS = {
        "image/jpeg": "jpg",
        "image/png": "png",
        "image/webp": "webp"
    }

    TAMANHO_MAXIMO = 5 * 1024 * 1024

    def validar(self,arquivo):
        if not arquivo:
         raise ValueError(
            "nenhuma imagem foi enviada"
         )
        if not arquivo.filename:
           raise ValueError(
              "selecione uma imagem"
           )
        tipo = arquivo.content_type

        print("Nome:", arquivo.filename)
        print("Tipo:", tipo)


        if tipo not in self.TIPOS_PERMITIDOS:

            raise ValueError(
                "Formato de imagem não permitido. "
                "Use JPG, PNG ou WEBP."
            )


        dados = arquivo.read()


        if not dados:

            raise ValueError(
                "A imagem está vazia."
            )


        tamanho = len(dados)


        if tamanho > self.TAMANHO_MAXIMO:

            raise ValueError(
                "A imagem deve ter no máximo 5 MB."
            )


        dados_base64 = base64.b64encode(
            dados
         ).decode("utf-8")


        formato = self.TIPOS_PERMITIDOS[tipo]


        return {

            "nome": arquivo.filename,

            "tipo": tipo,

            "formato": formato,

            "tamanho_original": tamanho,

            "dados": dados_base64

         }
