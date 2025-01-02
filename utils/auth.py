import json
import streamlit as st

# Função para carregar os dados de usuários
def carregar_usuarios():
    """
    Carrega os usuários do arquivo JSON.
    Se o arquivo não existir, retorna um dicionário vazio.
    """
    try:
        with open('data/users.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return{}
    
# Função para autenticar o usuário
def autenticar_usuario(username, password):
    """
    Verifica se o usuário existe e a senha está correta.
    """
    usuarios = carregar_usuarios()
    if username in usuarios and usuarios[username]['senha'] == password:
        return True
    return False

# Função para criar um novo usuário (opcional)
def criar_usuario(username, password):
    """
    Cria um novo usuário e adiciona ao arquivo de usuários.
    """
    usuarios = carregar_usuarios()

    if username in usuarios:
        return False #Usuário já existe
    
    usuarios[username] = {'senha': password}

    with open('data/users.json', 'w', encoding='utf-8') as file:
        json.dump(usuarios, file, indent=4)

    return True