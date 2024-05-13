import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image


st.set_page_config(layout="wide")


@st.cache_data
def gerar_df():
    df = pd.read_excel(
        io="glpinfo_pormunicipio.xlsx",
        engine="openpyxl",
        sheet_name="Worksheet",
        usecols="A:H",
        nrows=132751,
    )
    return df


df = gerar_df()
colunasUteis = ["ANO", "GRANDE REGIÃO", "UF",
                "PRODUTO", "MUNICÍPIO", "P13", "OUTROS"]
df = df[colunasUteis]

with st.sidebar:
    st.subheader('GLP INFO')
    logo_teste = Image.open('brasil.png')
    st.image(logo_teste, use_column_width=True)

    st.subheader('SELEÇÃO DE FILTROS')
    fRegiao = st.selectbox(
        "Selecione a Região:",
        options=df['GRANDE REGIÃO'].unique()
    )

    fEstado = st.selectbox(
        "Selecione o Estado:",
        options=df['UF'].unique()
    )

    # fAno = st.selectbox(
    #     "Selecione o Ano:",
    #     options=df['ANO'].unique()
    # )

    dadosUsuario = df.loc[(
        df['GRANDE REGIÃO'] == fRegiao) &
        (df['UF'] == fEstado)
        # (df['ANO'] == fAno)
    ]

# updateDatas = dadosUsuario['ANO'].__fo
# dadosUsuario['ANO'] = updateDatas

st.header('INFORMAÇÕES DE CONSUMO DE GLP BRASIL: 1922 À 2022')
st.markdown('**Região selecionada:** ' + fRegiao)
st.markdown('**Estado selecionado:** ' + fEstado)

grafP13Estado = alt.Chart(dadosUsuario).mark_line(
    point=alt.OverlayMarkDef(color='red', size=20)
).encode(
    x='ANO',
    y='P13',
    strokeWidth=alt.value(3)
).properties(
    height=500,
    width=920
)

st.altair_chart(grafP13Estado)
dadosUsuario
