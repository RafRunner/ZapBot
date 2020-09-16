from typing import *

import planilha


class InformacaoAdicionalASerObtida(object):

    # funcao_substituicao: Callable[[InformacaoAdicionalEspecifica, Pessoa], str]
    def __init__(self, coluna: str, nome_info: str, funcao_substituicao: Callable[[object, object], str]):
        self.coluna: int = planilha.trata_coluna(coluna)
        self.nome_info: str = nome_info
        self.funcao_substituicao: Callable[[object, object], str] = funcao_substituicao
        self.valores: List[str] = []

    def get_valor_linha(self, indice: int) -> str:
        if indice < len(self.valores):
            return self.valores[indice]
        else:
            return ''


class InformacaoAdicionalEspecifica(object):

    def __init__(self, info_adicional: InformacaoAdicionalASerObtida, indice: int):
        self.coluna: int = info_adicional.coluna
        self.nome_info: str = info_adicional.nome_info
        # funcao_substituicao: Callable[[InformacaoAdicionalEspecifica, Pessoa], str]
        self.funcao_substituicao: Callable[[object, object], str] = info_adicional.funcao_substituicao

        self.valor: str = info_adicional.get_valor_linha(indice)

    # funcao_substituicao: Callable[[InformacaoAdicionalEspecifica, Pessoa], str]
    def get_substituicao(self, pessoa: object) -> str:
        return self.funcao_substituicao(self, pessoa)
