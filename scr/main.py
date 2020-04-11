import errno

from bot import ZapBot
from bot import NumeroNaoEncontrado
from planilha import Planilha
from formatador import formatar_mensagens
from info_adicional import InformacaoAdicionalASerObtida

import time
import os

pasta_resultados = 'resultados'

try:
    os.makedirs(pasta_resultados)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise e

mensagens = ['Boa noite, %nome! Aqui é o Rafael Santana do CAWEM',
             'Então, devido a quarentena e a paralisação de aulas estamos aumentando o prazo para pagamento dos produtos do CA, antes o prazo era até dia 29, porém como também iremos demorar mais para poder entregar os produtos, estamos aumentando o prazo de pagamento até o fim de Abril. Conto com sua compreensão',
             'Caso desista do pedido ou quiser alterar ele, entre em contato comigo']

nome_planilha = 'Produtos CA'
numero_sheet = 0
linha_inicial = 3
linha_final = 105
coluna_nome = 'A'
coluna_numero = 'B'
coluna_check = 'O'

nome_arquivo_resultado = os.path.join(pasta_resultados, 'resultado envio aumento do prazo produtos CA')


def get_string_quantidade(nome_produto):
    return """quantidade = 1
if self.valor[0].lower() != "x":
    quantidade = self.valor[0]
    
nome_produto = "{}"

result = "0{} x {}".format(str(quantidade), nome_produto)
""".format(nome_produto, '{}', '{}', '{}')


# infos_adicionais = [InformacaoAdicionalASerObtida('C', 'CamisaLovelace', get_string_quantidade('Camisa Lovelace')),
#                     InformacaoAdicionalASerObtida('D', 'CamisaTEscuro', get_string_quantidade('Camisa Circuito Escuro')),
#                     InformacaoAdicionalASerObtida('E', 'Sacochila', get_string_quantidade('Sacochila')),
#                     InformacaoAdicionalASerObtida('F', 'Carteirinha', get_string_quantidade('Carteirinha')),
#                     InformacaoAdicionalASerObtida('G', '3Adesivos', get_string_quantidade('3 Adesivos')),
#                     InformacaoAdicionalASerObtida('I', 'ValorTotal', 'result = "Valor total: {}".format(self.valor)')]

planilha = Planilha(nome_planilha, numero_sheet, linha_inicial, linha_final, coluna_nome, coluna_numero, coluna_check)
pessoas = planilha.get_informacoes()

zap_bot = ZapBot.instance()
resultado = open(nome_arquivo_resultado + '.txt', 'a')

try:
    resultado.write('\n\n///////////////////////////////////////////Inicio de uma nova execução de envio!!//////////////////////////////////////////////////////\n\n')

    resultado.write('mensagens enviadas:\n')

    for mensagem in mensagens:
        resultado.write('#' + mensagem + '\n')

    resultado.write('\n')

    for pessoa in pessoas:
        if pessoa.invalido:
            resultado.write(str(pessoa))
            resultado.write('FALHA! Mensagens não enviada para a pessoa acima por estar com o número inválido\n\n')
            continue

        if pessoa.check:
            continue

        try:
            mensagens_formatadas = formatar_mensagens(mensagens, pessoa, pessoa.infos_adicionais)
            zap_bot.enviar_mensagens(pessoa.numero, mensagens_formatadas)
            planilha.check_pessoa(pessoa)
            resultado.write(str(pessoa))
            resultado.write('SUCESSO! Mensagens enviada para a pessoa acima com sucesso\n\n')
            time.sleep(2)

        except NumeroNaoEncontrado:
            resultado.write(str(pessoa))
            resultado.write('FALHA! Mensagens não enviada para a pessoa acima porque o número não foi encontrado\n\n')

except Exception as err:
    resultado.write('\nERRO CRÍTICO! A execução teve que ser interrompida por uma exception:' + str(err))
finally:
    resultado.close()
    zap_bot.close()

