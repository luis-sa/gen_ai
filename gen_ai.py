import json
from flask import jsonify
import re
import google.generativeai as genai
import os

os.environ['API_KEY'] = "AIzaSyAPOGkZ9DKYNvHpPffmPDEuAqYM9TCDKqA"
genai.configure(api_key=os.environ['API_KEY'])

model = genai.GenerativeModel('gemini-1.5-flash-latest')
list_criterios = ['documento SEI','definição do objeto', 'prazo de contrato', 'justificativa da contratação',
                  'descrição da solução', 'requisitos da contratação', 'modelo de execução', 'modelo de gestão do contrato',
                  'pagamento', 'seleção do fornecedor', 'valor da contratação', 'adequação orçamentária', 'habilitação técnica',
                  'habilitação econômico-financeira']

# faz upload do arquivo a ser analisado
'''def file_tr(path):
    regex = r"^./uploads/"
    name_file = re.sub(regex, "", path)
    name_file = name_file.removesuffix('.pdf')

    def check_file_exists(name_file):
        try:
            file_info = genai.get_file(name = name_file)
            if file_info:
                return True
            else: return False
        except Exception as e:
            print(f'Erro ao validar arquivo: {str(e)}')
            return False
    if check_file_exists(name_file = name_file):
        sample_file = genai.get_file(name = name_file)
        return sample_file
    else:
        try:
            name_file = path.removesuffix('.pdf')
            sample_file = genai.upload_file(path = path, display_name = 'doc_analise', name = name_file)
            print(f'Upload realizado: {sample_file.display_name}')
            return sample_file
        except Exception as e:
            print(f'Erro {e}')'''

def file_tr(path):
    sample_file = genai.upload_file(path = path, display_name = 'TR em análise')
    print(f"Arquivo '{sample_file.display_name}' submetido")
    return sample_file

#analise de acordo com o modelo do Gemini
def analise_tr(sample_file):
    sample_analysis = file_tr(sample_file)
    resume = model.generate_content([sample_analysis, f"Analise o documento e informe o tipo de objeto (comum ou tecnologia da informação) a ser adequirido"],
                                    generation_config=genai.GenerationConfig(temperature = 0.5))# temperature o mais o objetivo possível

    response = model.generate_content([sample_analysis, f"Analise se os seguintes critérios '{list_criterios}' no documento submetido estão presentes e apresente o resultado como tópicos"],
                                    generation_config=genai.GenerationConfig(temperature=1.5) #colocando a taxa de "criatividade" dele bem baixa
                                       )
    analysis = model.generate_content([response.text, f"Gere um documento somente com as falhas identificadas"], generation_config =
                                      genai.GenerationConfig(temperature = 1.5)) #colocando a taxa de "criatividade" dele bem baixa
    dict_results = {
        'resumo': resume.text,
        'analise': response.text,
        'sugestoes': analysis.text
    }

    results = [resume.text, response.text, analysis.text]

    return jsonify({'message': results})#tenho que corrigir a saída. tá bagunçado.

analise_tr('tr-pe11.pdf')