import streamlit as st
import google.generativeai as genai
import os
import requests

os.environ['API_KEY'] = "AIzaSyAPOGkZ9DKYNvHpPffmPDEuAqYM9TCDKqA"
genai.configure(api_key=os.environ['API_KEY'])
pagamento_google = "https://drive.google.com/file/d/1wN3Rgr-3MSW6VBQw64svVsLhSa_SGcmL/view?usp=drive_link"

st.title('Análise de editais')

st.text("Essa ferramenta busca analisar se o Termo de Referência submetido possui os requisitos mínimos propostos pela Lei nº 14.133/2021.")

st.header("Upload Termo de Referência")
uploaded_file = st.file_uploader("Termo de Referência", type=['pdf'])


if uploaded_file is not None:
    temp_dir = "temp_uploads"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    temp_file_path = os.path.join(temp_dir, uploaded_file.name)

    with open(temp_file_path, 'wb') as f:
        f.write(uploaded_file.getbuffer())

    with st.spinner('Processando...'):
        uploaded_file_gemini = genai.upload_file(path=temp_file_path, display_name = uploaded_file.name)
        st.spinner("Analisando:")

        model = genai.GenerativeModel('gemini-2.5-flash')
        list_criterios = ['Definição do objeto', 'Prazo de contrato', 'Justificativa da contratação',
                          'Descrição da solução', 'Requisitos da contratação', 'Modelo de execução',
                          'Modelo de gestão do contrato',
                          'Pagamento', 'Seleção do fornecedor', 'Valor da contratação', 'Adequação orçamentária',
                          'Habilitação técnica',
                          'Habilitação econômico-financeira', 'microempresas e empresas de pequeno porte']

        analysis = model.generate_content([uploaded_file_gemini, f"Analise se os seguintes critérios '{list_criterios}' no documento submetido estão presentes e apresente o resultado como tópicos em português brasileiro"]
                                          , generation_config=genai.GenerationConfig(temperature=1.5))



    st.subheader("Resultados")
    st.write(analysis.text)



