import streamlit as st
import pandas as pd
import datetime

# --- Dados iniciais do sistema ---
placa_modelo = "UCPIP V1.2"
sintomas = {
    "Placa não liga": [
        ("U12", "Regulador principal 3.3V", "Verificar tensão de saída: 3.3V"),
        ("U1", "Regulador auxiliar", "Verificar curto entre entrada e GND"),
        ("U27", "Regulador auxiliar", "Verificar tensão de saída"),
        ("C4", "Capacitor eletrolítico de entrada", "Verificar se está estufado ou em curto"),
        ("C5", "Capacitor eletrolítico de entrada", "Verificar continuidade com GND"),
        ("D2", "Diodo de proteção de entrada", "Verificar se está em curto")
    ],
    "Superaquecimento ou alto consumo": [
        ("U21", "Microprocessador principal", "Verificar consumo de corrente (>150mA pode indicar curto)"),
        ("U12", "Regulador de tensão", "Verificar dissipação excessiva"),
        ("C6", "Filtro de ruído", "Verificar resistência entre os terminais"),
        ("C7", "Filtro de ruído", "Verificar continuidade com GND"),
        ("U28", "Memória Flash SPI", "Verificar se esquenta em excesso")
    ],
    "Sem comunicação RS-485": [
        ("U11", "CI RS-485 SN65HVD3082EDR", "Verificar alimentação e sinal em A/B"),
        ("R39", "Resistor de linha", "Verificar valor de resistência"),
        ("R40", "Resistor de linha", "Verificar continuidade"),
        ("CNx", "Conector de comunicação", "Inspecionar pinos e solda fria")
    ],
    "LED não acende / Sem sinal visual": [
        ("LED1~LEDn", "LEDs de sinalização", "Verificar com multímetro no modo diodo"),
        ("R38", "Resistor limitador de corrente", "Verificar valor nominal"),
        ("R115", "Resistor limitador", "Verificar continuidade"),
        ("U10", "Flip-Flop de controle de LEDs", "Verificar alimentação e saída lógica")
    ],
    "Relé não aciona / Sem saída": [
        ("RL1~RL8", "Relés de saída", "Verificar tensão na bobina"),
        ("Q24", "Transistor de acionamento", "Testar com base polarizada"),
        ("U15", "Buffer lógico de controle", "Verificar nível de saída"),
        ("U16", "Flip-Flop de controle", "Testar nível lógico de acionamento"),
        ("D2", "Diodo de proteção do relé", "Verificar curto reverso")
    ]
}

# --- Interface Web com Streamlit ---
st.set_page_config(page_title="Diagnóstico de Placas", layout="centered")
st.title("🔍 Diagnóstico de Placa Eletrônica")
st.subheader(f"Modelo da placa: {placa_modelo}")

st.markdown("---")
st.markdown("**Informe o número de série da placa:**")
num_serie = st.text_input("Número de Série")

st.markdown("**Selecione o(s) sintoma(s) apresentado(s):**")
sintomas_selecionados = st.multiselect("", options=list(sintomas.keys()))

if sintomas_selecionados:
    st.markdown("---")
    st.markdown("### 🧩 Componentes a verificar:")

    for sintoma in sintomas_selecionados:
        st.markdown(f"#### 🔧 {sintoma}")
        tabela = pd.DataFrame(sintomas[sintoma], columns=["Componente", "Função", "Teste recomendado"])
        st.dataframe(tabela, use_container_width=True)

    st.markdown("---")
    observacoes = st.text_area("📝 Observações do operador:", placeholder="Descreva testes realizados, medições ou anomalias...")

    if st.button("Salvar diagnóstico"):
        data = {
            "Data": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Número de Série": num_serie,
            "Sintomas": ", ".join(sintomas_selecionados),
            "Observações": observacoes
        }
        historico = pd.DataFrame([data])
        historico.to_csv("historico_diagnostico.csv", mode="a", header=not pd.io.common.file_exists("historico_diagnostico.csv"), index=False)
        st.success("Diagnóstico salvo com sucesso!")
else:
    st.info("Selecione pelo menos um sintoma para iniciar o diagnóstico.")
