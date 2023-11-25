import streamlit as st
from datetime import datetime, timedelta
import requests
nome01 = "Rego"
nome02 = "Higor"
senha = "projetinho2024@"

def fazerLogin(nome,senhaLogin):
    if nome == nome01 or nome == nome02 and senhaLogin == senha:
        return True
    else:
        return False

# Função para verificar o login
def verificar_login():
    ultimo_login = st.session_state.get("ultimo_login", 0)
    diferenca_tempo = datetime.now() - datetime.fromtimestamp(ultimo_login)
    limite_tempo = timedelta(minutes=30)

    # Verifica se o tempo desde o último login é inferior ao limite
    if diferenca_tempo < limite_tempo:
        return st.session_state.get("logado", False)
    else:
        # Se o tempo expirou, faz logout
        st.session_state.logado = False
        st.session_state.ultimo_login = 0
        return False

# Função para definir o status de login
def definir_login(status):
    st.session_state.logado = status
    st.session_state.ultimo_login = datetime.now().timestamp()

def enviar_respostas_google_forms(dia_selecionado, exercicio, input_peso, input_repeticoes):
    # URL do formulário do Google
    url = f"https://docs.google.com/forms/u/0/d/e/1FAIpQLSetIvUgWSuMknDsK9Gkvg5NQPb7A22_pIy14tRLA4pEqNhgSA/formResponse?entry.611076805={dia_selecionado}&entry.1910590682={exercicio}&entry.720687172={input_peso}&entry.629247611={input_repeticoes}"

    # Enviar a requisição GET para o formulário
    response = requests.get(url)

    # Verificar se a requisição foi bem-sucedida (código de status 200)
    if response.status_code == 200:
        print("Dados enviados com sucesso para o formulário!")
    else:
        print("Erro ao enviar dados para o formulário. Código de status:", response.status_code)
        print(response.text)
