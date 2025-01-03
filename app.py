import streamlit as st
from datetime import datetime
from utils.leitor import buscar_leitura, carregar_progresso, marcar_dia_lido, resetar_progresso
from utils.auth import autenticar_usuario, criar_usuario  # Importação de funções de autenticação

def mostrar_leitura(dia):
    """
    Exibe a leitura correspondente ao dia selecionado.
    """
    leitura = buscar_leitura(dia)
    if leitura:
        st.subheader(f"Leitura do dia {dia}")
        st.write(f"**Escritura:** {leitura.get('Escritura', 'Não disponível')}")
        st.write(f"**Catecismo:** {leitura.get('Catecismo', 'Não disponível')}")
    else:
        st.warning("Leitura não encontrada para o dia selecionado.")

def mostrar_progresso():
    """
    Exibe o progresso do usuário com base nos dias lidos.
    """
    progresso = carregar_progresso(st.session_state.usuario_token)
    dias_lidos = len(progresso["dias_lidos"])
    dias_totais = 365
    progresso_percentual = (dias_lidos / dias_totais) * 100

    st.progress(progresso_percentual / 100)
    st.write(f"Progresso: {dias_lidos} de {dias_totais} dias lidos ({progresso_percentual:.2f}%)")
    if dias_lidos > 0:
        dias_lidos_lista = ", ".join(map(str, sorted(progresso["dias_lidos"])))
        st.info(f"Dias lidos: {dias_lidos_lista}")
    else:
        st.info("Nenhum dia foi marcado como lido até agora.")

def interface_usuario():
    """
    Exibe a interface para o usuário logado.
    """
    mostrar_progresso()

    dia_selecionado = st.selectbox("Selecione o dia:", range(1, 366))
    mostrar_leitura(dia_selecionado)

    if st.button(f"Marcar o dia {dia_selecionado} como lido"):
        marcar_dia_lido(st.session_state.usuario_token, dia_selecionado)
        st.success(f"Dia {dia_selecionado} marcado como lido!")

    if st.button("Próximo Dia"):
        dia_proximo = dia_selecionado + 1
        if dia_proximo <= 365:
            mostrar_leitura(dia_proximo)
        else:
            st.warning("Você já alcançou o último dia de leitura.")

    if st.button("Resetar Progresso"):
        if resetar_progresso(st.session_state.usuario_token):
            st.success("Progresso resetado com sucesso.")
        else:
            st.error("Erro ao resetar progresso.")

def interface_login():
    """
    Exibe a interface para login e criação de conta.
    """
    pagina = st.radio("Escolha uma opção:", ["Login", "Criar conta"])

    if pagina == "Login":
        email = st.text_input("Email")
        senha = st.text_input("Senha", type="password")
        if st.button("Entrar"):
            user = autenticar_usuario(email, senha)
            if user:
                st.session_state.usuario_email = email
                st.session_state.usuario_token = user["idToken"]
                st.success(f"Bem-vindo, {email}!")
            else:
                st.error("Email ou senha incorretos.")

    elif pagina == "Criar conta":
        novo_email = st.text_input("Email")
        nova_senha = st.text_input("Escolha uma senha", type="password")
        confirmacao_senha = st.text_input("Confirme a senha", type="password")
        if st.button("Criar conta"):
            if nova_senha != confirmacao_senha:
                st.error("As senhas não coincidem.")
            else:
                user = criar_usuario(novo_email, nova_senha)
                if user:
                    st.success(f"Conta criada com sucesso para {novo_email}! Faça login para continuar.")
                else:
                    st.error("Erro ao criar conta.")

def main():
    """
    Função principal do aplicativo.
    """
    st.title("Acompanhamento de Leitura - Bíblia e Catecismo")

    if "usuario_email" in st.session_state and "usuario_token" in st.session_state:
        st.sidebar.title(f"Bem-vindo, {st.session_state.usuario_email}!")
        interface_usuario()
    else:
        interface_login()

if __name__ == "__main__":
    main()
