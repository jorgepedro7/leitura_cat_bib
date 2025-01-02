import streamlit as st
from utils.leitor import obter_lectura_do_dia, marcar_dia_lido, carregar_progresso, resetar_progresso
from datetime import datetime
from utils.auth import autenticar_usuario, criar_usuario  # Importando as funções de autenticação

# Função para mostrar a leitura do dia
def mostrar_lectura(Data):
    lectura = obter_lectura_do_dia(Data)
    if lectura:
        st.subheader(f"Leitura do dia {Data}")
        st.write(f"Escritura: {lectura.get('Escritura', 'Não disponível')}")
        st.write(f"Catecismo: {lectura.get('Catecismo', 'Não disponível')}")
    else:
        st.warning("Leitura não encontrada para o dia selecionado.")

# Função para mostrar o progresso
def mostrar_progresso():
    progresso = carregar_progresso()
    dias_lidos = len(progresso["dias_lidos"])
    dias_totais = 365
    progresso_percentual = (dias_lidos / dias_totais) * 100
    progresso_percentual = min(progresso_percentual, 100)
    
    st.progress(progresso_percentual / 100)
    st.write(f"Progresso: {dias_lidos} de {dias_totais} dias lidos ({progresso_percentual:.2f}%)")
    
    dias_lidos_lista = ", ".join(map(str, sorted(progresso["dias_lidos"])))
    if dias_lidos_lista:
        st.info(f"Dias lidos: {dias_lidos_lista}")
    else:
        st.info("Nenhum dia foi marcado como lido até agora.")

# Função principal com login e criação de usuário
def main():
    st.title("Acompanhamento de Leitura - Bíblia e Catecismo")

    # Verificar se o usuário está logado
    usuario_logado = st.session_state.get("usuario", None)

    if usuario_logado:
        # Mostrar nome do usuário na barra superior
        st.sidebar.title(f"Bem-vindo, {usuario_logado}!")

        # Mostrar progresso de leitura
        mostrar_progresso()
        
        # Seleção de dia
        dias_disponiveis = [str(d) for d in range(1, 366)]  
        dia_selecionado = st.selectbox("Selecione o dia:", dias_disponiveis)
        
        # Mostrar leitura do dia selecionado
        mostrar_lectura(int(dia_selecionado))
        
        # Botão para marcar o dia como lido
        if st.button(f"Marcar o dia {dia_selecionado} como lido"):
            marcar_dia_lido(int(dia_selecionado))
            st.success(f"Dia {dia_selecionado} marcado como lido.")
        
        # Botão para o próximo dia
        if st.button('Próximo Dia'):
            dia_proximo = int(dia_selecionado) + 1
            if dia_proximo <= 365:
                mostrar_lectura(dia_proximo)
            else:
                st.warning("Você já alcançou o último dia de leitura.")

        # Botão para resetar o progresso
        if st.button("Resetar Progresso"):
            resetar_progresso()
            st.success("Progresso resetado com sucesso.")

    else:
        # Se não estiver logado, exibir opções de login e criação de conta
        pagina = st.radio("Escolha uma opção", ["Login", "Criar conta"])

        if pagina == "Login":
            # Formulário de login
            usuario = st.text_input("Nome de usuário")
            senha = st.text_input("Senha", type='password')

            if st.button("Entrar"):
                if autenticar_usuario(usuario, senha):
                    # Salvar o usuário logado no session_state
                    st.session_state.usuario = usuario
                    st.success(f"Bem-vindo, {usuario}!")
                    
                else:
                    st.error("Usuário ou senha incorretos.")

        elif pagina == "Criar conta":
            # Formulário de criação de usuário
            novo_usuario = st.text_input("Escolha um nome de usuário")
            nova_senha = st.text_input("Escolha uma senha", type='password')
            confirmacao_senha = st.text_input("Confirme a senha", type='password')

            if st.button("Criar conta"):
                if nova_senha != confirmacao_senha:
                    st.error("As senhas não coincidem.")
                else:
                    if criar_usuario(novo_usuario, nova_senha):
                        st.success(f"Conta criada com sucesso para {novo_usuario}! Agora faça login.")
                    else:
                        st.error(f"Usuário {novo_usuario} já existe. Escolha outro nome de usuário.")

if __name__ == "__main__":
    main()
