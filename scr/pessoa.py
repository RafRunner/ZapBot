class Pessoa:

    def __init__(self, linha, nome, numero, deve_enviar, invalido, infos_adicionais):
        self.linha = linha
        self.nome = nome
        self.numero = numero
        self.deve_enviar = deve_enviar
        self.invalido = invalido
        self.infos_adicionais = infos_adicionais

        self.primeiro_nome = nome.split()[0]

    def get_informacao_adicional(self, nome_informacao):
        if self.infos_adicionais is not None and len(self.infos_adicionais) > 0:
            return self.infos_adicionais[0].encontra_informacao_por_nome(nome_informacao)

        return None

    def __str__(self):
        return 'Linha:' + str(self.linha) + '\nNome: ' + self.nome + '\nNumero: ' + self.numero + '\nDeve enviar: ' + \
               str(self.deve_enviar) + '\nInvalido: ' + str(self.invalido) + '\n'
