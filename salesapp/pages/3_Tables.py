from pathlib import Path

import streamlit as st
import pandas as pd

from utilidades import leitura_de_dados

st.set_page_config(page_title="Tables", layout="wide")

leitura_de_dados()

df_vendas = st.session_state['dados']['df_vendas']
df_filiais = st.session_state['dados']['df_filiais']
df_produtos = st.session_state['dados']['df_produtos']



def mostra_tabela_produtos():
    st.dataframe(df_produtos)


def mostra_tabela_filiais():
    st.dataframe(df_filiais)


def mostra_tabela_vendas():
    st.sidebar.divider()
    st.sidebar.markdown('### Filter table')
    colunas_selecionadas = st.sidebar.multiselect('Select table columns:', list(df_vendas.columns), list(df_vendas.columns))
    col1, col2 = st.sidebar.columns(2)
    filtro_selecionada = col1.selectbox('Filter column', list(df_vendas.columns))
    # Build English-friendly value options for specific columns
    valores_unicos_coluna = list(df_vendas[filtro_selecionada].unique())
    valores_display = valores_unicos_coluna
    if filtro_selecionada == 'forma_pagamento':
        mapa = {'boleto': 'Bank slip', 'pix': 'PIX', 'credito': 'Credit card'}
        valores_display = [mapa.get(v, v) for v in valores_unicos_coluna]
    elif filtro_selecionada == 'cliente_genero':
        mapa = {'masculino': 'Male', 'feminino': 'Female'}
        valores_display = [mapa.get(v, v) for v in valores_unicos_coluna]
    valor_display = col2.selectbox('Filter value', valores_display)
    # Map back to original value
    if filtro_selecionada == 'forma_pagamento':
        rev = {'Bank slip': 'boleto', 'PIX': 'pix', 'Credit card': 'credito'}
        valor_filtro = rev.get(valor_display, valor_display)
    elif filtro_selecionada == 'cliente_genero':
        rev = {'Male': 'masculino', 'Female': 'feminino'}
        valor_filtro = rev.get(valor_display, valor_display)
    else:
        valor_filtro = valor_display
    filtrar = col1.button('Apply filter')
    limpar = col2.button('Clear')

    if filtrar:
        df_disp = df_vendas.loc[df_vendas[filtro_selecionada] == valor_filtro, colunas_selecionadas].copy()
        # Optional display rename/mapping
        rename = {'forma_pagamento': 'payment_method', 'cliente_genero': 'customer_gender'}
        df_disp = df_disp.rename(columns=rename)
        if 'payment_method' in df_disp.columns:
            df_disp['payment_method'] = df_disp['payment_method'].map({'boleto': 'Bank slip', 'pix': 'PIX', 'credito': 'Credit card'}).fillna(df_disp['payment_method'])
        if 'customer_gender' in df_disp.columns:
            df_disp['customer_gender'] = df_disp['customer_gender'].map({'masculino': 'Male', 'feminino': 'Female'}).fillna(df_disp['customer_gender'])
        st.dataframe(df_disp, height=800)
    elif limpar:
        df_disp = df_vendas[colunas_selecionadas].copy()
        rename = {'forma_pagamento': 'payment_method', 'cliente_genero': 'customer_gender'}
        df_disp = df_disp.rename(columns=rename)
        if 'payment_method' in df_disp.columns:
            df_disp['payment_method'] = df_disp['payment_method'].map({'boleto': 'Bank slip', 'pix': 'PIX', 'credito': 'Credit card'}).fillna(df_disp['payment_method'])
        if 'customer_gender' in df_disp.columns:
            df_disp['customer_gender'] = df_disp['customer_gender'].map({'masculino': 'Male', 'feminino': 'Female'}).fillna(df_disp['customer_gender'])
        st.dataframe(df_disp, height=800)
    else:
        df_disp = df_vendas[colunas_selecionadas].copy()
        rename = {'forma_pagamento': 'payment_method', 'cliente_genero': 'customer_gender'}
        df_disp = df_disp.rename(columns=rename)
        if 'payment_method' in df_disp.columns:
            df_disp['payment_method'] = df_disp['payment_method'].map({'boleto': 'Bank slip', 'pix': 'PIX', 'credito': 'Credit card'}).fillna(df_disp['payment_method'])
        if 'customer_gender' in df_disp.columns:
            df_disp['customer_gender'] = df_disp['customer_gender'].map({'masculino': 'Male', 'feminino': 'Female'}).fillna(df_disp['customer_gender'])
        st.dataframe(df_disp, height=800)


st.sidebar.markdown('## Select a Table')

tabelas_selecionada = st.sidebar.selectbox('Choose the table you want to view:',
                                           ['Sales', 'Products', 'Branches'])

if tabelas_selecionada == 'Products':
    mostra_tabela_produtos()
elif tabelas_selecionada == 'Branches':
     mostra_tabela_filiais()
elif tabelas_selecionada == 'Sales':
     mostra_tabela_vendas()
