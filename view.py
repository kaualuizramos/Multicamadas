import streamlit as st


class ContaView:
    @staticmethod
    def moeda(valor):
        return (
            f"R$ {valor:,.2f}"
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )

    def exibir_cabecalho(self):
        st.title("🏦 Banco Digital")
        st.caption("Sistema bancário — Arquitetura Multicamadas")
        st.divider()

    def formulario_criar_conta(self, service):
        st.subheader("Criar Conta")

        with st.form("form_criar_conta"):
            nome = st.text_input("Nome completo")
            cpf = st.text_input(
                "CPF",
                max_chars=14,
                placeholder="000.000.000-00"
            )
            saldo = st.number_input(
                "Saldo inicial (R$)",
                min_value=0.0,
                value=0.0,
                step=10.0,
                format="%.2f"
            )

            enviar = st.form_submit_button(
                "Criar Conta",
                use_container_width=True
            )

        if enviar:
            try:
                conta = service.criar_conta(nome, cpf, saldo)
                st.session_state.conta_selecionada = conta.numero
                st.session_state.aviso = (
                    "sucesso",
                    f"Conta {conta.numero} criada com sucesso!"
                )
            except ValueError as erro:
                st.session_state.aviso = ("erro", str(erro))

            st.rerun()

    def selecionar_conta(self, service, chave):
        contas = service.listar_contas()

        if not contas:
            st.info("Cadastre uma conta para começar.")
            return None

        numeros = [conta.numero for conta in contas]
        conta_atual = st.session_state.get("conta_selecionada")

        indice = (
            numeros.index(conta_atual)
            if conta_atual in numeros
            else 0
        )

        selecionada = st.selectbox(
            "Selecione a conta",
            numeros,
            index=indice,
            format_func=lambda numero: (
                f"Conta {numero} — "
                f"{service.consultar_conta(numero).cliente.nome}"
            ),
            key=chave
        )

        st.session_state.conta_selecionada = selecionada
        return selecionada

    def exibir_dados_conta(self, conta):
        st.subheader("Dados da Conta")
        st.write(f"**Número:** {conta.numero}")
        st.write(f"**Cliente:** {conta.cliente.nome}")
        st.write(f"**CPF:** {conta.cliente.cpf}")
        st.metric("Saldo disponível", self.moeda(conta.saldo))

    def formulario_deposito(self, service, numero):
        st.subheader("💰 Depósito")

        with st.form(f"form_deposito_{numero}"):
            valor = st.number_input(
                "Valor do depósito (R$)",
                min_value=0.0,
                value=0.0,
                step=10.0,
                format="%.2f",
                key=f"valor_deposito_{numero}"
            )

            enviar = st.form_submit_button(
                "Depositar",
                use_container_width=True
            )

        if enviar:
            try:
                service.depositar(numero, valor)
                st.session_state.aviso = (
                    "sucesso", "Depósito realizado com sucesso!"
                )
            except ValueError as erro:
                st.session_state.aviso = ("erro", str(erro))

            st.rerun()

    def formulario_saque(self, service, numero):
        st.subheader("💸 Saque")

        with st.form(f"form_saque_{numero}"):
            valor = st.number_input(
                "Valor do saque (R$)",
                min_value=0.0,
                value=0.0,
                step=10.0,
                format="%.2f",
                key=f"valor_saque_{numero}"
            )

            enviar = st.form_submit_button(
                "Sacar",
                use_container_width=True
            )

        if enviar:
            try:
                service.sacar(numero, valor)
                st.session_state.aviso = (
                    "sucesso", "Saque realizado com sucesso!"
                )
            except ValueError as erro:
                st.session_state.aviso = ("erro", str(erro))

            st.rerun()

    def exibir_historico(self, conta):
        st.subheader("📋 Histórico de Movimentações")
        historico = conta.historico

        if not historico:
            st.info("Nenhuma movimentação registrada.")
            return

        for item in reversed(historico):
            with st.container(border=True):
                st.write(f"**Data:** {item['data']}")
                st.write(f"**Operação:** {item['tipo']}")
                st.write(f"**Valor:** {self.moeda(item['valor'])}")
                st.write(
                    f"**Saldo após operação:** "
                    f"{self.moeda(item['saldo'])}"
                )

    def exibir_lista_contas(self, contas):
        st.subheader("Contas Cadastradas")

        if not contas:
            st.info("Nenhuma conta cadastrada.")
            return

        for conta in contas:
            with st.expander(
                f"Conta {conta.numero} — {conta.cliente.nome}"
            ):
                st.write(f"**CPF:** {conta.cliente.cpf}")
                st.write(f"**Saldo:** {self.moeda(conta.saldo)}")
