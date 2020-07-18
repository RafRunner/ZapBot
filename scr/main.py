from planilha import Planilha
from info_adicional import InformacaoAdicionalASerObtida
import enviador

nome_planilha = 'Produtos CA'
numero_sheet = 0
linha_inicial = 49
linha_final = 102
coluna_nome = 'A'
coluna_numero = 'B'
coluna_check = 'O'


# def get_funcao_quantidade(nome_produto):
#     def funcao_quantidade(info_adicional_especifica):
#         quantidade = 1
#         if info_adicional_especifica.valor[0].lower() != "x":
#             quantidade = info_adicional_especifica.valor[0]
#
#         return "0{} x {}".format(str(quantidade), nome_produto)
#
#     return funcao_quantidade
#
#
# def funcao_valor_total(info_adicional_especifica):
#     valor = int(str(info_adicional_especifica.valor)[3:len(str(info_adicional_especifica.valor)) - 3])
#
#     carteirinha = info_adicional_especifica.encontra_informacao_por_nome("Carteirinha")
#     if carteirinha is not None and carteirinha.valor != "":
#         valor -= 15
#     return "Valor total: R$ {},00".format(valor)


# infos_adicionais = [InformacaoAdicionalASerObtida('C', 'CamisaLovelace', get_funcao_quantidade('Camisa Lovelace')),
#                     InformacaoAdicionalASerObtida('D', 'CamisaTEscuro', get_funcao_quantidade('Camisa Circuito Escuro')),
#                     InformacaoAdicionalASerObtida('E', 'Sacochila', get_funcao_quantidade('Sacochila')),
#                     InformacaoAdicionalASerObtida('F', 'Carteirinha', get_funcao_quantidade('Carteirinha')),
#                     InformacaoAdicionalASerObtida('G', '3Adesivos', get_funcao_quantidade('3 Adesivos')),
#                     InformacaoAdicionalASerObtida('I', 'ValorTotal', funcao_valor_total)]

infos_adicionais = [InformacaoAdicionalASerObtida('M', 'PrecisaDevolverDinheiro', lambda a: ''),
                    InformacaoAdicionalASerObtida('N', 'CarteirinhaJaDevolvida', lambda a: '')]


def funcao_deve_enviar(info_adicional_especifica):
    precisa_devolver = info_adicional_especifica.encontra_informacao_por_nome('PrecisaDevolverDinheiro').valor == "x"
    ja_devolveu = info_adicional_especifica.encontra_informacao_por_nome('CarteirinhaJaDevolvida').valor == "x"

    return precisa_devolver and not ja_devolveu


planilha = Planilha(nome_planilha, numero_sheet, linha_inicial, linha_final, coluna_nome, coluna_numero, coluna_check,
                    infos_adicionais, funcao_deve_enviar)


mensagens = ['Boa tarde, %nome! Aqui é o Rafael Santana do CAWEM',
             'Estou aqui para avisar que você já fez o pagamento da carteirinha do CA e, como esse ano nem faz sentido mais ter a carteirinha, estamos devolvendo o dinheiro',
             'Para devolução do dinheiro, por favor informar uma conta bancária, ou uma conta do PicPay ou, se possível, gerar um boleto no valor de 15 reais',
             'Obrigado pela atenção!']

nome_arquivo_resultado = 'devolução carteirinha CA'

enviador.enviar_mensagens_com_informacoes_planilha(planilha, mensagens, nome_arquivo_resultado)
