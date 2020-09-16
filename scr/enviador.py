from typing import *
from bot import ZapBot
from bot import NumeroNaoEncontrado
from formatador import formatar_mensagens
from pessoa import Pessoa
from planilha import Planilha

import time
import os
import errno


def enviar_mensagens_com_informacoes_planilha(planilha: Planilha, mensagens: List[str], nome_arquivo_resultado: str):
    pasta_resultados: str = 'resultados'
    arquivo_resultado = os.path.join(pasta_resultados, nome_arquivo_resultado)

    try:
        os.makedirs(pasta_resultados)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise e

    pessoas: List[Pessoa] = planilha.get_pessoas()

    zap_bot: ZapBot = ZapBot.instance()
    resultado = open(arquivo_resultado + '.txt', 'a')

    try:
        resultado.write('\n\n///////////////////////////////////////////Inicio de uma nova execução de envio!!//////////////////////////////////////////////////////\n\n')

        resultado.write('mensagens enviadas:\n')

        for mensagem in mensagens:
            resultado.write('#' + mensagem + '\n')

        resultado.write('\n')

        for pessoa in pessoas:
            if pessoa.invalido:
                resultado.write(str(pessoa))
                resultado.write('FALHA! Mensagens não enviadas para a pessoa acima por estar com o número inválido\n\n')
                continue

            if not pessoa.deve_enviar:
                resultado.write(str(pessoa))
                resultado.write('Mensagens não enviadas para a pessoa acima pois não era necessário\n\n')
                continue

            try:
                mensagens_formatadas: List[str] = formatar_mensagens(mensagens, pessoa)
                zap_bot.enviar_mensagens(pessoa.numero, mensagens_formatadas)
                planilha.marca_como_enviado(pessoa)
                resultado.write(str(pessoa))
                resultado.write('SUCESSO! Mensagens enviadas para a pessoa acima com sucesso\n\n')
                time.sleep(2)

            except NumeroNaoEncontrado:
                resultado.write(str(pessoa))
                resultado.write('FALHA! Mensagens não enviadas para a pessoa acima porque o número não foi encontrado\n\n')

    except Exception as err:
        resultado.write('\nERRO CRÍTICO! A execução teve que ser interrompida por uma exception:' + str(err))
    finally:
        resultado.close()
        zap_bot.close()
