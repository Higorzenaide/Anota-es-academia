import streamlit as st
from datetime import datetime, timedelta
from functionsAll import fazerLogin,verificar_login,definir_login


def main():
    # Verifica se o usuário está logado
    if verificar_login():
        st.success("Você já está logado!")

    # Se não estiver logado ou se o tempo de sessão expirou, exibe o formulário de login
    else:
        with st.form(key="include_senha"):
            input_name = st.text_input(label="Insira o seu nome")
            input_pass = st.text_input(label="Insira a sua senha", type="password")
            input_button = st.form_submit_button("Logar")

        if input_button:
            retorno = fazerLogin(input_name, input_pass)
            if retorno:
                definir_login(True)
                st.success("Login efetuado")
            else:
                st.error("Tente novamente")

if __name__ == '__main__':
    main()
