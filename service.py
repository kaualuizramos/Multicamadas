import re

from model import Cliente, Conta, converter_dinheiro


class BancoService:
    def __init__(self, repository):
        self.repository = repository

    def criar_conta(self, nome, cpf, saldo_inicial):
        nome = nome.strip()
        cpf = re.sub(r"\D", "", cpf)

        if not nome:
            raise ValueError("Informe o nome do cliente.")

        if len(cpf) != 11 or cpf == cpf[0] * 11:
            raise ValueError("Informe um CPF válido com 11 dígitos.")

        if self.repository.buscar_por_cpf(cpf):
            raise ValueError("Já existe uma conta com esse CPF.")

        saldo = converter_dinheiro(saldo_inicial)

        if saldo < 0:
            raise ValueError("O saldo inicial não pode ser negativo.")

        cliente = Cliente(nome, cpf)
        conta = Conta(cliente, saldo)

        self.repository.salvar(conta)
        return conta

    def depositar(self, numero_conta, valor):
        conta = self._obter_conta(numero_conta)
        conta.depositar(valor)
        return conta

    def sacar(self, numero_conta, valor):
        conta = self._obter_conta(numero_conta)
        conta.sacar(valor)
        return conta

    def consultar_conta(self, numero_conta):
        return self._obter_conta(numero_conta)

    def listar_contas(self):
        return self.repository.listar_todas()

    def consultar_historico(self, numero_conta):
        return self._obter_conta(numero_conta).historico

    def _obter_conta(self, numero_conta):
        conta = self.repository.buscar_por_numero(numero_conta)

        if conta is None:
            raise ValueError("Conta não encontrada.")

        return conta
