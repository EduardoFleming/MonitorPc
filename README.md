# 🖥️ Monitor PC & AI Tech

> **Monitoramento de Hardware Inteligente com Diagnóstico via Inteligência Artificial**

O **Monitor PC** é uma ferramenta de diagnóstico que une a coleta de dados de hardware em tempo real com a inteligência do Google Gemini. Ele não apenas exibe suas especificações, mas atua como um consultor técnico que analisa o equilíbrio do seu setup para o seu perfil de uso.

---

## 🚀 Funcionalidades

- **📈 Monitoramento em Tempo Real:** Acompanhamento dinâmico de uso de CPU, RAM e GPU (NVIDIA), incluindo temperaturas.
- **📊 Specs Detalhadas:** Identificação precisa de Processador, Placa-Mãe (incluindo modelos OEM como HP/Dell), GPU e Armazenamento.
- **🧠 Consultor IA (Gemini):**
  - Análise personalizada baseada no seu objetivo (Jogos, Trabalho ou Uso Doméstico).
  - Identificação de gargalos técnicos reais.
  - Tabela de recomendações com links diretos para pesquisa de preços no Google Shopping.
- **🖼️ Interface Nativa:** Roda como um aplicativo de desktop em uma janela dedicada para melhor experiência do usuário.

---

## 🛠️ Requisitos e Compatibilidade

Para garantir o funcionamento perfeito, verifique os requisitos:

1. **Sistema Operacional:** Windows 10 ou 11 (devido ao uso de bibliotecas `wmi` e `pywin32`).
2. **Hardware NVIDIA:** O monitoramento de temperatura e carga de GPU é exclusivo para placas NVIDIA (via `pynvml`).
3. **Versão do Python:** - ✅ Recomendado: **Python 3.12**
   - ⚠️ **Atenção:** Pode haver incompatibilidades com versões muito recentes como o Python 3.14 devido a bibliotecas gráficas.

---

## ⚙️ Como Usar (Passo a Passo)

### 1. Obtenha sua API Key do Gemini
O projeto utiliza a inteligência do Google para realizar as análises.
1. Acesse o [Google AI Studio](https://aistudio.google.com/app/apikey).
2. Clique no botão **"Create API key"**.
3. Copie a chave gerada (um código longo que começa com `AIza...`).

### 2. Execução do Aplicativo
Você não precisa instalar bibliotecas manualmente; o inicializador faz o trabalho duro.
1. Baixe os arquivos do repositório para uma pasta no seu computador.
2. Abra o **Terminal** (ou PowerShell) dentro dessa pasta. No VS Code, você pode usar o atalho `Ctrl + '`.
3. Digite o comando abaixo e **pressione a tecla Enter**:
   `python app.py`
4. Aguarde alguns segundos. O sistema verificará as dependências e abrirá a janela do aplicativo automaticamente.

### 3. Configuração da Chave e Análise
Com a janela do **Monitor PC** aberta:
1. No canto esquerdo, localize o menu cinza (a **Barra Lateral**).
2. Clique no campo **"🔑 API Key do Gemini"**.
3. Cole a sua chave (Ctrl + V) e **pressione a tecla Enter** no teclado para confirmar.
4. Agora, navegue até a aba **"🧠 Consultor IA"**, selecione seu perfil e clique no botão azul **"🔍 Analisar Agora"**.

---

## 👨‍💻 Tecnologias Utilizadas

- **Interface:** Streamlit & PyWebview.
- **IA:** Google Generative AI (Gemini Flash 3.0).
- **Monitoramento:** Psutil, WMI e PyNVML.

---

## 📝 Notas de Versão
- **v1.0:** Lançamento inicial com interface em abas, monitoramento estável e integração com Gemini.
- **Correção de Portas:** Implementada alocação dinâmica de portas para evitar conflitos ao abrir o app.