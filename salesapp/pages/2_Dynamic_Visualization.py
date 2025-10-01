from pathlib import Path

import streamlit as st
import pandas as pd


from utilidades import leitura_de_dados, COMISSAO

st.set_page_config(page_title="Dynamic Visualization", layout="wide")

COL_MAP = {
    'Branch': 'filial',
    'Salesperson': 'vendedor',
    'Product': 'produto',
    'Customer Gender': 'cliente_genero',
    'Payment Method': 'forma_pagamento',
}
VAL_MAP = {'Price': 'preco', 'Commission': 'comissao'}
FUNCOES_AGG = {'Sum': 'sum', 'Count': 'count'}

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

# English display mappings for certain categorical columns
df_vendas['forma_pagamento_en'] = df_vendas['forma_pagamento'].map({
    'boleto': 'Bank slip',
    'pix': 'PIX',
    'credito': 'Credit card',
}).fillna(df_vendas['forma_pagamento'])
df_vendas['cliente_genero_en'] = df_vendas['cliente_genero'].map({
    'masculino': 'Male',
    'feminino': 'Female',
}).fillna(df_vendas['cliente_genero'])

indices_labels = st.sidebar.multiselect('Select index columns', list(COL_MAP.keys()))

col_analises_exc = [k for k in COL_MAP.keys() if k not in indices_labels]
colunas_labels = st.sidebar.multiselect('Select columns', col_analises_exc)

valor_label = st.sidebar.selectbox('Select the value to analyze:', list(VAL_MAP.keys()))
metrica_label = st.sidebar.selectbox('Select the metric:', list(FUNCOES_AGG.keys()))

if len(indices_labels) > 0 and len(colunas_labels) > 0:
    metrica_selecionada = FUNCOES_AGG[metrica_label]
    valor_selecionado = VAL_MAP[valor_label]
    # Map labels to data columns
    indices_cols = [COL_MAP[l] for l in indices_labels]
    columns_cols = [COL_MAP[l] for l in colunas_labels]
    # Replace selected PT-BR fields with English-display counterparts for specific columns
    indices_pt_en = ['forma_pagamento_en' if c == 'forma_pagamento' else 'cliente_genero_en' if c == 'cliente_genero' else c for c in indices_cols]
    cols_pt_en = ['forma_pagamento_en' if c == 'forma_pagamento' else 'cliente_genero_en' if c == 'cliente_genero' else c for c in columns_cols]
    vendas_pivotadas = pd.pivot_table(
        df_vendas,
        index=indices_pt_en,
        columns=cols_pt_en,
        values=valor_selecionado,
        aggfunc=metrica_selecionada,
    )
    vendas_pivotadas['GRAND TOTAL'] = vendas_pivotadas.sum(axis=1)
    vendas_pivotadas.loc['GRAND TOTAL'] = vendas_pivotadas.sum(axis=0).to_list()
    st.dataframe(vendas_pivotadas)


