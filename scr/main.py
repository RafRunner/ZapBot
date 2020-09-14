from planilha import Planilha
from info_adicional import InformacaoAdicionalASerObtida
import enviador

nome_planilha = 'Teste bot'
numero_sheet = 0
linha_inicial = 4
linha_final = 4
coluna_nome = 'C'
coluna_numero = 'B'
coluna_check = 'E'

infos_adicionais = [InformacaoAdicionalASerObtida('D', 'CaminhoArquivo', lambda info: info.valor)]
infos_adicionais = [InformacaoAdicionalASerObtida('D', 'CaminhoArquivo', lambda info: info.valor)]


def funcao_deve_enviar(pessoa):
    return True


nome_arquivo_resultado = 'teste bot arquivos'


planilha = Planilha(nome_planilha, numero_sheet, linha_inicial, linha_final, coluna_nome, coluna_numero, coluna_check,
                    infos_adicionais, funcao_deve_enviar)


mensagens = ['Essa é uma mensagem de teste', 'C:\\Users\\rafae\\Pictures\\stickbug.jpg', '%CaminhoArquivo']

enviador.enviar_mensagens_com_informacoes_planilha(planilha, mensagens, nome_arquivo_resultado)
