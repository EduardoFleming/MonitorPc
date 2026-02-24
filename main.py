import streamlit as st
import time

import hardwareInfo
import hardwareMonitoring
import aiAnalysis

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Monitor de Hardware", layout="wide")

# --- MENU LATERAL (SIDEBAR) PARA A CHAVE DA API ---
with st.sidebar:
    st.header("⚙️ Configurações da IA")
    st.write("Para usar o Diagnóstico IA, insira sua chave do Google Gemini abaixo.")
    API_KEY = st.text_input("🔑 API Key do Gemini", type="password")
    st.markdown("[Obter chave gratuita](https://aistudio.google.com/app/apikey)")
    st.divider()
    st.caption("Monitor PC v1.0")

# --- SESSION STATE ---
if "analise_pronta" not in st.session_state:
    st.session_state.analise_pronta = False
if "texto_resultado" not in st.session_state:
    st.session_state.texto_resultado = ""

# --- TÍTULO ---
st.title("🖥️ Monitor & AI Tech")

# --- COLETA DE DADOS ESTÁTICOS ---
processorName = hardwareInfo.getCpuInfo()
gpuName = hardwareInfo.getGpuInfo()
motherboardName = hardwareInfo.getMotherboardInfo()
ramAmount = hardwareInfo.getRamInfo()
diskInfoList = hardwareInfo.getDiskInfo()

# --- CRIAÇÃO DAS ABAS ---
tab1, tab2, tab3 = st.tabs(["⚙️ Peças", "📈 Monitoramento", "🧠 Consultor IA"])

# ==========================================
# ABA 1: PEÇAS
# ==========================================
with tab1:
    col_a, col_b = st.columns(2)
    with col_a:
        st.caption("Processador")
        st.code(processorName)
        st.caption("Memória RAM")
        st.code(ramAmount)
    with col_b:
        st.caption("Placa de Vídeo")
        st.code(gpuName)
        st.caption("Placa-Mãe")
        st.code(motherboardName)
    
    st.divider()
    st.caption("Armazenamento")
    if not diskInfoList:
        st.warning("Nenhum disco detectado.")
    else:
        for disk in diskInfoList:
            st.code(disk, language=None)

# ==========================================
# ABA 3: IA INTERATIVA
# ==========================================
with tab3:
    st.header("Diagnóstico Personalizado")

    if not st.session_state.get('analise_pronta', False):
        st.info("Responda para gerar o diagnóstico:")
        
        col_p1, col_p2 = st.columns(2)
        
        with col_p1:
            uso_principal = st.radio(
                "Objetivo:",
                ["🎮 Jogos", "💼 Trabalho", "🍿 Uso Doméstico"],
                horizontal=False
            )

        with col_p2:
            opcoes_detalhe = []
            if uso_principal == "🎮 Jogos":
                opcoes_detalhe = ["Competitivo Leve (CS2, LoL)", "AAA Pesado (Cyberpunk, GTA)", "Indie/Retro"]
            elif uso_principal == "💼 Trabalho":
                opcoes_detalhe = ["Edição Vídeo/3D", "Programação", "Escritório Geral"]
            else:
                opcoes_detalhe = ["Filmes 4K/YouTube", "Estudos/Navegação", "Servidor de Arquivos"]
                
            uso_detalhe = st.selectbox("Detalhe:", opcoes_detalhe)

        if st.button("🔍 Analisar Agora", type="primary", use_container_width=True):
            if not API_KEY:
                st.error("⚠️ Insira sua API Key do Gemini no menu lateral esquerdo para usar a IA.")
            else:
                with st.spinner("Analisando componentes e buscando preços..."):
                    texto_bruto = aiAnalysis.consultar_gemini(
                        API_KEY, processorName, gpuName, ramAmount, 
                        motherboardName, diskInfoList, uso_principal, uso_detalhe
                    )
                    
                    texto_bruto = texto_bruto.replace("**[RESUMO]**", "[RESUMO]").replace("**[TABELA]**", "[TABELA]")
                    
                    if "[RESUMO]" in texto_bruto and "[TABELA]" in texto_bruto:
                        partes = texto_bruto.split("[RESUMO]")
                        analise_completa = partes[0].strip()
                        
                        resto = partes[1].split("[TABELA]")
                        resumo_rapido = resto[0].strip()
                        tabela_precos = resto[1].strip()
                    else:
                        analise_completa = texto_bruto
                        resumo_rapido = "Resumo indisponível. A IA mudou o formato da resposta."
                        tabela_precos = "Tabela indisponível."

                    st.session_state.texto_analise = analise_completa
                    st.session_state.texto_resumo = resumo_rapido
                    st.session_state.texto_tabela = tabela_precos
                    st.session_state.analise_pronta = True
                    st.rerun()

    else:
        st.success("Diagnóstico Concluído!")
        
        st.markdown(st.session_state.texto_analise)
        st.divider()

        st.subheader("💰 Tabela de Hardware")
        st.markdown(st.session_state.texto_tabela)
        st.divider()

        with st.expander("📝 EXIBIR RESUMO RÁPIDO", expanded=False):
            st.info("Resumo direto ao ponto:")
            st.markdown(st.session_state.texto_resumo)

        st.divider()
        
        if st.button("🔄 Nova Consulta"):
            st.session_state.analise_pronta = False
            st.rerun()

# ==========================================
# ABA 2: MONITORAMENTO
# ==========================================
with tab2:
    st.header("Tempo Real")
    col1, col2, col3 = st.columns(3)
    
    metric_cpu = col1.empty()
    metric_ram = col2.empty()
    metric_gpu = col3.empty()

    while True:
        cpu = hardwareMonitoring.getCpuUsage()
        ram = hardwareMonitoring.getRamUsage()
        gpu = hardwareMonitoring.getGpuUsage()

        metric_cpu.metric("CPU Usage", f"{cpu}%")
        metric_ram.metric("RAM Usage", f"{ram}%")
        metric_gpu.metric("GPU Usage", gpu["usage"], delta=gpu["temp"])
        
        time.sleep(2)
