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
            if not API_KEY or "COLE_SUA" in API_KEY:
                st.error("⚠️ Configure a API Key no código.")
            else:
                with st.spinner("Analisando componentes e buscando preços..."):
                    texto_bruto = aiAnalysis.consultar_gemini(
                        API_KEY, processorName, gpuName, ramAmount, 
                        motherboardName, diskInfoList, uso_principal, uso_detalhe
                    )
                    
                    # --- LIMPEZA DE SEGURANÇA ---
                    # Remove formatações acidentais que a IA possa colocar nas tags
                    texto_bruto = texto_bruto.replace("**[RESUMO]**", "[RESUMO]").replace("**[TABELA]**", "[TABELA]")
                    
                    # --- A MÁGICA DO CORTE ---
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
                        # st.write("DEBUG IA:", texto_bruto) # Descomente esta linha se quiser ver onde a IA errou

                    # Salva no estado
                    st.session_state.texto_analise = analise_completa
                    st.session_state.texto_resumo = resumo_rapido
                    st.session_state.texto_tabela = tabela_precos
                    st.session_state.analise_pronta = True
                    st.rerun()

    # [PARTE 2] RESULTADO (Se já tem análise)
    else:
        st.success("Diagnóstico Concluído!")
        
        # 1. MOSTRA A ANÁLISE COMPLETA PRIMEIRO
        st.markdown(st.session_state.texto_analise)
        
        st.divider()

        # 2. MOSTRA A TABELA DE PREÇOS EM DESTAQUE
        st.subheader("💰 Tabela de Hardware e Preços Médios")
        st.caption("Valores estimados pela IA baseados em cotações recentes.")
        st.markdown(st.session_state.texto_tabela)

        st.divider()

        # 3. MOSTRA O BOTÃO DO RESUMO
        with st.expander("📝 EXIBIR RESUMO RÁPIDO (O que importa)", expanded=False):
            st.info("Resumo direto ao ponto:")
            st.markdown(st.session_state.texto_resumo)

        st.divider()
        
        # 4. BOTÃO PARA VOLTAR
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
