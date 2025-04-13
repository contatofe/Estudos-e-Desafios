import streamlit as st
import pytesseract
from PIL import Image
import pandas as pd
from datetime import datetime
import re

pytesseract.pytesseract.tesseract_cmd = 'tesseract'  # Padrão para Linux/macOS

# Inicializa o estado da sessão
if 'data' not in st.session_state:
    st.session_state.data = []
if 'last_uploaded' not in st.session_state:
    st.session_state.last_uploaded = None

# Função para extrair texto da imagem usando OCR em português
def extract_text_from_image(image):
    try:
        # Configura o idioma para português (por)
        text = pytesseract.image_to_string(image, lang='por')
        return text
    except Exception as e:
        st.error(f"Erro ao processar a imagem: {e}")
        return ""

# Função para extrair números isolados do texto
def extract_numbers(text):
    numbers = re.findall(r'\b\d+\b', text)
    return ", ".join(numbers)

# Função principal do aplicativo
def main():
    st.title("Aplicativo OCR com Streamlit")

    # Upload de imagem
    uploaded_file = st.file_uploader("Faça upload de uma imagem", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Imagem carregada", use_container_width=True)

        # Checar se o arquivo já foi processado
        if uploaded_file.name != st.session_state.last_uploaded:
            # Extrair texto
            extracted_text = extract_text_from_image(image)
            st.subheader("Texto extraído:")
            st.write(extracted_text)

            # Extrair números
            numbers = extract_numbers(extracted_text)
            st.subheader("Números encontrados:")
            st.write(numbers)

            # Salvar dados
            new_entry = {
                "Data/Hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "Conteúdo Completo": extracted_text,
                "Números": numbers
            }
            st.session_state.data.append(new_entry)
            st.session_state.last_uploaded = uploaded_file.name
        else:
            st.info("Este arquivo já foi processado.")

    # Exibir tabela com histórico
    if st.session_state.data:
        st.subheader("Registros salvos:")
        df = pd.DataFrame(st.session_state.data)
        st.table(df)

        # Botão para exportar CSV
        if st.button("Exportar para Excel"):
            df.to_excel("registros_ocr.xlsx", index=False)
            st.success("Arquivo Excel salvo com sucesso!")

if __name__ == "__main__":
    main()
