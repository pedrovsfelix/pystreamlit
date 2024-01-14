import pandas as pd # pip install pandas openpyxl
import plotly.express as px # pip install plotly-express
import streamlit as st # pip install streamlit

dados = pd.read_excel('dados.xlsx')

st.set_page_config(page_title="Dashboard", page_icon=":bar_chart:", layout="wide")

st.sidebar.header("Filtros: ")

estado = st.sidebar.multiselect(
    "Selecione ao menos um estado:",
    options=dados["UF"].unique(),
    default=dados["UF"].unique()
)

produto = st.sidebar.multiselect(
    label="Selecione ao menos um produto:",
    options=dados["PRODUTO"].unique(),
    default=dados["PRODUTO"].unique()
)

dados_selection = dados.query(
    "UF==@estado &PRODUTO==@produto"
)

# --- PÁGINA PRINCIPAL ---

st.title(":bar_chart: Dashboard - Vendas anuais de etanol hidratado e derivados de petróleo por município")
st.markdown("##")

# metrics ---
litros_comercializados = int(dados_selection["VENDAS"].sum())
estados_comerciantes = len(pd.unique(dados_selection["UF"]))

left_column, middle_column, right_column = st.columns(3)

def metrics():
    from streamlit_extras.metric_cards import style_metric_cards
    col1,col2 = st.columns(2)
    col1.metric("Litros comercializados:",value=f"{litros_comercializados:_.0f}".replace("_", "."))
    col2.metric("Estados comerciantes:",value=estados_comerciantes)

    style_metric_cards(background_color="#3d3d3d", border_left_color="#ce2d4f")
metrics()

st.markdown("---")
st.markdown("##")

# pie chart
div1, div2=st.columns(2)
def pie():
    with div1:
        theme_plotly=None
        fig=px.pie(dados_selection, values="VENDAS", names="PRODUTO",title="Combustíveis")
        fig.update_layout(legend_title="PRODUTO", legend_y=0.9)
        fig.update_traces(textinfo="percent+label", textposition="inside")
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
pie()

def bar():
    with div2:
        theme_plotly=None
        fig=px.bar(dados_selection, y="VENDAS", x="REGIAO", text_auto='.2s', title="Vendas x Ano")
        fig.update_traces(textfont_size=18, textangle=0, textposition="outside",cliponaxis=False)
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
bar()