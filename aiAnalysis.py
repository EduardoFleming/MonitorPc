import google.generativeai as genai

def consultar_gemini(api_key, cpu, gpu, ram, board, disks, uso_principal, uso_detalhe):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')

    prompt = f"""
    Atue como um especialista sênior em hardware de PC.
    
    DADOS DO CLIENTE:
    - Objetivo: {uso_principal} -> Foco: {uso_detalhe}
    - Hardware: CPU {cpu} | GPU {gpu} | RAM {ram} | MB {board} | Disco {disks}

    REGRAS RÍGIDAS DE COMPORTAMENTO:
    1. ZERO CONVERSA: Não comece com "Olá", "Análise pronta", "Com base no seu hardware". Vá direto ao título.
    2. FORMATO: Siga estritamente a estrutura Markdown abaixo.
    3. DEFINIÇÃO DE GARGALO (IMPORTANTE):
       - Se uma peça for muito forte para o uso (ex: GPU potente para escritório), ISSO É BOM (chame de "Sobra de desempenho" ou "Margem futura").
       - NÃO chame peça sobrando de "Gargalo" ou "Subutilizada" em tom negativo.
       - Gargalo é APENAS quando uma peça fraca impede o funcionamento total de outra (ex: CPU em 100% travando a GPU).

    ESTRUTURA DE SAÍDA (Copie este modelo):

    # 📋 Relatório: {uso_detalhe}

    ### 1. Veredito Final
    (Diga se atende, se sobra ou se falta desempenho. Seja direto.)

    ### 2. Análise Técnica
    (Explique como esse conjunto específico roda o software de {uso_detalhe}.)

    ### 3. Pontos de Atenção
    (Cite gargalos reais ou limitações. Se sobrar tudo, diga "Sem gargalos, máquina com ótima margem".)

    ### 4. Sugestão de Melhoria
    (Só sugira se for necessário para o uso atual.)

    |||RESUMO|||
    
    ✅ Veredito: (1 frase curta)
    ⚠️ Gargalo: (Diga "Nenhum" se for apenas sobra de potência)
    🛒 Recomendação: (1 frase curta se houver, caso não, escreva "manter atual")
    ⏳ Tempo de vida: (Quanto tempo o usuário pode ter sem se preocupar em ter que dar um upgrade)
    """

    try:
        response = model.generate_content(prompt)
        return response.text.strip() # Remove espaços extras no começo
    except Exception as e:
        return f"Erro na IA: {e}"