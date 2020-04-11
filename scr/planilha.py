from oauth2client.service_account import ServiceAccountCredentials
from pessoa import Pessoa
from info_adicional import InformacaoAdicionalEspecifica

import gspread
import formatador


def trata_coluna(nome_coluna):
    return ord(nome_coluna.lower()) - 96


def normaliza_tamanho_colunas(nomes, numeros, checks):
    while len(numeros) < len(nomes):
        numeros.append('')
    while len(checks) < len(nomes):
        checks.append(False)


class Planilha:

    def __init__(self, nome_planilha, numero_sheet, linha_inicial, linha_final, coluna_nomes, coluna_numeros, coluna_check, infos_adicionais=None, inverter_check=False):
        scope = ['https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json", scope)
        client = gspread.authorize(creds)

        self.planilha = client.open(nome_planilha)
        self.sheet = self.planilha.worksheets()[numero_sheet]

        self.linha_inicial = linha_inicial - 1
        self.linha_final = linha_final
        self.coluna_nomes = trata_coluna(coluna_nomes)
        self.coluna_numeros = trata_coluna(coluna_numeros)
        self.coluna_check = trata_coluna(coluna_check)
        self.infos_adicionais = infos_adicionais
        self.inverter_check = inverter_check

    def get_valores_coluna(self, coluna):
        return self.sheet.col_values(coluna)[self.linha_inicial:self.linha_final]

    def __carrega_informacoes_adicionais(self):
        if self.infos_adicionais is None:
            self.infos_adicionais = []
            return

        for info in self.infos_adicionais:
            info.valor = self.get_valores_coluna(info.coluna)
            info.deve_substituir = list(map(formatador.parse_verdadeiro_falso, info.valor))

            if info.inverter_check:
                for i in range(0, len(info.deve_substituir)):
                    info.deve_substituir[i] = not info.deve_substituir[i]

    def __get_informacoes_adicionais_especificas(self, indice):
        infos = []
        for info in self.infos_adicionais:
            infos.append(InformacaoAdicionalEspecifica(info, indice, self.infos_adicionais))
        return infos

    def get_informacoes(self):
        info = []
        invalidos = []

        nomes = self.get_valores_coluna(self.coluna_nomes)
        numeros = self.get_valores_coluna(self.coluna_numeros)
        checks = self.get_valores_coluna(self.coluna_check)

        normaliza_tamanho_colunas(nomes, numeros, checks)

        numeros_tratados = []
        for numero in numeros:
            try:
                numero_tratado = formatador.formatar_numero_goiania_brasil(numero)
                numeros_tratados.append(numero_tratado)
                invalidos.append(False)

            except formatador.NumeroInvalido:
                numeros_tratados.append(numero)
                invalidos.append(True)

        checks_booleanos = list(map(formatador.parse_verdadeiro_falso, checks))
        if self.inverter_check:
            for i in range(0, len(checks_booleanos)):
                checks_booleanos[i] = not checks_booleanos[i]

        self.__carrega_informacoes_adicionais()

        for i in range(0, len(nomes)):
            info_adicional_especifica = self.__get_informacoes_adicionais_especificas(i)
            pessoa = Pessoa(self.linha_inicial + i + 1, nomes[i], numeros_tratados[i], checks_booleanos[i], invalidos[i], info_adicional_especifica)
            info.append(pessoa)

        return info

    def check_pessoa(self, pessoa):
        linha = pessoa.linha
        self.sheet.update_cell(linha, self.coluna_check, 'True')

