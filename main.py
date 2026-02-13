import streamlit as st
import time

import hardwareInfo
import hardwareMonitoring
import aiAnalysis

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Monitor de Hardware", layout="wide")

# --- CONFIGURAÇÃO DA IA ---
API_KEY = "AIzaSyAD-s802jeV6kHr8fDJ-X-iiHsDIb88Bnk" 

# --- INICIALIZAÇÃO DO ESTADO (SESSION STATE) ---
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
tab1, tab2, tab3 = st.tabs(["📊 Specs", "📈 Monitoramento", "🧠 Consultor IA"])

# ==========================================
# ABA 1: SPECS
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

    # [PARTE 1] FORMULÁRIO (Se ainda não tem análise)
    if not st.session_state.analise_pronta:
        st.info("Responda para gerar o diagnóstico:")
        
        col_p1, col_p2 = st.columns(2)
        
        with col_p1:
            uso_principal = st.radio(
                "Objetivo:",
                ["🎮 Jogos", "💼 Trabalho", "🍿 Uso Doméstico"],
                horizontal=False
            )

        with col_p2:
            # Lógica para definir as opções do segundo menu
            opcoes_detalhe = []
            if uso_principal == "🎮 Jogos":
                opcoes_detalhe = ["Competitivo Leve (CS2, LoL)", "AAA Pesado (Cyberpunk, GTA)", "Indie/Retro"]
            elif uso_principal == "💼 Trabalho":
                opcoes_detalhe = ["Edição Vídeo/3D", "Programação", "Escritório Geral"]
            else:
                opcoes_detalhe = ["Filmes 4K/YouTube", "Estudos/Navegação", "Servidor de Arquivos"]
                
            uso_detalhe = st.selectbox("Detalhe:", opcoes_detalhe)

        if st.button("🔍 Analisar Agora", type="primary", use_container_width=True):
            if not API_KEY or "COLE_SUA" in API_KEY:
                st.error("⚠️ Configure a API Key no código.")
            else:
                with st.spinner("Analisando componentes..."):
                    texto_bruto = aiAnalysis.consultar_gemini(
                        API_KEY, processorName, gpuName, ramAmount, 
                        motherboardName, diskInfoList, uso_principal, uso_detalhe
                    )
                    
                    # Separa o texto onde a IA escreveu "|||RESUMO|||"
                    if "|||RESUMO|||" in texto_bruto:
                        partes = texto_bruto.split("|||RESUMO|||")
                        analise_completa = partes[0]
                        resumo_rapido = partes[1]
                    else:
                        analise_completa = texto_bruto
                        resumo_rapido = "Resumo não disponível."

                    # Salva no estado
                    st.session_state.texto_analise = analise_completa
                    st.session_state.texto_resumo = resumo_rapido
                    st.session_state.analise_pronta = True
                    st.rerun()

    # [PARTE 2] RESULTADO (Se já tem análise)
    else:
        st.success("Diagnóstico Concluído!")
        
        st.markdown(st.session_state.texto_analise)
        
        st.divider()

        # st.expander cria um botão que expande/recolhe conteúdo
        with st.expander("📝 EXIBIR RESUMO RÁPIDO (O que importa)", expanded=False):
            st.info("Resumo direto ao ponto:")
            st.markdown(st.session_state.texto_resumo)

        st.divider()
        
        # Botão para voltar
        if st.button("🔄 Nova Consulta"):
            st.session_state.analise_pronta = False
            st.rerun()

# ==========================================
# ABA 2: MONITORAMENTO (Loop Infinito)
# ==========================================
with tab2:
    st.header("Tempo Real")
    col1, col2, col3 = st.columns(3)
    
    # Criamos os elementos vazios
    metric_cpu = col1.empty()
    metric_ram = col2.empty()
    metric_gpu = col3.empty()

    # Loop principal
    while True:
        # Pega os dados
        cpu = hardwareMonitoring.getCpuUsage()
        ram = hardwareMonitoring.getRamUsage()
        gpu = hardwareMonitoring.getGpuUsage()

        # Atualiza apenas os números
        metric_cpu.metric("CPU Usage", f"{cpu}%")
        metric_ram.metric("RAM Usage", f"{ram}%")
        metric_gpu.metric("GPU Usage", gpu["usage"], delta=gpu["temp"])
        
        # Pausa
        time.sleep(2)