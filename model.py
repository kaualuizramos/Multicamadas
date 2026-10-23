from datetime import datetime
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP


CENTAVO = Decimal("0.01")


def converter_dinheiro(valor):
    try:
        dinheiro = Decimal(str(valor))

        if not dinheiro.is_finite():
            raise ValueError("Informe um valor monetário válido.")

        return dinheiro.quantize(
            CENTAVO,
            rounding=ROUND_HALF_UP
        )
    except (InvalidOperation, TypeError, ValueError):
        raise ValueError("Informe um valor monetário válido.")


class Cliente:
    def __init__(self, nome, cpf):
        self.nome = nome.strip()
        self.cpf = cpf


class Conta:
    proximo_numero = 1

    def __init__(self, cliente, saldo_inicial=0):
        saldo = converter_dinheiro(saldo_inicial)

        if saldo < 0:
            raise ValueError("O saldo inicial não pode ser negativo.")

        self.numero = Conta.proximo_numero
        Conta.proximo_numero += 1

        self.cliente = cliente
        self._saldo = saldo
        self._historico = []

        if saldo > 0:
            self._registrar_historico("Depósito inicial", saldo)

    @property
    def saldo(self):
        return self._saldo

    @property
    def historico(self):
        return tuple(
            movimentacao.copy()
            for movimentacao in self._historico
        )

    def _registrar_historico(self, tipo, valor):
        self._historico.append({
            "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "tipo": tipo,
            "valor": valor,
            "saldo": self._saldo
        })

    def depositar(self, valor):
        valor = converter_dinheiro(valor)

        if valor <= 0:
            raise ValueError("O depósito deve ser maior que zero.")

        self._saldo += valor
        self._registrar_historico("Depósito", valor)

    def sacar(self, valor):
        valor = converter_dinheiro(valor)

        if valor <= 0:
            raise ValueError("O saque deve ser maior que zero.")

        if valor > self._saldo:
            raise ValueError("Saldo insuficiente para realizar o saque.")

        self._saldo -= valor
        self._registrar_historico("Saque", valor)


class BancoDados:
    def __init__(self):
        self.contas = []

    def salvar(self, conta):
        self.contas.append(conta)

    def listar_todas(self):
        return list(self.contas)

    def buscar_por_numero(self, numero):
        for conta in self.contas:
            if conta.numero == numero:
                return conta
        return None

    def buscar_por_cpf(self, cpf):
        for conta in self.contas:
            if conta.cliente.cpf == cpf:
                return conta
        return None
