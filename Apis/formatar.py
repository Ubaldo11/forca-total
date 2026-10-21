import re

try:
    from Apis.treino import gerar_treino
except ImportError:
    from treino import gerar_treino


def limpar_html(texto):
    if not texto:
        return ''
    texto = re.sub(r'<[^>]+>', '', texto)   # remove todas as tags
    texto = re.sub(r'\s+', ' ', texto)       # junta espaços/quebras em um só
    return texto.strip()


def formatar_exercicios(dados):
    lista = []

    for ex in dados['results']:
        # procura a tradução em inglês (language == 2)
        traducao = None
        for t in ex['translations']:
            if t['language'] == 2:
                traducao = t
                break

        # se não achou tradução em inglês, pula esse exercício
        if traducao is None:
            continue

        lista.append({
            'nome': traducao['name'],
            'descricao': limpar_html(traducao['description']),
            'imagem': ex['images'][0]['image'] if ex['images'] else None,
        })

    return lista


if __name__ == '__main__':
    dados = gerar_treino('costa')
    resultado = formatar_exercicios(dados)
    for item in resultado:
        print(item)