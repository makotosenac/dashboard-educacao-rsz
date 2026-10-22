
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Análise da Educação no RS",
    layout="wide"
)

st.title("Estabelecimentos de Ensino Fundamental no RS")

st.write("""
Este dashboard apresenta uma análise dos estabelecimentos
de ensino fundamental nos municípios do Rio Grande do Sul.
""")

arquivo = st.file_uploader(
    "Envie o arquivo CSV",
    type=["csv"]
)

if arquivo is not None:
    df = pd.read_csv(arquivo, encoding="latin1", skiprows=1)

    st.subheader("Visualização inicial")
    st.dataframe(df.head())
    
    st.subheader("Filtrar por município")

    municipios = sorted(df["Município"].dropna().unique())

    municipio_selecionado = st.selectbox(
        "Escolha um município",
        ["Todos os municípios"] + municipios
    )

    if municipio_selecionado != "Todos os municípios":
        df_filtrado = df[df["Município"] == municipio_selecionado]
    else:
        df_filtrado = df


    col1, col2 = st.columns(2)

    col1.metric("Quantidade de registros", df.shape[0])
    col2.metric("Quantidade de colunas", df.shape[1])

    st.subheader("Colunas disponíveis")
    st.write(list(df.columns))

    st.subheader("Verificação dos dados")

    st.write("Tipos de dados:")
    st.write(df.dtypes)

    st.write("Valores ausentes por coluna:")
    st.write(df.isnull().sum())

    st.write("Quantidade de registros duplicados:")
    st.write(df.duplicated().sum())

    st.subheader("Evolução dos estabelecimentos por ano")

    anos = list(range(2014, 2025))
    totais = []

    for ano in anos:
        coluna = f"Educação/Ensino Fundamental/Estabelecimentos de Ensino/Total {ano} (Estabelecimentos)"
        total = pd.to_numeric(df[coluna], errors="coerce").sum()
        totais.append(total)

    grafico = pd.DataFrame({
        "Ano": anos,
        "Total de estabelecimentos": totais
    })

    fig = px.line(
        grafico,
        x="Ano",
        y="Total de estabelecimentos",
        markers=True,
        title="Estabelecimentos de Ensino Fundamental no RS (2014–2024)"
    )

    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    **O que podemos observar?**

    Este gráfico apresenta a evolução da quantidade de
    estabelecimentos de Ensino Fundamental no Rio Grande
    do Sul entre 2014 e 2024. Ele permite observar se o
    total aumentou, diminuiu ou permaneceu semelhante
    ao longo dos anos.
    """)


    st.subheader("Top 10 municípios em 2024")

    coluna_2024 = "Educação/Ensino Fundamental/Estabelecimentos de Ensino/Total 2024 (Estabelecimentos)"

    df[coluna_2024] = pd.to_numeric(
        df[coluna_2024], errors="coerce"
    )

    top10 = df.nlargest(10, coluna_2024)

    grafico_municipios = px.bar(
        top10,
        x=coluna_2024,
        y="Município",
        orientation="h",
        title="10 municípios com mais estabelecimentos em 2024",
        labels={
            coluna_2024: "Quantidade de estabelecimentos",
            "Município": "Município"
        }
    )

    grafico_municipios.update_layout(
        yaxis={"categoryorder": "total ascending"}
    )

    st.plotly_chart(grafico_municipios, use_container_width=True)
