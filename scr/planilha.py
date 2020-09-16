from typing import *
from oauth2client.service_account import ServiceAccountCredentials
from pessoa import Pessoa
from info_adicional import InformacaoAdicionalEspecifica
from info_adicional import InformacaoAdicionalASerObtida

import gspread
import formatador


def trata_coluna(nome_coluna: str) -> int:
    return ord(nome_coluna.lower()) - 96


def normaliza_tamanho_colunas(nomes, numeros, enviados) -> None:
    while len(numeros) < len(nomes):
        numeros.append('')
    while len(enviados) < len(nomes):
        enviados.append(False)


class Planilha(object):

    def __init__(self, nome_planilha: str, numero_sheet: int, linha_inicial: int, linha_final: int, coluna_nomes: str, coluna_numeros: str, coluna_enviado: str,
                 infos_a_serem_obtidas: List[InformacaoAdicionalASerObtida], funcao_deve_enviar: Callable[[Pessoa], bool]):

        scope = ['https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json", scope)
        client = gspread.authorize(creds)

        planilha = client.open(nome_planilha)
        self.sheet = planilha.worksheets()[numero_sheet]

        self.linha_inicial: int = linha_inicial - 1
        self.linha_final: int = linha_final
        self.coluna_nomes: int = trata_coluna(coluna_nomes)
        self.coluna_numeros: int = trata_coluna(coluna_numeros)
        self.coluna_enviado: int = trata_coluna(coluna_enviado)
        self.infos_a_serem_obtidas: Optional[List[InformacaoAdicionalASerObtida]] = infos_a_serem_obtidas
        self.funcao_deve_enviar: Optional[Callable[[Pessoa], bool]] = funcao_deve_enviar

    def get_valores_coluna(self, coluna: int) -> List[str]:
        return self.sheet.col_values(coluna)[self.linha_inicial:self.linha_final]

    def __carrega_informacoes_adicionais(self) -> None:
        for info in self.infos_a_serem_obtidas:
            info.valores = self.get_valores_coluna(info.coluna)

    def __get_informacoes_adicionais_especificas(self, indice: int) -> List[InformacaoAdicionalEspecifica]:
        infos_especificas = []
        for info in self.infos_a_serem_obtidas:
            infos_especificas.append(InformacaoAdicionalEspecifica(info, indice))

        return infos_especificas

    def get_pessoas(self) -> List[Pessoa]:
        pessoas: List[Pessoa] = []
        invalidos: List[bool] = []

        nomes: List[str] = self.get_valores_coluna(self.coluna_nomes)
        numeros: List[str] = self.get_valores_coluna(self.coluna_numeros)
        enviados: List[str] = self.get_valores_coluna(self.coluna_enviado)

        normaliza_tamanho_colunas(nomes, numeros, enviados)

        numeros_tratados: List[str] = []
        for numero in numeros:
            try:
                numero_tratado: str = formatador.formatar_numero_goiania_brasil(numero)
                numeros_tratados.append(numero_tratado)
                invalidos.append(False)

            except formatador.NumeroInvalido:
                numeros_tratados.append(numero)
                invalidos.append(True)

        enviados_booleanos: List[bool] = list(map(formatador.parse_verdadeiro_falso, enviados))

        self.__carrega_informacoes_adicionais()

        for i in range(0, len(nomes)):
            infos_adicionais_especificas: List[InformacaoAdicionalEspecifica] = self.__get_informacoes_adicionais_especificas(i)

            deve_enviar: bool = not enviados_booleanos[i]

            pessoa: Pessoa = Pessoa(self.linha_inicial + i + 1, nomes[i], numeros_tratados[i], deve_enviar, invalidos[i], infos_adicionais_especificas)

            if deve_enviar and self.funcao_deve_enviar is not None:
                pessoa.deve_enviar = self.funcao_deve_enviar(pessoa)

            pessoas.append(pessoa)

        return pessoas

    def marca_como_enviado(self, pessoa: Pessoa) -> None:
        self.sheet.update_cell(pessoa.linha, self.coluna_enviado, 'True')
