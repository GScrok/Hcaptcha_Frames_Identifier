import google.generativeai as genai
import PIL
import json

from decouple import config
from utils import *

genai.configure(api_key=config('API_KEY'))

def consult_grid_gemini(): 
    img = PIL.Image.open(image_entire_captcha)


    model = genai.GenerativeModel("models/gemini-1.5-flash")

    response = model.generate_content(
    [
    '''
        Analise a seguinte imagem que contém:
        1. Uma modal central com uma grade 3x3 (9 quadros)
        2. Possivelmente uma imagem de referência (top) localizada:
           - À direita do texto
           - Acima da grade 3x3

        Retorne um JSON estruturado da seguinte forma:
        {
            "top": "descrição da imagem de referência" (se existir),
            "grid": {
                "1": "descrição do quadro 1",
                "2": "descrição do quadro 2",
                ...
                "9": "descrição do quadro 9"
            }
        }

        Observações:
        - Numere os quadros da esquerda para direita, de cima para baixo (1-9)
        - Forneça descrições sem muitos detalhes
        - Omita o campo "top" se não houver imagem de referência
    ''', 
    img
    ])

    response.resolve()
    json_convert = response.text.strip("(```)")
    json_convert = json_convert.replace('json\n', '', 1).replace('```','')
    print(json_convert)
    json_convert = json.loads(json_convert)
    
    return json_convert

def consult_gemini():
    answer_grid=consult_grid_gemini()

    img = PIL.Image.open(image_title_captcha)

    model = genai.GenerativeModel("models/gemini-1.5-flash")

    response = model.generate_content(
    [
    f'''
        Nessa imagem que estou te enviando, possui um título em cima de um Grid 3x3 de quadros com imagens.
        Se houver uma imagem ao lado do título, desconsidere.
        Com esse título e o Objeto que estou enviando, me retorne, APENAS UMA LISTA, contendo os números dos quadros corretos, 
        com as opções disponíveis, de 1 a 9, as quais estão corretas.
        Se possuir no Objeto abaixo um campo top diferente de None, leve ele em consideração para responder a pergunta do titulo.
        {answer_grid}
    
        EU NÃO DESEJO UMA FUNÇÃO, E SIM A RESPOSTA DA IMAGEM ANALISADA.
        
        O retorno esperado é uma lista com seus valores [n1, n2, ...], não tendo nenhuma outra mensagem ou palavra junto da lista.
    ''', 
    img
    ])

    response.resolve()
    
    response_filtered = filter_by_list(response.text.strip("(```)"))
    if not response_filtered:
        raise Exception('Não encontrou de relação do TITLE com o GRID.')
    
    return response_filtered

#Alter
image_entire_captcha = 'screenshot_hcaptcha.png'
image_title_captcha = 'screenshot_title_hcaptcha.png'


correct_answers = consult_gemini()
print(f"Os quadros corretos são: {', '.join(map(str, correct_answers))}")