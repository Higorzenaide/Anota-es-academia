# exemplo.py
import streamlit as st
from datetime import datetime, timedelta
from functionsAll import fazerLogin, verificar_login, definir_login, enviar_respostas_google_forms
import requests
import time
from decouple import config
import os
from functionsAll import SupabaseClient

def User(usuario):
    st.session_state.logado = usuario

# Obtenha as chaves da variável de ambiente
url = config('SUPABASE_URL')
key = config('SUPABASE_API_KEY')

def main():
    # Verifica se o usuário está logado
    if not verificar_login():
        st.warning("Você não está logado ou seu tempo de sessão expirou. Faça o login novamente.")
        return
    
    # Conteúdo da página que só deve ser exibido se o usuário estiver logado
    st.title("Registro de treino")

    # Layout em duas colunas
    col1, col2 = st.columns(2)

    # Coluna 1
    with col1:
        modo_de_treino = ['Solo/Alone', 'Dupla imbativel']
        modo_de_treino_select = st.selectbox("Escolha um modo de treino:", modo_de_treino)
        if modo_de_treino_select != 'Solo/Alone':
            StartOn = ['Higor','Rego']
            StartOn_Select = st.selectbox("Selecione com quem ira começar:",StartOn)

        semana_de_treino = ['Selecione', 'Semana 1', 'Semana 2', 'Semana 3', 'Semana 4']
        semana_de_treino_select = st.selectbox("Selecione qual semana está:", semana_de_treino)
        if semana_de_treino_select != 'Selecione':
            st.info("Serão 3 Séries cada exercício")
        else:
            return
        # Select Box para escolher o dia da semana
        dias_semana = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
        dia_selecionado = st.selectbox("Escolha o dia da semana:", dias_semana)


    # Coluna 2
    with col2:
        # Mostrar opções adicionais com base na seleção do dia
        if dia_selecionado == 'Segunda':
            exercicio = st.selectbox("Exercício para Segunda-feira:", ['Supino inclinado Smith 45°', 'Supino inclinado Halter Banco 30°', 'Supino Máquina', 'Supino inclinado no Smith Banco 75°', 'Elevação lateral halter', 'paralela'])
        elif dia_selecionado == 'Terça':
            exercicio = st.selectbox("Exercício para Terça-feira:", ['Agachamento Livre / Smith', 'Leg press 45°', 'Cadeira extensora', 'Mesa flexora', 'Flexor em pé unilateral', 'Cadeira abdutora'])
        elif dia_selecionado == 'Quarta':
            exercicio = st.selectbox("Exercício para Quarta-feira:", ['Remada curvada', 'Remada baixa', 'Remana Máquina', 'Remada cavalinho', 'Crucifixo invertido máquina', 'Rosca direta banco 45°'])
        elif dia_selecionado == 'Quinta':
            exercicio = st.selectbox("Exercício para Quinta-feira:", ['Supino Reto', 'Crucifixo Inclinado Halter', 'Cross Over de baixo para cima', 'Desenvolvimento máquina pegada neutra', 'Elevação Lateral Unilateral no cross over', 'Supino Reto fechado'])
        elif dia_selecionado == 'Sexta':
            exercicio = st.selectbox("Exercício para Sexta-feira:", ['Levantamento terra', 'Hack Squat', 'Leg Press', 'Cadeira Flexora', 'Búlgaro'])
        elif dia_selecionado == 'Sábado':
            exercicio = st.selectbox("Exercício para Sábado:", ['Barra fixa', 'Puxador frontal Supinado', 'Puxador frontal Neutro', 'Pull Dowwn com corda', 'Crucifixo invertido halter banco 45°', 'Rocas Martelo C/ Halter Simultâneo'])
        elif dia_selecionado == 'Domingo':
            exercicio = st.selectbox("Exercício para Domingo:", ['Barra fixa', 'Puxador frontal Supinado', 'Puxador frontal Neutro', 'Pull Dowwn com corda', 'Crucifixo invertido halter banco 45°', 'Rocas Martelo C/ Halter Simultâneo'])
        else:
            exercicio = ""

        # Campo de número 1
        input_peso = st.number_input("Insira o peso:", min_value=0, max_value=100, value=0, step=10)
        input_repeticoes = st.number_input("Insira a quantidade de repetições:", min_value=0, max_value=100, value=0, step=2)

        if 'logado' not in st.session_state:
            st.session_state.logado = ''

        if 'enviar_no_nome_de' not in st.session_state:
            st.session_state.enviar_no_nome_de = ''

        if 'contador_series_validas' not in st.session_state:
            st.session_state.contador_series_validas = 0
        
        if 'contador_de_envio' not in st.session_state:
            st.session_state.contador_de_envio = 0

        if 'contador_de_series_Rego' not in st.session_state:
            st.session_state.contador_de_series_Rego = 0

        if 'contador_de_series_Higor' not in st.session_state:
            st.session_state.contador_de_series_Higor = 0

        if modo_de_treino_select != 'Solo/Alone':
            if st.session_state.contador_de_envio == 0:
                if StartOn_Select != '':
                    if StartOn_Select == 'Rego':
                        nome = ['Rego','Higor']
                        nome_select = st.selectbox("Enviar no nome de:", nome,disabled=True)
                    else:
                        nome = ['Higor','Rego']
                        nome_select = st.selectbox("Enviar no nome de:", nome,disabled=True)
            else:
                pass
            
            if st.session_state.enviar_no_nome_de != "":
                if  st.session_state.enviar_no_nome_de == 'Higor':
                    nome = ['Rego','Higor']
                    nome_select = st.selectbox("Enviar no nome de:", nome,disabled=True)
                else:
                    nome = ['Higor','Rego']
                    nome_select = st.selectbox("Enviar no nome de:", nome,disabled=True)
            else:
                pass
        
        contador_de_series_Semana01 = ['0/3','1/3','2/3','3/3']
        contador_de_series_Semana02_03_04 = [1,2,3,4]

        if semana_de_treino_select == 'Semana 1' and modo_de_treino_select == 'Solo/Alone':
            if st.session_state.contador_series_validas == 1:
                st.selectbox('Séries feitas',['1/3'],disabled=True)
            elif st.session_state.contador_series_validas == 2:
                st.selectbox('Séries feitas',['2/3'],disabled=True)
            elif st.session_state.contador_series_validas == 3:
                st.selectbox('Séries feitas',['3/3'],disabled=True)
        elif semana_de_treino_select == 'Semana 1' and modo_de_treino_select == 'Dupla imbativel':
            higor_options = [f'{st.session_state.contador_de_series_Higor}/3']
            rego_options = [f'{st.session_state.contador_de_series_Rego}/3']

            higor = st.selectbox('Séries feitas Higor', higor_options, key='higor', disabled=True)
            rego = st.selectbox('Séries feitas Rego', rego_options, key='rego', disabled=True)
        elif semana_de_treino_select == 'Semana 2' or semana_de_treino_select == 'Semana 3' or semana_de_treino_select == 'Semana 4'and modo_de_treino_select == 'Dupla imbativel':
            higor_options = [f'{st.session_state.contador_de_series_Higor}/4']
            rego_options = [f'{st.session_state.contador_de_series_Rego}/4']

            higor = st.selectbox('Séries feitas Higor', higor_options, key='higor', disabled=True)
            rego = st.selectbox('Séries feitas Rego', rego_options, key='rego', disabled=True)
        else:
            if st.session_state.contador_series_validas == 1:
                st.selectbox('Séries feitas',['1/4'],disabled=True)
            elif st.session_state.contador_series_validas == 2:
                st.selectbox('Séries feitas',['2/4'],disabled=True)
            elif st.session_state.contador_series_validas == 3:
                st.selectbox('Séries feitas',['3/4'],disabled=True)
            elif st.session_state.contador_series_validas == 3:
                st.selectbox('Séries feitas',['4/4'],disabled=True)

        # Botão para enviar o formulário
        if st.button("Enviar Formulário"):
            if modo_de_treino_select != 'Solo/Alone':
                if nome_select == 'Higor':
                    if semana_de_treino_select == 'Semana 1':
                        st.session_state.contador_de_series_Higor += 1
                        if st.session_state.contador_de_series_Higor == 4:
                            st.session_state.contador_de_series_Higor = 1
                    else:
                        st.session_state.contador_de_series_Higor += 1
                        if st.session_state.contador_de_series_Higor == 5:
                            st.session_state.contador_de_series_Higor = 1
                elif nome_select == 'Rego':
                    if semana_de_treino_select == 'Semana 1':
                        st.session_state.contador_de_series_Rego += 1
                        if st.session_state.contador_de_series_Rego == 4:
                            st.session_state.contador_de_series_Rego = 1
                    else:
                        st.session_state.contador_de_series_Rego += 1
                        if st.session_state.contador_de_series_Rego == 5:
                            st.session_state.contador_de_series_Rego = 1
                else:
                    pass
            
            if st.session_state.contador_de_envio == 0:
                if st.session_state.contador_de_envio == 1:
                    pass
                else:
                    st.session_state.contador_de_envio +=1
            if modo_de_treino_select != 'Solo/Alone':
                st.session_state.enviar_no_nome_de = nome_select
            
            if semana_de_treino_select == 'Semana 1':
                st.session_state.contador_series_validas += 1
                if st.session_state.contador_series_validas == 4:
                    st.session_state.contador_series_validas = 1
            else:
                st.session_state.contador_series_validas += 1
                if st.session_state.contador_series_validas == 4:
                    st.session_state.contador_series_validas = 1
            # Enviar dados para o Google Forms
            if modo_de_treino_select == 'Dupla imbativel':
                enviar_respostas_google_forms(st.session_state.enviar_no_nome_de,dia_selecionado, exercicio, input_peso, input_repeticoes)
            else:
                enviar_respostas_google_forms(st.session_state.logado,dia_selecionado, exercicio, input_peso, input_repeticoes)
            
            # Exibir as mensagens de sucesso
            mensagem_dia = st.empty()

            # Atualizar as mensagens com os dados
            mensagem_dia.success(f"Adiconado ao formulário com sucesso")
            st.success(f'{st.session_state.enviar_no_nome_de}')

            # Esperar alguns segundos
            time.sleep(2)

            # Limpar as mensagens
            mensagem_dia.empty()

            # Usar st.modal para criar um pop-up
            st.experimental_rerun()  # Força a atualização da interface

if __name__ == '__main__':
    main()
