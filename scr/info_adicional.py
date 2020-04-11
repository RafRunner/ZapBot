import planilha


def encontra_informacao_por_nome(todas_informacoes, nome):
    for info in todas_informacoes:
        if info.nome_coluna == nome:
            return info

    return None


class InformacaoAdicionalASerObtida:

    def __init__(self, coluna, nome_coluna, funcao_substituicao, inverter_check=False):
        self.coluna = planilha.trata_coluna(coluna)
        self.nome_coluna = nome_coluna
        self.funcao_substituicao = funcao_substituicao
        self.valor = []
        self.deve_substituir = []
        self.inverter_check = inverter_check

    def get_deve_substituir_linha(self, indice):
        if len(self.deve_substituir) > indice:
            return self.deve_substituir[indice]
        else:
            return False

    def get_valor_linha(self, indice):
        if len(self.valor) > indice:
            return self.valor[indice]
        else:
            return ''


class InformacaoAdicionalEspecifica:

    def __init__(self, info_adicional, indice, todas_informacoes):
        self.coluna = info_adicional.coluna
        self.nome_coluna = info_adicional.nome_coluna
        self.indice = indice

        deve_substituir = info_adicional.get_deve_substituir_linha(indice)
        self.valor = info_adicional.get_valor_linha(indice)

        self.substituicao_efetiva = self.formata_substituicao(deve_substituir, info_adicional.funcao_substituicao, todas_informacoes)

    # result deve ser preenchido internamente pela função de substituição e deve ser uma string. Nela estão disponíveis
    # todas as variáveis disponíveis localemnte nessa função (claro né hu3)
    def formata_substituicao(self, deve_substituir, funcao_substituicao, todas_informacoes):
        if deve_substituir:
            exec('global result; %s' % funcao_substituicao)
            global result
            return result
        else:
            return ''
