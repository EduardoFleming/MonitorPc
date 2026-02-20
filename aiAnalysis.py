import google.generativeai as genai

def consultar_gemini(api_key, cpu, gpu, ram, board, disks, uso_principal, uso_detalhe):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-3-flash-preview')

    prompt = f"""
    Atue como um especialista de alto nível em hardware de PC.
    
    DADOS DO CLIENTE:
    - Objetivo: {uso_principal} -> Foco: {uso_detalhe}
    - Hardware: CPU {cpu} | GPU {gpu} | RAM {ram} | MB {board} | Disco {disks}

    REGRAS RÍGIDAS (MUITO IMPORTANTE):
    1. Vá direto ao título, sem introduções.
    2. Você DEVE usar EXATAMENTE as tags "[RESUMO]" e "[TABELA]" para dividir o texto, sem colocar asteriscos ou formatações nelas.
    3. Na tabela, liste os preços médios de mercado atuais em Reais (R$).
    4. Gargalo é só se realmente alguma peça atrpalhar o desempenho de outra

    COPIE EXATAMENTE ESTE FORMATO PARA A SUA RESPOSTA:

    # 📋 Relatório: {uso_detalhe}

    ### 1. Veredito Final
    (Texto)

    ### 2. Análise Técnica
    (Tópicos)

    ### 3. Pontos de Atenção
    (Texto)

    [RESUMO]
    ✅ Veredito: (1 frase curta)
    ⚠️ Gargalo: (Diga "Nenhum" se não houver)
    🛒 Recomendação: (1 frase curta)

    [TABELA]
    | Tipo de Peça | Modelo (Atual ou Upgrade) | Pesquisar |
    | :--- | :--- | :--- |
    | Processador | ... | [Ver Preço](https://www.google.com/search?tbm=shop&q=...) |
    | Placa de Vídeo | ... | [Ver Preço](https://www.google.com/search?tbm=shop&q=...) |
    | Memória RAM | ... | [Ver Preço](https://www.google.com/search?tbm=shop&q=...) |
    | Placa-Mãe | ... | [Ver Preço](https://www.google.com/search?tbm=shop&q=...) |
    """

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Erro na IA: {e}"
