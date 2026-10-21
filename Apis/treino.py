import requests

url = 'https://wger.de/api/v2/exerciseinfo/'

def gerar_treino(grupo_muscular):
    if grupo_muscular == 'abs':
        musculo = 6

    elif grupo_muscular == 'bracos':
        musculo = 1

    elif grupo_muscular == 'costa':
        musculo = 12

    elif grupo_muscular == 'panturrilha':
        musculo = 11

    elif grupo_muscular == 'peito':
        musculo = 4

    elif grupo_muscular == 'perna':
        musculo = 10

    elif grupo_muscular == 'ombro':
        musculo = 2

    parametros = {
    "muscles": musculo,
    "limit": 5,
    }

    resposta = requests.get(url, params=parametros)
    dados = resposta.json()

    return dados