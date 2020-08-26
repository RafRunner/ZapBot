from oauth2client.service_account import ServiceAccountCredentials
from pessoa import Pessoa
from info_adicional import InformacaoAdicionalEspecifica

import gspread
import formatador


def trata_coluna(nome_coluna):
    return ord(nome_coluna.lower()) - 96


def normaliza_tamanho_colunas(nomes, numeros, enviados):
    while len(numeros) < len(nomes):
        numeros.append('')
    while len(enviados) < len(nomes):
        enviados.append(False)


class Planilha:

    def __init__(self, nome_planilha, numero_sheet, linha_inicial, linha_final, coluna_nomes, coluna_numeros,
                 coluna_enviado, infos_adicionais=None, funcao_deve_enviar=None):

        scope = ['https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json", scope)
        client = gspread.authorize(creds)

        planilha = client.open(nome_planilha)
        self.sheet = planilha.worksheets()[numero_sheet]

        self.linha_inicial = linha_inicial - 1
        self.linha_final = linha_final
        self.coluna_nomes = trata_coluna(coluna_nomes)
        self.coluna_numeros = trata_coluna(coluna_numeros)
        self.coluna_enviado = trata_coluna(coluna_enviado)
        self.infos_adicionais = infos_adicionais
        self.funcao_deve_enviar = funcao_deve_enviar

    def get_valores_coluna(self, coluna):
        return self.sheet.col_values(coluna)[self.linha_inicial:self.linha_final]

    def __carrega_informacoes_adicionais(self):
        if self.infos_adicionais is None:
            self.infos_adicionais = []
            return

        for info in self.infos_adicionais:
            info.valores = self.get_valores_coluna(info.coluna)
            info.devem_substituir = list(map(formatador.parse_verdadeiro_falso, info.valores))

    def __get_informacoes_adicionais_especificas(self, indice):
        infos_especificas = []
        for info in self.infos_adicionais:
            infos_especificas.append(InformacaoAdicionalEspecifica(info, indice))

        for info_especifica in infos_especificas:
            info_especifica.todas_informacoes_especificas = infos_especificas

        return infos_especificas

    def get_pessoas(self):
        pessoas = []
        invalidos = []

        nomes = self.get_valores_coluna(self.coluna_nomes)
        numeros = self.get_valores_coluna(self.coluna_numeros)
        enviados = self.get_valores_coluna(self.coluna_enviado)

        normaliza_tamanho_colunas(nomes, numeros, enviados)

        numeros_tratados = []
        for numero in numeros:
            try:
                numero_tratado = formatador.formatar_numero_goiania_brasil(numero)
                numeros_tratados.append(numero_tratado)
                invalidos.append(False)

            except formatador.NumeroInvalido:
                numeros_tratados.append(numero)
                invalidos.append(True)

        enviados_booleanos = list(map(formatador.parse_verdadeiro_falso, enviados))

        self.__carrega_informacoes_adicionais()

        for i in range(0, len(nomes)):
            infos_adicionais_especificas = self.__get_informacoes_adicionais_especificas(i)

            deve_enviar = not enviados_booleanos[i]

            pessoa = Pessoa(self.linha_inicial + i + 1, nomes[i], numeros_tratados[i], deve_enviar, invalidos[i],
                            infos_adicionais_especificas)

            if deve_enviar and self.funcao_deve_enviar is not None:
                pessoa.deve_enviar = self.funcao_deve_enviar(pessoa)

            pessoas.append(pessoa)

        return pessoas

    def marca_como_enviado(self, pessoa):
        linha = pessoa.linha
        self.sheet.update_cell(linha, self.coluna_enviado, 'True')

