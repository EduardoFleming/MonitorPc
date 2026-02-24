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
- **🖼️ Interface Nativa:** Roda como um aplicativo de desktop (janela dedicada) sem precisar abrir o navegador manualmente.

---

## 🛠️ Requisitos e Compatibilidade

Para garantir o funcionamento perfeito, verifique os requisitos:

1. **Sistema Operacional:** Windows 10 ou 11 (devido ao uso de bibliotecas `wmi` e `pywin32`).
2. **Hardware NVIDIA:** O monitoramento de temperatura e carga de GPU é exclusivo para placas NVIDIA (via `pynvml`).
3. **Versão do Python:** - ✅ Recomendado: **Python 3.12**
   - ⚠️ **Atenção:** Pode haver incompatibilidades com versões muito recentes como o Python 3.14.

---

## ⚙️ Como Usar

### 1. Obtenha sua API Key
O projeto utiliza o modelo Gemini da Google para as análises.
- Gere sua chave gratuita em: [Google AI Studio](https://aistudio.google.com/app/apikey).

### 2. Execução
Não é necessário instalar bibliotecas manualmente; o script de inicialização faz isso por você.

1. Baixe os arquivos do repositório.
2. Abra o terminal na pasta do projeto (ou use o terminal do VS Code).
3. Execute o inicializador:
   ```bash
   python app.py