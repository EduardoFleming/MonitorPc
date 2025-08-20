import streamlit as st
import time

import hardwareInfo
import hardwareMonitoring

# --- CONFIGURAÇÃO DA PÁGINA ---
# Isso deve ser o primeiro comando do Streamlit no seu script
st.set_page_config(
    page_title="Monitor de Hardware",
    page_icon="🖥️",
    layout="wide"
)

# --- TÍTULO PRINCIPAL DA APLICAÇÃO ---
st.title("🖥️ Software de Monitoramento de Hardware")

# --- BUSCA OS DADOS ESTÁTICOS (só precisa fazer uma vez) ---
processorName = hardwareInfo.getCpuInfo()
gpuName = hardwareInfo.getGpuInfo()
motherboardName = hardwareInfo.getMotherboardInfo()
ramAmount = hardwareInfo.getRamInfo()
diskInfoList = hardwareInfo.getDiskInfo()

# --- CRIAÇÃO DAS ABAS ---
tab1, tab2 = st.tabs(["📊 Informações do PC", "📈 Monitoramento em Tempo Real"])

# --- CONTEÚDO DA ABA 1: Informações Estáticas ---
with tab1:
    st.header("Especificações de Hardware")

    # Para cada informação, usamos um subheader e o st.code()
    # que já vem com um botão de "copiar" embutido!
    st.subheader("Processador")
    st.code(processorName, language=None)

    st.subheader("Placa de Vídeo (GPU)")
    st.code(gpuName, language=None)

    st.subheader("Placa-Mãe")
    st.code(motherboardName, language=None)

    st.subheader("Memória RAM Total")
    st.code(ramAmount, language=None)

    st.subheader("Partições de Disco")
    for disk in diskInfoList:
        st.code(disk, language=None)

# --- CONTEÚDO DA ABA 2: Monitoramento em Tempo Real ---
with tab2:
    st.header("Uso de Recursos Atuais")

    # Criamos um "espaço reservado" na tela que vamos atualizar
    placeholder = st.empty()

    # Loop infinito para manter os dados atualizados
    while True:
        # Pega os dados mais recentes do hardware
        cpu_usage = hardwareMonitoring.getCpuUsage()
        ram_usage = hardwareMonitoring.getRamUsage()
        gpu_stats = hardwareMonitoring.getGpuUsage()

        # Usa o placeholder para redesenhar a seção de monitoramento
        with placeholder.container():
            # Cria 3 colunas para organizar os dados
            col1, col2, col3 = st.columns(3)

            # Coluna da CPU
            with col1:
                st.metric(label="Uso da CPU", value=f"{cpu_usage}%")
            
            # Coluna da RAM
            with col2:
                st.metric(label="Uso de RAM", value=f"{ram_usage}%")

            # Coluna da GPU
            with col3:
                st.metric(label="Uso da GPU", value=gpu_stats["usage"])
                st.metric(label="Temp. da GPU", value=gpu_stats["temp"])
            
            # Espera 2 segundos antes de atualizar novamente
            time.sleep(2)