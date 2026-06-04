# Guia do desenvolvedor — CortexForge

Informações para quem for manter, estender ou compartilhar o código do projeto.

Repositório: [github.com/nilknarfsam/CortexForge](https://github.com/nilknarfsam/CortexForge)

## Estrutura interna do CortexForge

```
CortexForge/
├── app.py                      # Entrada: QApplication + MainWindow
├── requirements.txt            # PySide6, requests
├── agents/                     # Prompts de sistema (texto)
│   ├── architect.txt
│   ├── coder.txt
│   └── reviewer.txt
├── core/                       # Lógica sem UI
│   ├── config.py               # Agentes, load_agent_prompt
│   ├── ollama_client.py        # HTTP Ollama (tags, generate)
│   ├── project_context.py      # name, path da pasta aberta
│   ├── project_scanner.py      # Estatísticas de arquivos/pastas
│   └── project_summary.py      # Resumo + build_prompt_with_context
├── ui/
│   ├── main_window.py          # Layout e orquestração
│   └── ollama_worker.py        # QThread para generate()
├── projects/                   # Reservado (uso futuro)
└── docs/                       # Documentação
```

## Responsabilidades por camada

| Camada | Responsabilidade |
|--------|------------------|
| `app.py` | Bootstrap Qt |
| `ui/` | Widgets, eventos, thread de geração |
| `core/` | Ollama, config, projeto, scanner, resumo |
| `agents/` | Texto de system prompt por perfil |

A UI **não** deve conter chamadas HTTP diretas; use `OllamaClient`.

## Fluxo de uma mensagem no chat

1. Usuário pressiona Enter → `MainWindow._send_message()`.
2. Carrega prompt do agente: `load_agent_prompt(agent_id)`.
3. Se houver projeto: `build_prompt_with_context(agent, _project_summary, mensagem)`.
4. `OllamaGenerateWorker` chama `OllamaClient.generate()` em background.
5. Sinal `finished` → atualiza chat e barra de status.

Ver diagrama em [ARCHITECTURE.md](ARCHITECTURE.md).

## Configuração de agentes

- Constante `DEFAULT_AGENT` em `core/config.py` (padrão: `coder`).
- Novo agente: adicionar `.txt` em `agents/`, entradas em `AGENT_FILES` e `AGENT_LABELS`.

Detalhes: [AGENTS.md](AGENTS.md).

## Cliente Ollama

`core/ollama_client.py`:

| Método | Uso |
|--------|-----|
| `is_available()` | GET `/api/tags` |
| `list_models()` | Parse de modelos |
| `generate(prompt)` | POST `/api/generate` |
| `debug_generate_payload(prompt)` | JSON exato do POST (debug) |

URL padrão: `http://localhost:11434`.

Em `HTTPError`, logs no terminal: `STATUS`, `BODY`, modelo, tamanho e preview do prompt.

## Projeto e contexto

| Classe | Função |
|--------|--------|
| `ProjectContext` | Armazena `name` e `path` |
| `ProjectScanner` | Varre árvore; retorna `ProjectScanResult` |
| `ProjectSummaryBuilder` | Texto do resumo para o prompt |

O scanner **não lê conteúdo** de arquivos. Ignora `.git`, `__pycache__`, `node_modules`, etc.

## Ambiente de desenvolvimento

```powershell
git clone https://github.com/nilknarfsam/CortexForge.git
cd CortexForge
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Validação básica

```powershell
python -m py_compile app.py ui\main_window.py ui\ollama_worker.py core\ollama_client.py core\config.py core\project_context.py core\project_scanner.py core\project_summary.py
```

### Executar

```powershell
python app.py
```

## Convenções

- Mensagens de erro amigáveis em português na UI.
- Logs de diagnóstico HTTP no **terminal** (`print`), não no chat.
- Sem novas dependências sem atualizar `requirements.txt`.
- Commits locais; **sem push automático** pela aplicação.

## O que não está implementado

- Histórico de conversa persistente
- Streaming de tokens
- RAG / embeddings / banco vetorial
- Leitura de conteúdo de arquivos do projeto
- Git integrado na UI
- Multiagentes orquestrados

Consulte [ROADMAP.md](ROADMAP.md).

## Documentação relacionada

| Arquivo | Conteúdo |
|---------|----------|
| [INSTALLATION.md](INSTALLATION.md) | Instalação e hardware |
| [QUICK_START.md](QUICK_START.md) | Uso em 5 minutos |
| [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | Erros comuns |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Arquitetura detalhada |
| [AGENTS.md](AGENTS.md) | Perfis de agentes |
| [CHANGELOG.md](../CHANGELOG.md) | Versões |

## Compartilhar alterações

1. Faça branch ou trabalhe em `main` localmente.
2. `git add` / `git commit` com mensagem clara.
3. `git push` manualmente quando quiser publicar (a aplicação não faz isso por você).

## Contato e issues

Use o rastreador de issues do GitHub para bugs e melhorias, com passos para reproduzir e logs do terminal quando aplicável.
