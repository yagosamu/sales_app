from pathlib import Path
from datetime import date, timedelta

import plotly.express as px
import streamlit as st
import pandas as pd

from utilidades import leitura_de_dados, COMISSAO

st.set_page_config(page_title="Overview", layout="wide")

selecao_keys = {
    'Branch': 'filial',
    'Salesperson': 'vendedor',
    'Product': 'produto',
    'Payment Method': 'forma_pagamento',
    'Customer Gender': 'cliente_genero',
}

leitura_de_dados()

df_vendas = st.session_state['dados']['df_vendas']
df_filiais = st.session_state['dados']['df_filiais']
df_produtos = st.session_state['dados']['df_produtos']

df_produtos = df_produtos.rename(columns={'nome': 'produto'})
df_vendas = df_vendas.reset_index()
df_vendas = pd.merge(left=df_vendas,
                     right=df_produtos[['produto', 'preco']],
                     on='produto',  
                     how='left')
df_vendas = df_vendas.set_index('data')
df_vendas['comissao'] = df_vendas['preco'] * COMISSAO

# English display mappings (data remains in PT-BR under original columns)
df_vendas['forma_pagamento_en'] = df_vendas['forma_pagamento'].map({
    'boleto': 'Bank slip',
    'pix': 'PIX',
    'credito': 'Credit card',
}).fillna(df_vendas['forma_pagamento'])
df_vendas['cliente_genero_en'] = df_vendas['cliente_genero'].map({
    'masculino': 'Male',
    'feminino': 'Female',
}).fillna(df_vendas['cliente_genero'])

data_final_def = df_vendas.index.date.max()
data_inicial_def = date(year=data_final_def.year, month=data_final_def.month, day=1)
data_inicial = st.sidebar.date_input('Start Date', data_inicial_def)
data_final = st.sidebar.date_input('End Date', data_final_def)
analise_selecionada = st.sidebar.selectbox('Analyze by:', list(selecao_keys.keys()))
# Use English-friendly columns for specific categories
analise_selecionada = selecao_keys[analise_selecionada]
if analise_selecionada == 'forma_pagamento':
    analise_selecionada = 'forma_pagamento_en'
elif analise_selecionada == 'cliente_genero':
    analise_selecionada = 'cliente_genero_en'

df_vendas_corte = df_vendas[(df_vendas.index.date >= data_inicial) & (df_vendas.index.date <= data_final)]
df_vendas_corte_anterior = df_vendas[(df_vendas.index.date >= data_inicial - timedelta(days=30)) & (df_vendas.index.date <= data_final - timedelta(days=30))]

st.markdown('# Analysis Dashboard')

col1, col2, col3, col4 = st.columns(4)

valor_vendas = f"R$ {df_vendas_corte['preco'].sum():.2f}"
dif_metrica = df_vendas_corte['preco'].sum() - df_vendas_corte_anterior['preco'].sum()
col1.metric('Sales value in period', valor_vendas, float(dif_metrica))

quantidade_vendas = df_vendas_corte['preco'].count()
dif_metrica = df_vendas_corte['preco'].count() - df_vendas_corte_anterior['preco'].count()
col2.metric('Number of sales in period', quantidade_vendas, int(dif_metrica))

principal_filial = df_vendas_corte['filial'].value_counts().index[0]
col3.metric('Top Branch', principal_filial)

principal_vendedor = df_vendas_corte['vendedor'].value_counts().index[0]
col4.metric('Top Salesperson', principal_vendedor)

st.divider()

col21, col22 = st.columns(2)

df_vendas_corte['dia_venda'] = df_vendas_corte.index.date
venda_dia = df_vendas_corte.groupby('dia_venda')['preco'].sum()
venda_dia.name = 'Sales Value'
venda_dia.index.name = 'Sale day'

fig = px.line(venda_dia)
col21.plotly_chart(fig)

fig = px.pie(df_vendas_corte, 
             names=analise_selecionada,
             values='preco')


col22.plotly_chart(fig)

st.divider()
