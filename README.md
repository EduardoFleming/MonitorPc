# 🖥️ Monitor Pc

> **Monitoramento de Hardware Inteligente com Análise via IA**

O **Monitor Pc** é uma aplicação desktop que vai além de apenas mostrar números. Ele combina o monitoramento em tempo real do seu hardware (CPU, GPU, RAM) com uma **Inteligência Artificial (LLM)** que analisa se o seu computador é adequado para o seu uso específico (Jogos, Trabalho ou Lazer).

---

## 🚀 Funcionalidades

- **📊 Monitoramento em Tempo Real:** Acompanhe o uso de CPU, Memória RAM e GPU (NVIDIA) e temperaturas.
- **📋 Identificação de Hardware:** Lista automaticamente seu processador, placa de vídeo, placa-mãe e discos.
- **🧠 Técnico Virtual (IA):**
  - Você diz para que vai usar o PC (ex: "Jogos Competitivos" ou "Edição de Vídeo").
  - A IA analisa suas peças e diz se o PC aguenta.
  - Aponta gargalos reais e sugere upgrades se necessário.
- **☁️ Instalação Automática:** O sistema verifica e instala as dependências necessárias na primeira execução.

---

## ⚠️ Limitações e Requisitos (Leia Antes)

Este projeto está em **desenvolvimento (Work in Progress)**. Algumas funcionalidades possuem restrições importantes:

1.  **Sistema Operacional:** Atualmente funciona **apenas no Windows**.
2.  **Placa de Vídeo:** O monitoramento detalhado (uso % e temperatura) só funciona em placas **NVIDIA**. Outras placas serão identificadas, mas sem dados em tempo real.
3.  **Versão do Python:**
    - ✅ Recomendado: **Python 3.12**
    - ❌ **Não funciona no Python 3.14** (devido a incompatibilidades com bibliotecas gráficas).

---

## 🛠️ Como Usar

### 1. Pré-requisitos

- Ter o [Python 3.12](https://www.python.org/downloads/) instalado.
- Uma **API Key do Google Gemini** (Grátis). Gere a sua [aqui no Google AI Studio](https://aistudio.google.com/app/apikey).
- **Configuração Obrigatória da Chave:**
  1. Após gerar sua chave, abra o arquivo `main.py` em um editor de texto (Bloco de Notas, VS Code, etc).
  2. Localize a variável `API_KEY` logo no início do arquivo.
  3. Cole sua chave dentro das aspas. Deve ficar assim:
     ```python
     API_KEY = "AIzaSyD_Sua_Chave_Aqui_..."
     ```

### 2. Instalação e Execução

Não é necessário instalar bibliotecas manualmente. O script `app.py` cuida de tudo.

1. Baixe o repositório ou coloque todos os arquivos `.py` em uma pasta.
2. Abra o terminal (CMD ou PowerShell) dentro dessa pasta. (Pode ser feito pelo VSCode)
3. Execute o comando:

```bash
py app.py
