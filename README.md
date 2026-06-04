# CortexForge

Assistente desktop local de programação, construído em Python com **PySide6** e integrado ao **Ollama**.

Repositório: [github.com/nilknarfsam/CortexForge](https://github.com/nilknarfsam/CortexForge)

## Objetivo

Oferecer um ambiente simples para conversar com modelos locais (via Ollama), usando perfis de agente especializados (arquitetura, código e revisão), sem depender de serviços em nuvem.

## Visão geral

O CortexForge é uma aplicação desktop com:

- **Painel de projetos** — seleção de pasta, estatísticas e resumo automático
- **Chat central** — mensagens do usuário e respostas do assistente (geração assíncrona)
- **Barra superior** — modelo Ollama, agente ativo e atualização de modelos
- **Barra de status** — Pronto / spinner + Gerando... / Erro
- **Streaming** — respostas do Ollama exibidas token a token no chat

Toda a inferência ocorre na máquina do usuário, através do Ollama em `http://localhost:11434`.

## Requisitos mínimos

| Componente | Especificação |
|------------|---------------|
| **CPU** | 4 núcleos |
| **RAM** | 8 GB |
| **Recomendado (RAM)** | **16 GB** |
| **Python** | 3.10 ou superior |
| **Ollama** | Instalado e em execução |

### Modelo recomendado

```text
qwen2.5-coder:7b
```

```powershell
ollama pull qwen2.5-coder:7b
```

Guia completo de instalação: **[docs/INSTALLATION.md](docs/INSTALLATION.md)**

## Início rápido

```powershell
git clone https://github.com/nilknarfsam/CortexForge.git
cd CortexForge
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
ollama pull qwen2.5-coder:7b
python app.py
```

Passo a passo detalhado: **[docs/QUICK_START.md](docs/QUICK_START.md)**

## Como usar (resumo)

1. Inicie o app e confirme **Ollama está disponível** no chat.
2. Selecione o **modelo** (ex.: `qwen2.5-coder:7b`) e clique em **Atualizar** se necessário.
3. Escolha o **agente**: Architect, Coder ou Reviewer.
4. (Opcional) **Abrir Pasta** no painel Projetos — exibe estatísticas e resumo no contexto do chat.
5. Digite a mensagem e pressione **Enter**.

## Estrutura interna do CortexForge

```
CortexForge/
├── app.py                 # Entrada da aplicação
├── core/                  # Ollama, config, scanner, resumo de projeto
├── ui/                    # MainWindow e worker assíncrono
├── agents/                # Prompts Architect, Coder, Reviewer
└── docs/                  # Documentação
```

Detalhes: **[docs/DEVELOPER_GUIDE.md](docs/DEVELOPER_GUIDE.md)** e **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)**

## Integração com Ollama

| Operação        | Endpoint           |
|-----------------|--------------------|
| Disponibilidade | `GET /api/tags`    |
| Listar modelos  | `GET /api/tags`    |
| Gerar texto     | `POST /api/generate` |

Erros HTTP são diagnosticados no terminal (status, corpo, modelo, tamanho do prompt). No chat: mensagens como `Erro HTTP 500`.

## Agentes atuais

| Agente    | Arquivo                | Foco                           |
|-----------|------------------------|--------------------------------|
| Architect | `agents/architect.txt` | Arquitetura e design           |
| Coder     | `agents/coder.txt`     | Implementação (padrão)         |
| Reviewer  | `agents/reviewer.txt`  | Revisão e qualidade            |

Detalhes: **[docs/AGENTS.md](docs/AGENTS.md)**

## Problemas comuns

| Problema | Onde ver ajuda |
|----------|----------------|
| Ollama não conecta | [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) |
| Erro HTTP 500 | Terminal + [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) |
| Modelo não listado | `ollama pull qwen2.5-coder:7b` |
| `ModuleNotFoundError` | Ativar venv e `pip install -r requirements.txt` |

## Documentação

| Documento | Descrição |
|-----------|-----------|
| [INSTALLATION.md](docs/INSTALLATION.md) | Instalação, hardware, Ollama, compartilhamento |
| [QUICK_START.md](docs/QUICK_START.md) | Primeiros passos |
| [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) | Solução de problemas |
| [DEVELOPER_GUIDE.md](docs/DEVELOPER_GUIDE.md) | Estrutura interna e desenvolvimento |
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | Módulos e fluxo do prompt |
| [AGENTS.md](docs/AGENTS.md) | Perfis de agentes |
| [ROADMAP.md](docs/ROADMAP.md) | Versões planejadas |
| [CHANGELOG.md](CHANGELOG.md) | Histórico de versões |

## Roadmap

Consulte [docs/ROADMAP.md](docs/ROADMAP.md) para versões planejadas (v0.9+, v1.0).

## Privacidade e execução local

O CortexForge **roda inteiramente na sua máquina**. Não envia dados automaticamente para repositórios remotos nem realiza **push** automático no Git. Commits e publicação no GitHub são responsabilidade do desenvolvedor.

## Licença

Definir conforme política do repositório no GitHub.
