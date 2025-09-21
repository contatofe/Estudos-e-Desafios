import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import random
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import matplotlib.colors as mcolors

#Funções

def radar():
    categorias = df.columns[1:].tolist() 
    categorias_radar = categorias + [categorias[0]]

    fig = go.Figure()

    for i, (index, row) in enumerate(df.iterrows()):
        valores = row[1:].values.tolist()
        valores += valores[:1]  # Fechar o polígono
        
        fig.add_trace(go.Scatterpolar(
            r=valores,
            theta=categorias_radar,
            fill='toself',
            name=row['Etiqueta'],
            line_color='lightgreen',
            fillcolor='rgba(0, 200, 0, 0.2)'
        ))

    fig.update_layout(
        height=500,  
        width=None,  
        margin=dict(t=50, b=100, l=50, r=50),  # ✅ b=100 para dar espaço à legenda embaixo
        polar=dict(
            bgcolor='rgba(230, 255, 230, 0.8)',
            radialaxis=dict(
                visible=True,
                range=[0, 10],
                tickvals=[0, 2, 4, 6, 8, 10],
                gridcolor='white',
                linecolor='white'
            ),
            angularaxis=dict(
                gridcolor='rgba(255, 255, 255, 0.5)',
                linecolor='rgba(255, 255, 255, 0.8)',
                rotation=90
            )
        ),
        # ✅ legend FORA do polar — no nível principal do layout
        legend=dict(
            orientation="h",      
            yanchor="bottom",       
            y=-0.3,                
            xanchor="center",       
            x=0.5,                  
            font=dict(size=15),     
            traceorder="normal"     
        )
    )

    return fig


def barras(df, coluna_avaliacao):

  participantes = df['Etiqueta'].tolist()
  avaliacoes = df[coluna_avaliacao].tolist()

  #Calcula média
  media = sum(avaliacoes) / len(avaliacoes)

  #Simula cores dependendo da nota
  cores = ['#A8E6A1' if avaliacao >= media else '#B19CD9' for avaliacao in avaliacoes]

  fig = go.Figure()

  #Criar barras
  fig.add_trace(go.Bar(
      x=participantes,
      y=avaliacoes,
      marker_color=cores,
      text=[f'{n:.1f}' for n in avaliacoes],
      textposition='outside',
  ))

  #Criar Linha de média
  fig.add_hline(
      y=media,
      line_color="white",
      line_width=3,
      annotation_text=f"Média: {media:.2f}",
      annotation_position="top left",
      annotation_font_size=14,
      annotation_bgcolor="white"
  )

  # Customizar gráfico
  fig.update_layout(
    title=f"Avaliação: {coluna_avaliacao} vs Média",
    yaxis_title=coluna_avaliacao,
    xaxis_title="Participante",
    showlegend=False,
    height=500,
    plot_bgcolor='rgba(230, 255, 230, 0.5)',   
  )
  return fig

def correlacao():

    # Criando paleta de cores
    colors = ['#B19CD9',  # lilás (ex: amethyst / light purple)
            '#FFFFFF',  # branco
            '#A8E6A1']  # verde claro (mint green / light green)

    custom_cmap = mcolors.LinearSegmentedColormap.from_list("lilas_branco_verde", colors)

    # Criando gráfico
    corr = (df.drop(columns=['Etiqueta'])).corr(method="pearson")

    plt.figure(figsize=(8, 4))
    sns.heatmap(corr, annot=True, cmap=custom_cmap, vmin=-1, vmax=1, center=0)
    
    fig = plt.gcf()
    plt.close()  
    return fig

# Configuração inicial
st.set_page_config(
    page_title="Dados Neuromath",
    page_icon="🧠",
    layout="wide",  # usa toda a largura da tela
    initial_sidebar_state="expanded"
)
#Título
st.html(
    """
    <div style='text-align: center;'>
        <img src='https://i.postimg.cc/y1JHW0Rs/Header.png' width='900'/>
    </div>
    """
)
st.markdown("---")  
st.markdown("<h1 style='text-align: center;'>Resultados da coleta inicial</h1>", unsafe_allow_html=True)
st.markdown("---")  

# Carregando dados

df = pd.read_csv("Dados/Dados.csv", sep = ";")
df['DAt (BFP)'] = df['DAt (BFP)'].astype(int)

col1, col2 = st.columns(2)

# Gráfico 1

with col1:
    with st.container(height=600, border=True):
        st.markdown("<h3 style='text-align: center;'>Visualização dos resultados dos testes</h3>", unsafe_allow_html=True)
        fig_radar = radar()
        st.plotly_chart(fig_radar, use_container_width=True)

# Gráfico 2

with col2:
    with st.container(height=600, border=True):
        st.markdown("<h3 style='text-align: center;'>Correlação de Pearson entre os testes</h3>", unsafe_allow_html=True)
        fig_corr = correlacao()
        st.pyplot(fig_corr, use_container_width=True)
        st.markdown("**|r| entre 0.8 e 1.0:** Correlação forte ou muito forte. \n\n **|r| entre 0.5 e 0.8:** Correlação moderada. \n\n **|r| entre 0.3 e 0.5:** Correlação fraca \n\n **|r| entre 0.0 e 0.3:** Correlação desprezível ou muito fraca.")

# Gráfico 3

st.markdown("---")  
st.markdown("<h3 style='text-align: center;'>Comparação do desempenho individual vs média</h3>", unsafe_allow_html=True)

colunas_avaliacao = df.columns[1:].tolist()

tabs = st.tabs(colunas_avaliacao)

for tab, coluna in zip(tabs, colunas_avaliacao):
    with tab:
        fig_barras = barras(df, coluna)  
        st.plotly_chart(fig_barras, use_container_width=True)

# Tabela


st.markdown("---")  
st.markdown("<h3 style='text-align: center;'>Dados Tabelados</h3>", unsafe_allow_html=True)
st.dataframe(df, hide_index=True, use_container_width=True, height = 525)