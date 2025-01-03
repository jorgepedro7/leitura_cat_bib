# import json
# import os

# # Função para carregar as leituras
# def carregar_lecturas():
#     with open('data/leitura.json', 'r', encoding='utf-8') as file:
#         data = json.load(file)
#     return data

# # Função para carregar o progresso
# def carregar_progresso():
#     try:
#         with open('data/progresso.json', 'r', encoding='utf-8') as file:
#             progresso = json.load(file)
#     except FileNotFoundError:
#         progresso = {"dias_lidos": []}
#         salvar_progresso(progresso)  # Cria o arquivo de progresso se não existir
#     return progresso

# # Função para salvar o progresso
# def salvar_progresso(progresso):
#     with open('data/progresso.json', 'w', encoding='utf-8') as file:
#         json.dump(progresso, file, indent=4)

# # Função para obter a leitura do dia
# def obter_lectura_do_dia(Data):
#     data = carregar_lecturas()
#     for lectura in data:
#         if lectura['Data'] == Data:
#             return lectura
#     return None

# # Função para marcar o dia como lido
# def marcar_dia_lido(Data):
#     progresso = carregar_progresso()
#     if Data not in progresso["dias_lidos"]:
#         progresso["dias_lidos"].append(Data)
#         salvar_progresso(progresso)

# # Função de resetar progresso
# def resetar_progresso():
#     """
#     Reseta o progresso da leitura, apagando o arquivo 'progresso.json'.
#     """
#     if os.path.exists('data/progresso.json'):
#         os.remove('data/progresso.json')
#         return "Progresso resetado com sucesso."
#     else:
#         return "Arquivo de progresso não encontrado."
from firebase_config import db
import json

COLECAO_PROGRESSO = "progresso"

def carregar_leituras():
    try:
        with open('data/leitura.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def carregar_progresso(usuario_id):
    doc_ref = db.collection(COLECAO_PROGRESSO).document(usuario_id)
    try:
        doc = doc_ref.get()
        return doc.to_dict() if doc.exists else {"dias_lidos": []}
    except Exception as e:
        print(f"Erro ao carregar progresso: {e}")
        return {"dias_lidos": []}

def salvar_progresso(usuario_id, progresso):
    try:
        db.collection(COLECAO_PROGRESSO).document(usuario_id).set(progresso)
    except Exception as e:
        print(f"Erro ao salvar progresso: {e}")

def marcar_dia_lido(usuario_id, dia):
    progresso = carregar_progresso(usuario_id)
    if dia not in progresso["dias_lidos"]:
        progresso["dias_lidos"].append(dia)
        salvar_progresso(usuario_id, progresso)

def resetar_progresso(usuario_id):
    try:
        db.collection(COLECAO_PROGRESSO).document(usuario_id).set({"dias_lidos": []})
        return True
    except Exception as e:
        print(f"Erro ao resetar progresso: {e}")
        return False

def buscar_leitura(dia):
    leituras = carregar_leituras()
    return next((l for l in leituras if l['Data'] == dia), None)
