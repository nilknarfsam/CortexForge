# Início rápido — CortexForge

Guia em poucos passos para começar a usar o assistente local.

## Pré-requisitos

- Python 3.10+ e dependências instaladas ([INSTALLATION.md](INSTALLATION.md))
- Ollama em execução
- Modelo `qwen2.5-coder:7b` (ou outro já baixado)

```powershell
ollama pull qwen2.5-coder:7b
```

## 1. Iniciar a aplicação

```powershell
cd CortexForge
.\.venv\Scripts\Activate.ps1   # Windows
python app.py
```

## 2. Verificar o Ollama

Ao abrir, o chat exibe mensagens `[Sistema]`:

- `Ollama está disponível.`
- Lista de modelos carregados

Se aparecer erro de conexão, consulte [TROUBLESHOOTING.md](TROUBLESHOOTING.md).

## 3. Selecionar modelo

Na barra superior:

1. Campo **Modelo:** — escolha `qwen2.5-coder:7b` (recomendado).
2. Se a lista estiver vazia, clique em **Atualizar**.

## 4. Selecionar agente

Campo **Agente:**

| Agente | Quando usar |
|--------|-------------|
| **Architect** | Estrutura, módulos, decisões de design |
| **Coder** | Implementação, exemplos de código (padrão) |
| **Reviewer** | Revisão e melhorias de qualidade |

## 5. Abrir um projeto (opcional)

No painel esquerdo **Projetos**:

1. Clique em **Abrir Pasta**.
2. Selecione a pasta do seu código.
3. O painel mostra:
   - Nome e caminho
   - Estatísticas (pastas, arquivos, `.py`, etc.)
   - **Resumo do Projeto** (usado automaticamente no chat)

Sem pasta aberta, o chat funciona apenas com o prompt do agente.

## 6. Enviar uma mensagem

1. Digite no campo inferior do chat.
2. Pressione **Enter**.
3. A barra de status mostra **Gerando resposta...**
4. A resposta aparece em streaming sob `[CortexForge]` (texto vai sendo escrito em tempo real).

Exemplo:

```text
[Você]
Como organizar um projeto Python em pacotes?

[CortexForge]
...
```

## 7. Barra de status

| Mensagem | Significado |
|----------|-------------|
| **Pronto** | Pode enviar nova mensagem |
| **Gerando resposta...** | Aguarde o Ollama |
| **Erro** | Falha na última operação (veja o chat) |

## Fluxo resumido

```
Iniciar app → Escolher modelo → Escolher agente → (Abrir pasta) → Digitar → Enter
```

## Documentação relacionada

- [INSTALLATION.md](INSTALLATION.md) — instalação detalhada
- [AGENTS.md](AGENTS.md) — perfis de agentes
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) — erros comuns
