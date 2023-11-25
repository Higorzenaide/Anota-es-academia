# exemplo.py
import streamlit as st
from datetime import datetime, timedelta
from functionsAll import fazerLogin,verificar_login,definir_login,enviar_respostas_google_forms
import requests

def main():
    # Verifica se o usuário está logado
    if not verificar_login():
        st.warning("Você não está logado ou seu tempo de sessão expirou. Faça o login novamente.")
        return

    # Conteúdo da página que só deve ser exibido se o usuário estiver logado
    st.title("Regitro de treino")

     # Select Box para escolher o dia da semana
    dias_semana = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta','Sábado','Domingo']
    dia_selecionado = st.selectbox("Escolha o dia da semana:", dias_semana)

    # Mostrar opções adicionais com base na seleção do dia
    if dia_selecionado == 'Segunda':
        exercicio = st.selectbox("Exercício para Segunda-feira:", ['Supino inclinado Smith 45°', 'Supino inclinado Halter Banco 30°', 'Supino Máquina','Supino inclinado nO Smith Banco 75°','Elevação lateral halter','paralela'])
    elif dia_selecionado == 'Terça':
        exercicio = st.selectbox("Exercício para Terça-feira:", ['Agachamento Livre / Smith','Leg press 45°','Cadeira extensora','Mesa flexora','Flexor em pé unilateral','Cadeira abdutora'])
    elif dia_selecionado == 'Quarta':
        exercicio = st.selectbox("Exercício para Quarta-feira:", ['Remada curvada','Remada baixa','Remana Máquina','Remada cavalinho','Crucifixo invertido máquina','Rosca direta banco 45°'])
    elif dia_selecionado == 'Quinta':
        exercicio = st.selectbox("Exercício para Quinta-feira:", ['Supino Reto','Crucifixo Inclinado Halter','Cross Over de baixo para cima','Desenvolvimento máquina pegada neutra','Elevação Lateral Unilateral no cross over','Supino Reto fechado'])
    elif dia_selecionado == 'Sexta':
        exercicio = st.selectbox("Exercício para Sexta-feira:", ['Levantamento terra','Hack Squat','Leg Press','Cadeira Flexora','Búlgaro'])
    elif dia_selecionado == 'Sábado':
        exercicio = st.selectbox("Exercício para Sexta-feira:", ['Barra fixa','Puxador frontal Supinado','Puxador frontal Neutro','Pull Dowwn com corda','Crucifixo invertido halter banco 45°','Rocas Martelo C/ Halter Simultaneo'])
    elif dia_selecionado == 'Domingo':
        exercicio = st.selectbox("Exercício para Sexta-feira:", ['Barra fixa','Puxador frontal Supinado','Puxador frontal Neutro','Pull Dowwn com corda','Crucifixo invertido halter banco 45°','Rocas Martelo C/ Halter Simultaneo'])
    else:
        exercicio = ""
    
    # Campo de número 1
    input_peso = st.number_input("Insira o peso:", min_value=0, max_value=100, value=0, step=10)
    input_repeticoes = st.number_input("Insira am quantidade de repetições:", min_value=0, max_value=100, value=0, step=10)


    # Botão para enviar o formulário
    if st.button("Enviar Formulário"):
        # Enviar dados para o Google Forms
        enviar_respostas_google_forms(dia_selecionado, exercicio, input_peso, input_repeticoes)
        # Exibindo os valores inseridos
        st.success(f"Dia selecionado: {dia_selecionado}")
        st.success(f"Exercício selecionado: {exercicio}")
        st.success(f"Kg ou Lbs: {input_peso}")
        st.success(f"Repetições: {input_repeticoes}")

if __name__ == '__main__':
    main()
