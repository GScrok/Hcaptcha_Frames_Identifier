import google.generativeai as genai
import PIL


from decouple import config
from utils import *

genai.configure(api_key=config('API_KEY'))
model = genai.GenerativeModel("models/gemini-2.0-flash-exp")


def consult_gemini():
    img = PIL.Image.open(image_entire_captcha)

    response = model.generate_content(
    [
    '''
        Analise a seguinte imagem que contém:
        1. Uma modal central com uma grade 3x3 (9 quadros)
        2. Um título acima da grade 3x3
        3. Possivelmente uma imagem de referência localizada:
           - À direita do titulo
           - Acima da grade 3x3

        INTERPRETE o título para encontrar o alvo ÚNICO da imagem. 
        Exemplo 1, se no título for socilitado que é para clicar em um OBJETO, você vai me retornar a descrição do objeto INANIMADO e ignorará os demais elementos.
        Exemplo 2, se no título for socilitado que é para clicar em um ANIMAL, você vai me retornar a descrição do animal VIVO e ignorará os demais elementos
        
        Realize a descrição dessas imagens nesse formato desejado:
        {
            titulo: 'Descrição do título',
            imagem_referencia: 'Alvo da imagem de referência (caso exista, senão nulo), com descrição prescisa',
            quadro_1: 'Descrição do quadro 1'
        }
        

        Observações:
        - Numere os quadros da esquerda para direita, de cima para baixo (1-9)
        - Faça uma descrição RELEVANTE das imagens
        - Os objetos que aparecem na imagem de referencia, eles não tem relação entre si
        - Na imagem de referencia (caso exista), me retorne apenas o alvo principal dela e não a descrição completa
    ''', 
        # - O retorno esperado é uma lista com seus valores [n1, n2, ...]
        # - Não retorne nenhuma mensagem ou explicação além da lista
        # - Forneça descrições das imagens sem muitos detalhes
        # - O retorno esperado é uma lista com seus valores [n1, n2, ...].
    img
    ])

    response.resolve()
    frames_described_dict = convert_response(response.text)
    # pprint.pprint(frames_described_dict)

    response = model.generate_content(
    [
    f'''
        Analise o seguinte dicionário que contém:
        1. Um título indicando o que deve ser feito
        2. Uma possível imagem de referência.
        3. Nove quadros com suas descrições

        Preciso que você interprete o texto com a imagem de referência (caso exista), e me retorne o número dos quadros que estão
        de acordo com eles.

        {frames_described_dict}

        Observações:
        - O retorno esperado é uma lista com seus valores [n1, n2, ...]
        - Não retorne nenhuma mensagem ou explicação além da lista
    '''
    ])

    response.resolve()
    frames_correct_list = convert_response(response.text)
    # pprint.pprint(frames_correct_list)
    return frames_correct_list
    
#Alter
image_entire_captcha = 'screenshot_hcaptcha_example.png'


correct_answers = consult_gemini()
print(f"Os quadros corretos são: {', '.join(map(str, correct_answers))}")