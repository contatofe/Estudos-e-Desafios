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

def radar(df: pd.DataFrame) -> go.Figure:
    # Mantém APENAS as 3 séries desejadas
    categorias_keep = [
        'Funcionamento PNa Existente - PAM01',
        'Funcionamento PNa de Referência',
        'Funcionamento PNa Esperado'
    ]
    df_red = df[df['Etiqueta'].isin(categorias_keep)].copy()

    # (opcional) mover a 1ª linha para o final por estética
    if len(df_red) > 0:
        df_plot = pd.concat([df_red.iloc[1:], df_red.iloc[[0]]], ignore_index=True)
    else:
        df_plot = df_red.copy()

    # Colunas de métricas
    categorias_cols = df_plot.columns[1:].tolist()
    if not categorias_cols:
        raise ValueError("Não há colunas de métricas após 'Etiqueta'.")

    # Garantir numérico
    df_plot[categorias_cols] = df_plot[categorias_cols].apply(pd.to_numeric, errors='coerce')

    # Fechar o polígono
    categorias_radar = categorias_cols + [categorias_cols[0]]

    cores_destaque = {
        'Funcionamento PNa Esperado': ('rgba(234,116,111,1.0)', 'rgba(234,116,111,0.20)'),
        'Funcionamento PNa de Referência': ('rgba(88,183,248,1.0)', 'rgba(88,183,248,0.20)'),
        # A existente (PAM01) fica na cor padrão abaixo
    }
    cor_padrao_linha = 'rgb(63,78,28)'
    cor_padrao_fill  = 'rgba(154,193,69,0.40)'

    fig = go.Figure()
    for _, row in df_plot.iterrows():
        r_vals = row[categorias_cols].tolist()
        r_vals.append(r_vals[0])  # fecha

        cor_linha, cor_fill = cores_destaque.get(
            row['Etiqueta'], (cor_padrao_linha, cor_padrao_fill)
        )

        fig.add_trace(go.Scatterpolar(
            r=r_vals,
            theta=categorias_radar,
            fill='toself',
            name=row['Etiqueta'],
            line=dict(color=cor_linha),
            fillcolor=cor_fill
        ))

    fig.update_layout(
        title=dict(text='Perfil Psiconeuroatencional (PNa) de PAM01 em noções matemáticas', x=0.5, font=dict(size=24)),
        legend=dict(orientation='h', yanchor='top', y=-0.2, xanchor='center', x=0.5),
        polar=dict(
            bgcolor='rgba(170,223,54,0.05)',
            radialaxis=dict(visible=True, range=[0, 10], tickvals=[0, 2, 4, 6, 8, 10],
                            gridcolor='white', linecolor='white'),
            angularaxis=dict(gridcolor='rgba(139,184,56,0.10)', linecolor='rgba(139,184,56,0.10)',
                             rotation=90, direction='clockwise')
        ),
        margin=dict(l=40, r=40, t=80, b=80)
    )
    return fig



def barras(df, coluna_avaliacao):

  participantes = df['Etiqueta'].tolist()
  avaliacoes = df[coluna_avaliacao].tolist()

  #Calcula média
  media = sum(avaliacoes) / len(avaliacoes)

  #Simula cores dependendo da nota
  cores = ['#9AC145' if avaliacao >= media else '#EA746F' for avaliacao in avaliacoes]

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
    plot_bgcolor='rgba(170,223,54,0.05)',   
  )
  return fig

def correlacao():

    # Criando paleta de cores
    colors = ['#EA746F',  # vermelho
            '#FFFFFF',  # branco
            '#9AC145']  # verde claro (mint green / light green)

    custom_cmap = mcolors.LinearSegmentedColormap.from_list("lilas_branco_verde", colors)

    # Criando gráfico
    corr = (df.drop(columns=['Etiqueta'])).corr(method="spearman")

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

df = pd.read_csv("Neuromath/Dados/Dados_v2.csv", sep = ",")
#df['DAt (BFP)'] = df['DAt (BFP)'].astype(int)

df['Etiqueta'] = df['Etiqueta'].str.replace('PAM01', 'Funcionamento PNa Existente - PAM01')
df['Etiqueta'] = df['Etiqueta'].str.replace('Valores Esperados', 'Funcionamento PNa Esperado')
df['Etiqueta'] = df['Etiqueta'].str.replace('Valores de Referência', 'Funcionamento PNa de Referência')

categorias = ['Funcionamento PNa Esperado', 'Funcionamento PNa de Referência', 'Funcionamento PNa Existente - PAM01']

df_red = df[df['Etiqueta'].isin(categorias)]

col1, col2 = st.columns(2)

# Gráfico 1

with col1:
    with st.container(height=600, border=True):
        st.markdown("<h3 style='text-align: center;'>Visualização dos resultados dos testes</h3>", unsafe_allow_html=True)
        fig_radar = radar(df)
        st.plotly_chart(fig_radar, use_container_width=True)

# Gráfico 2

with col2:
    with st.container(height=600, border=True):
        st.markdown("<h3 style='text-align: center;'>Correlação entre os testes</h3>", unsafe_allow_html=True)
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