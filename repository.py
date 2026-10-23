class ContaRepository:
    def __init__(self, banco_dados):
        self.banco_dados = banco_dados

    def salvar(self, conta):
        self.banco_dados.salvar(conta)

    def listar_todas(self):
        return self.banco_dados.listar_todas()

    def buscar_por_numero(self, numero):
        return self.banco_dados.buscar_por_numero(numero)

    def buscar_por_cpf(self, cpf):
        return self.banco_dados.buscar_por_cpf(cpf)
