import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Comparador de Scooters", layout="wide")

# Título do App
st.title("🛴 Comparador Interativo de Scooters Elétricas")

# Carregar dados
@st.cache_data
def carregar_dados():
    return pd.read_csv("produtos.csv")

dados = carregar_dados()

# Sidebar - Seleção de produtos para comparação
st.sidebar.header("Selecione as scooters para comparar:")

opcoes = dados["Modelo"].tolist()
produtos_selecionados = st.sidebar.multiselect("Modelos:", opcoes, default=opcoes[:2])

# Filtragem dos dados
dados_filtrados = dados[dados["Modelo"].isin(produtos_selecionados)]

if dados_filtrados.empty:
    st.warning("Selecione pelo menos uma scooter para iniciar a comparação.")
else:
    # Mostrar tabela comparativa
    st.subheader("📊 Comparação de Especificações")
    st.dataframe(dados_filtrados.set_index("Modelo"))

    # Gráfico Radar para comparação visual
    st.subheader("🌟 Comparação Visual (Gráfico Radar)")

    categorias = ["Velocidade Máxima (km/h", "Autonomia (km)", "Motor", "Peso Máximo Suportado (kg)", "Aro"]

    fig = go.Figure()

    for index, row in dados_filtrados.iterrows():
        valores = [
            row["Velocidade Máxima (km/h)"],
            row["Autonomia (km)"],
            row["Motor"] / 10,  # Ajuste para melhor visualização
            row["Peso Máximo Suportado (kg)"],
            row["Aro"],
            row["Bateria"],
            row["Removível"]
        ]

        fig.add_trace(go.Scatterpolar(
            r=valores,
            theta=categorias,
            fill='toself',
            name=row["Modelo"]
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(dados_filtrados["Motor"])/10 + 10]
            )
        ),
        showlegend=True
    )

    st.plotly_chart(fig, use_container_width=True)


