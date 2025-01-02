import json
import os

# Função para carregar as leituras
def carregar_lecturas():
    with open('data/leitura.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

# Função para carregar o progresso
def carregar_progresso():
    try:
        with open('data/progresso.json', 'r', encoding='utf-8') as file:
            progresso = json.load(file)
    except FileNotFoundError:
        progresso = {"dias_lidos": []}
        salvar_progresso(progresso)  # Cria o arquivo de progresso se não existir
    return progresso

# Função para salvar o progresso
def salvar_progresso(progresso):
    with open('data/progresso.json', 'w', encoding='utf-8') as file:
        json.dump(progresso, file, indent=4)

# Função para obter a leitura do dia
def obter_lectura_do_dia(Data):
    data = carregar_lecturas()
    for lectura in data:
        if lectura['Data'] == Data:
            return lectura
    return None

# Função para marcar o dia como lido
def marcar_dia_lido(Data):
    progresso = carregar_progresso()
    if Data not in progresso["dias_lidos"]:
        progresso["dias_lidos"].append(Data)
        salvar_progresso(progresso)

# Função de resetar progresso
def resetar_progresso():
    """
    Reseta o progresso da leitura, apagando o arquivo 'progresso.json'.
    """
    if os.path.exists('data/progresso.json'):
        os.remove('data/progresso.json')
        return "Progresso resetado com sucesso."
    else:
        return "Arquivo de progresso não encontrado."
