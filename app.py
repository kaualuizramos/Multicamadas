import streamlit as st

from model import BancoDados
from repository import ContaRepository
from service import BancoService
from view import ContaView


st.set_page_config(
    page_title="Banco Digital",
    page_icon="🏦",
    layout="centered"
)


# Inicializar o armazenamento da sessão
if "banco_dados" not in st.session_state:
    st.session_state.banco_dados = BancoDados()

if "conta_selecionada" not in st.session_state:
    st.session_state.conta_selecionada = None

if "aviso" not in st.session_state:
    st.session_state.aviso = None


# Instanciar as camadas
banco = st.session_state.banco_dados
repository = ContaRepository(banco)
service = BancoService(repository)
view = ContaView()


# Mostrar mensagens após operações
aviso = st.session_state.aviso

if aviso:
    tipo, mensagem = aviso

    if tipo == "erro":
        st.error(mensagem)
    else:
        st.success(mensagem)

    st.session_state.aviso = None


# Interface principal
view.exibir_cabecalho()

aba_criar, aba_operacoes, aba_historico = st.tabs([
    "Criar Conta",
    "Depósito e Saque",
    "Histórico"
])


with aba_criar:
    view.formulario_criar_conta(service)
    st.divider()
    view.exibir_lista_contas(service.listar_contas())


with aba_operacoes:
    numero = view.selecionar_conta(
        service, "seletor_operacoes"
    )

    if numero is not None:
        conta = service.consultar_conta(numero)
        view.exibir_dados_conta(conta)

        coluna_deposito, coluna_saque = st.columns(2)

        with coluna_deposito:
            view.formulario_deposito(service, numero)

        with coluna_saque:
            view.formulario_saque(service, numero)


with aba_historico:
    numero = view.selecionar_conta(
        service, "seletor_historico"
    )

    if numero is not None:
        conta = service.consultar_conta(numero)
        view.exibir_dados_conta(conta)
        view.exibir_historico(conta)
