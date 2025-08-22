import json
from flask import jsonify
import re
import google.generativeai as genai
import os

os.environ['API_KEY'] = "AIzaSyAPOGkZ9DKYNvHpPffmPDEuAqYM9TCDKqA"
genai.configure(api_key=os.environ['API_KEY'])

model = genai.GenerativeModel('gemini-2.5-pro')

list_criterios = ['documento SEI','definição do objeto', 'prazo de contrato', 'justificativa da contratação',
                  'descrição da solução', 'requisitos da contratação', 'modelo de execução', 'modelo de gestão do contrato',
                  'pagamento', 'seleção do fornecedor', 'valor da contratação', 'adequação orçamentária', 'habilitação técnica',
                  'habilitação econômico-financeira']

with open(f'C:\\Users\\luiss\\PycharmProjects\\generative_ai\\app\\model_redacoes\\pagamento.txt', 'r', encoding='utf-8') as modelo:
    modelo_pagamento = modelo.read()


def file_tr(path):
    sample_file = genai.upload_file(path = path, display_name = 'TR em análise')
    print(f"Arquivo '{sample_file.display_name}' submetido")
    return sample_file

#analise de acordo com o modelo do Gemini
def analise_tr(sample_file):
    #sample_analysis = file_tr(sample_file)
    sample_analysis = sample_file
    resume = model.generate_content([sample_analysis, f"Analise o documento e informe o tipo de objeto (comum ou tecnologia da informação) a ser adequirido"],
                                    generation_config=genai.GenerationConfig(temperature = 0.5))# temperature o mais o objetivo possível

    response = model.generate_content([sample_analysis, f"Analise se os seguintes critérios '{list_criterios}' no documento submetido estão presentes e apresente o resultado como tópicos"],
                                    generation_config=genai.GenerationConfig(temperature=1.5) #colocando a taxa de "criatividade" dele bem baixa
                                       )
    #patterns = model.generate_content([sample_analysis, f"Analise se as redações presentes em {modelo_pagamento} estão presentes, considerando pequenas variações."])

    analysis = model.generate_content([response.text, f"Gere um documento somente com as falhas identificadas"], generation_config =
                                      genai.GenerationConfig(temperature = 1.5)) #colocando a taxa de "criatividade" dele bem baixa
    dict_results = {
        'resumo': resume.text,
        #'padrões': patterns.text,
        'analise': response.text,
        'sugestoes': analysis.text
    }

    results = [resume.text, response.text, analysis.text]

    print(dict_results)

