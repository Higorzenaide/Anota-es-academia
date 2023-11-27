import streamlit as st
from datetime import datetime, timedelta
import requests
from decouple import config
from supabase import create_client, Client
import time


# Obtenha as chaves da variável de ambiente
url = config('SUPABASE_URL')
key = config('SUPABASE_API_KEY')
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
    limite_tempo = timedelta(minutes=120)

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

def enviar_respostas_google_forms(user,dia_selecionado, exercicio, input_peso, input_repeticoes):
    # URL do formulário do Google
    url1 = f"https://docs.google.com/forms/u/0/d/e/1FAIpQLSetIvUgWSuMknDsK9Gkvg5NQPb7A22_pIy14tRLA4pEqNhgSA/formResponse?entry.611076805={dia_selecionado}&entry.1910590682={exercicio}&entry.720687172={input_peso}&entry.629247611={input_repeticoes}"
    url2 = f"https://docs.google.com/forms/u/0/d/e/1FAIpQLSfC_w_VWmRC7eF9aVtxBnasl7lwXykDJ_m1YiFlsrH6NzdOLQ/formResponse?entry.99674157={dia_selecionado}&entry.653917994={exercicio}&entry.582363435={input_peso}&entry.1904628187={input_repeticoes}"
    # Enviar a requisição GET para o formulário
    
    if user == 'Higor':
        response = requests.get(url2)
        st.success("Enviei no Higor")
    else:
        response = requests.get(url1)
        st.success("Enviei no Rego")

    # Verificar se a requisição foi bem-sucedida (código de status 200)
    if response.status_code == 200:
        print("Dados enviados com sucesso para o formulário!")
    else:
        print("Erro ao enviar dados para o formulário. Código de status:", response.status_code)
        print(response.text)


class SupabaseClient:
    def __init__(self, url, key):
        self.url = url
        self.key = key
        self.supabase = None

    def create_client(self):
        try:
            self.supabase = create_client(self.url, self.key)
            if self.supabase:
                print("Cliente Supabase criado com sucesso!")
            else:
                print("Erro ao criar o cliente Supabase.")
        except Exception as e:
            print(f"Erro: {e}")

    def login(self, email, password):
        try:
            if self.supabase:
                res = self.supabase.auth.sign_up({
                    "email": email,
                    "password": password
                })
                if res['user']:
                    print(f"Usuário {email} autenticado com sucesso!")
                else:
                    print("Erro ao autenticar o usuário.")
            else:
                print("Cliente Supabase não foi inicializado.")
        except Exception as e:
            print(f"Erro ao autenticar o usuário: {e}")
