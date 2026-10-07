#Projeto em Python para cadastrar vendas
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

# Passo 1: Criar a tela do sistema
st.write("# Sistema de Vendas")

tabela = pd.read_csv("database/vendas.csv")

# Passo 2: Criar o formulário de cadastro

if "mostrar_formulario" not in st.session_state:
    st.session_state.mostrar_formulario = False


# Botão para abrir/fechar
if st.sidebar.button(
    "➕ Cadastrar venda",
    use_container_width=True
):
    st.session_state.mostrar_formulario = not st.session_state.mostrar_formulario


if st.session_state.mostrar_formulario:
    st.sidebar.write("## Cadastrar venda")


    # Valores iniciais do formulário(para o botão limpar)
    if "data_venda" not in st.session_state:
        st.session_state.data_venda = date.today()

    if "vendedor_venda" not in st.session_state:
        st.session_state.vendedor_venda = "Ana"

    if "produto_venda" not in st.session_state:
        st.session_state.produto_venda = "Notebook"

    if "quantidade_venda" not in st.session_state:
        st.session_state.quantidade_venda = 0

    if "valor_venda" not in st.session_state:
        st.session_state.valor_venda = 0.0

    def limpar_form():
        st.session_state.data_venda = date.today()
        st.session_state.vendedor_venda = "Ana"
        st.session_state.produto_venda = "Notebook"
        st.session_state.quantidade_venda = 0
        st.session_state.valor_venda = 0.0
        

    # Campos do formulário
    data = st.sidebar.date_input("Data", max_value=date.today(), key="data_venda")
    vendedor = st.sidebar.selectbox("Vendedor", ["Ana", "Bruno", "Carla"], key="vendedor_venda")
    produto = st.sidebar.selectbox("Produto", ["Notebook", "Celular", "Fone"], key="produto_venda")
    quantidade = st.sidebar.number_input("Quantidade", step=1, key="quantidade_venda")
    valor = st.sidebar.number_input("Valor", key="valor_venda")


    col1, col2 = st.sidebar.columns([2, 1])

    with col1:
        botao = st.button("Cadastrar venda", use_container_width=True)

    with col2:
        limpar = st.button( "Limpar", type="primary", use_container_width=True, on_click=limpar_form)

    # Passo 3: Salvar a venda na base de dados
    if botao:
        if quantidade <= 0:
            st.error("A quantidade deve ser maior que zero.")

        elif valor <= 0:
            st.error("O valor deve ser maior que zero.")
        else:
            nova_venda = [data, vendedor, produto, quantidade, valor]

            tabela.loc[len(tabela)] = nova_venda
            tabela.to_csv("database/vendas.csv", index=False)

            st.success("Venda cadastrada com SUCESSO!")


    

# Passo 4: Mostrar a base de dados na tela
st.write("## Vendas cadastradas")
st.dataframe(tabela)

# Passo 5: Criar o dashboard
st.write("## Dashboard")
soma = tabela["valor"].sum()
st.metric("Faturamento total", f"R${soma}")

grafico = px.bar(tabela, x="vendedor", y="valor", color="produto")
st.plotly_chart(grafico)

grafico2 = px.pie(tabela, names="produto", values="valor")
st.plotly_chart(grafico2)