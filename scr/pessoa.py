class Pessoa:

    def __init__(self, linha, nome, numero, check, invalido, infos_adicionais):
        self.linha = linha
        self.nome = nome
        self.numero = numero
        self.check = check
        self.invalido = invalido
        self.infos_adicionais = infos_adicionais

        self.primeiro_nome = nome.split()[0]

    def __str__(self):
        return 'Linha:' + str(self.linha) + '\nNome: ' + self.nome + '\nNumero: ' + self.numero + '\nCheck: ' + str(self.check) + '\nInvalido: ' + str(self.invalido) + '\n'
