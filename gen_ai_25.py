import google.generativeai as genai
import os

os.environ['API_KEY'] = "AIzaSyAPOGkZ9DKYNvHpPffmPDEuAqYM9TCDKqA"
genai.configure(api_key=os.environ['API_KEY'])

model = genai.GenerativeModel('gemini-2.5-pro')

try:
    sample_file = genai.upload_file('C:\\Users\\luiss\\PycharmProjects\\generative_ai\\app\\uploads\\SEI_172602089_Termo_de_Referencia_21.pdf')
    print('Arquivo enviado com sucesso!')

except Exception as e:
    print(e)

with open(f'C:\\Users\\luiss\\PycharmProjects\\generative_ai\\app\\model_redacoes\\pagamento.txt', 'r', encoding='utf-8') as modelo:
    modelo_pagamento = modelo.read()

requisitos_lei = ['definição do objeto', 'prazo de contrato', 'justificativa da contratação',
                  'descrição da solução', 'requisitos da contratação', 'modelo de execução', 'modelo de gestão do contrato',
                  'pagamento', 'seleção do fornecedor', 'valor da contratação', 'adequação orçamentária', 'habilitação técnica',
                  'habilitação econômico-financeira', 'previsão no plano anual de contratações', 'participação de microempresas e empresas de pequeno porte']

prompt_completo = f"""
    O objeto da análise é verificar se o Termo de Referência a ser inserido conta com todas as informações necessárias 
    para atendimento a lei. É necessário que analise se contém os requisitos mínimos definidos pela legislação. 
    
    ** Requisitos da Lei **
    {requisitos_lei}
    
    Analise o documento e me diga se constam os "Requisitos da Lei". Apresente o resultado como um texto com tudo o que foi identificado e aqueles faltantes.
    
    Documento a ser analisado: {sample_file.uri}
"""

response = model.generate_content(prompt_completo)
print(response)