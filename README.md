# HardwareAnalysis

Aplicativo desktop para identificar componentes do computador e receber recomendações de upgrade contextualizadas com Gemini. O objetivo é ajudar a decidir **o que atualizar, por que atualizar e o que confirmar antes da compra**.

## O que oferece

- Interface desktop nativa em Python com PySide6.
- Temas claro e escuro, com a escolha salva entre execuções.
- Identificação de CPU, GPU, placa-mãe, memória, discos e sistema operacional, conforme os dados disponíveis.
- Métricas de CPU e memória em tempo real, com histórico gráfico local.
- Leitura opcional de carga e temperatura em GPUs NVIDIA quando NVML e o driver estão disponíveis.
- Consultor com filtros para jogos leves/AAA, trabalho ou uso doméstico, orçamento e preferência de compra.
- Recomendações com prioridade, justificativa, compatibilidade e verificações antes da compra.

## Instalação e execução

Recomendado: Python 3.12 em ambiente virtual.

```bash
python -m venv .venv
```

Ative o ambiente virtual e inicie o app diretamente. Na primeira execução, ele verifica e instala as dependências necessárias com o próprio Python que está rodando o programa — incluindo WMI no Windows e NVML para sensores NVIDIA. É preciso ter conexão com a internet nessa primeira inicialização.

```bash
python main.py
```

Também é possível iniciar pelo atalho legado `python app.py`.

## Compatibilidade e limites

O app busca funcionar em Windows, Linux e macOS. A disponibilidade de identificação de GPU, placa-mãe e sensores depende do sistema, permissões, drivers e ferramentas instaladas. CPU, memória e discos funcionam via Psutil. A leitura atual de carga/temperatura da GPU usa NVML, compatível com NVIDIA; provedores de sensores para AMD/Intel e temperatura de CPU não estão integrados.

A IA não substitui verificações de compatibilidade: placa-mãe OEM, BIOS, fonte, gabinete, soquete e tipo de memória podem exigir confirmação manual. Os campos adicionais do consultor são opcionais e são ignorados quando vazios. Se o orçamento não comportar um upgrade que valha a pena, o consultor deve explicar isso sem recomendar que o usuário ultrapasse o limite.

O Gemini não consulta preços em tempo real. Links de pesquisa são atalhos para buscar produtos, não cotações. Ao solicitar uma análise, os dados detectados do PC e as preferências são enviados ao Gemini.

## Chave Gemini

Crie uma chave no [Google AI Studio](https://aistudio.google.com/app/apikey) e informe-a na barra lateral do app. A chave permanece somente na sessão atual e não é gravada em arquivo. Opcionalmente, configure `GEMINI_API_KEY` no ambiente antes de iniciar.

## Estrutura

- `main.py`: valida/instala dependências e contém a interface PySide6, formulários, monitoramento e recomendações.
- `app.py`: atalho opcional para iniciar `main.py`.
- `hardwareInfo.py`: descoberta de hardware com caminhos específicos por sistema e fallbacks.
- `hardwareMonitoring.py`: métricas de CPU, memória e provedor opcional NVIDIA NVML.
- `aiAnalysis.py`: prompt do consultor, validação de JSON e links de pesquisa.

## Privacidade

A coleta de hardware é local. Ao pedir uma análise, os dados detectados, o perfil e as preferências são enviados ao Gemini usando a chave informada. A chave digitada no app não é gravada pelo aplicativo.
