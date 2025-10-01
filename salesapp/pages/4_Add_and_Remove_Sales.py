from pathlib import Path
from datetime import datetime

import streamlit as st
import pandas as pd

from utilidades import leitura_de_dados

leitura_de_dados()

df_vendas = st.session_state['dados']['df_vendas']
df_filiais = st.session_state['dados']['df_filiais']
df_produtos = st.session_state['dados']['df_produtos']

df_filiais['cidade/estado'] = df_filiais['cidade'] + '/' + df_filiais['estado']
cidades_filiais = df_filiais['cidade/estado'].to_list()


st.set_page_config(page_title="Add and Remove Sales", layout="wide")

st.sidebar.markdown('## Add Sales')
filial_selecionada = st.sidebar.selectbox('Select branch:', cidades_filiais)
vendedores = df_filiais.loc[df_filiais['cidade/estado'] == filial_selecionada, 'vendedores'].iloc[0]
# Convertendo a string de vendedores em uma lista
vendedores = vendedores.strip('][').replace("'", '').split(', ')
vendedor_selecionado = st.sidebar.selectbox('Select salesperson:', vendedores)
produtos = df_produtos['nome'].to_list()
produto_selecionado = st.sidebar.selectbox('Select product:', produtos)
nome_cliente = st.sidebar.text_input('Customer name')

genero_label = st.sidebar.selectbox('Customer gender:', ['Male', 'Female'])
forma_pagamento_label = st.sidebar.selectbox('Payment method:', ['Bank slip', 'PIX', 'Credit card'])

genero_selecionado = {'Male': 'masculino', 'Female': 'feminino'}[genero_label]
forma_pagamento = {'Bank slip': 'boleto', 'PIX': 'pix', 'Credit card': 'credito'}[forma_pagamento_label]

adicionar_venda = st.sidebar.button('Add Sale')
if adicionar_venda:
    lista_adicionar = [df_vendas['id_venda'].max() + 1,
                       filial_selecionada.split('/')[0],
                       vendedor_selecionado,
                       produto_selecionado,
                       nome_cliente,
                       genero_selecionado,
                       forma_pagamento]
    hora_adicionar = datetime.now()
    df_vendas.loc[hora_adicionar] = lista_adicionar
    caminho_datasets = st.session_state['caminho_datasets']
    df_vendas.to_csv(caminho_datasets / 'vendas.csv', decimal=',', sep=';')

st.sidebar.markdown('## Remove Sales')
id_remocao = st.sidebar.number_input('Sale ID to remove:', 0, df_vendas['id_venda'].max())
remover_venda = st.sidebar.button('Remove Sale')
if remover_venda:
    df_vendas = df_vendas[df_vendas['id_venda'] != id_remocao]
    caminho_datasets = st.session_state['caminho_datasets']
    df_vendas.to_csv(caminho_datasets / 'vendas.csv', decimal=',', sep=';')
    st.session_state['dados']['df_vendas'] = df_vendas

st.dataframe(df_vendas, height=800)
