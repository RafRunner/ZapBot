import planilha


class InformacaoAdicionalASerObtida:

    def __init__(self, coluna, nome_coluna, funcao_substituicao, inverter_substituicao=False):
        self.coluna = planilha.trata_coluna(coluna)
        self.nome_coluna = nome_coluna
        self.funcao_substituicao = funcao_substituicao
        self.valor = []
        self.deve_substituir = []
        self.inverter_substituicao = inverter_substituicao

    def get_deve_substituir_linha(self, indice):
        deve_substituir = False
        if len(self.deve_substituir) > indice:
            deve_substituir = self.deve_substituir[indice]

        if self.inverter_substituicao:
            deve_substituir = not deve_substituir

        return deve_substituir

    def get_valor_linha(self, indice):
        if len(self.valor) > indice:
            return self.valor[indice]
        else:
            return ''


class InformacaoAdicionalEspecifica:

    def __init__(self, info_adicional, indice):
        self.coluna = info_adicional.coluna
        self.nome_coluna = info_adicional.nome_coluna
        self.indice = indice
        self.todas_informacoes_especificas = []

        deve_substituir = info_adicional.get_deve_substituir_linha(indice)
        self.valor = info_adicional.get_valor_linha(indice)

        self.substituicao_efetiva = self.formata_substituicao(deve_substituir, info_adicional.funcao_substituicao)

    def formata_substituicao(self, deve_substituir, funcao_substituicao):
        if deve_substituir:
            return funcao_substituicao(self)
        else:
            return ''

    def encontra_informacao_por_nome(self, nome):
        for info_especifica in self.todas_informacoes_especificas:
            if info_especifica.nome_coluna == nome:
                return info_especifica

        return None
