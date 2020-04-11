import re


class NumeroInvalido(Exception):
    pass


def formatar_numero_goiania_brasil(numero):
    numero_formatado = re.subn(r'[- ()+]', '', numero)[0]

    if numero_formatado == '':
        raise NumeroInvalido()

    numero_formatado = re.search(r'\d+', numero_formatado).group()

    if len(numero_formatado) < 8:
        raise NumeroInvalido()

    if len(numero_formatado) == 13:
        return numero_formatado

    if len(numero_formatado) > 8 and numero_formatado[-9] != '9':
        numero_formatado = numero_formatado[0:-8] + '9' + numero_formatado[-8:]

    elif len(numero_formatado) == 8:
        numero_formatado = '9' + numero_formatado

    if len(numero_formatado) == 9:
        numero_formatado = '5562' + numero_formatado

    elif len(numero_formatado) == 11:
        numero_formatado = '55' + numero_formatado

    return numero_formatado


def parse_verdadeiro_falso(valor):
    valor_tratado = valor.lower()

    if valor_tratado == 'sim' or valor_tratado == 's' or valor_tratado == 'verdadeiro' or valor_tratado == 'v' or valor_tratado == 'true' or valor_tratado == 't':
        return True

    if valor_tratado == 'nao' or valor_tratado == 'não' or valor_tratado == 'n' or valor_tratado == 'falso' or valor_tratado == 'f' or valor_tratado == 'false':
        return False

    return bool(valor_tratado)


def formatar_mensagens(mensagens, pessoa, infos_adicionais=None):
    mensagens_formatadas = []

    for mensagem in mensagens:
        mensagem_formatada = re.subn(r'%nome', pessoa.primeiro_nome, mensagem)[0]

        if infos_adicionais is not None:
            for info in infos_adicionais:
                mensagem_formatada = re.subn('%' + info.nome_coluna, info.substituicao_efetiva, mensagem_formatada)[0]

        mensagens_formatadas.append(mensagem_formatada)

    return mensagens_formatadas
