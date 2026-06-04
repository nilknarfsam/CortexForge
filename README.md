# CortexForge

Assistente desktop local de programação, construído em Python com **PySide6** e integrado ao **Ollama**.

Repositório: [github.com/nilknarfsam/CortexForge](https://github.com/nilknarfsam/CortexForge)

## Objetivo

Oferecer um ambiente simples para conversar com modelos locais (via Ollama), usando perfis de agente especializados (arquitetura, código e revisão), sem depender de serviços em nuvem.

## Visão geral

O CortexForge é uma aplicação desktop com:

- **Painel de projetos** — seleção de pasta de trabalho (a partir da v0.5)
- **Chat central** — mensagens do usuário e respostas do assistente
- **Barra superior** — modelo Ollama, agente ativo e atualização de modelos

Toda a inferência ocorre na máquina do usuário, através do Ollama em `http://localhost:11434`.

## Requisitos

- Python 3.10 ou superior
- [Ollama](https://ollama.com/) instalado e em execução (`ollama serve`)
- Pelo menos um modelo baixado (ex.: `ollama pull llama3.2`)

## Instalação

```powershell
cd CortexForge
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Como executar

```powershell
python app.py
```

Certifique-se de que o Ollama está ativo antes de enviar mensagens.

## Como usar

1. Abra a aplicação e aguarde a verificação do Ollama na área de chat.
2. Selecione um **modelo** na barra superior (use **Atualizar** para recarregar a lista).
3. Escolha um **agente**: Architect, Coder ou Reviewer.
4. (Opcional, v0.5+) No painel **Projetos**, clique em **Abrir Pasta** e selecione o diretório do seu projeto.
5. Digite sua mensagem no campo inferior e pressione **Enter**.
6. A resposta aparecerá como `[CortexForge]` no chat.

## Integração com Ollama

O módulo `core/ollama_client.py` comunica-se com a API local:

| Operação        | Endpoint        |
|-----------------|-----------------|
| Disponibilidade | `GET /api/tags` |
| Listar modelos  | `GET /api/tags` |
| Gerar texto     | `POST /api/generate` |

Mensagens de erro são exibidas de forma amigável na interface.

## Agentes atuais

| Agente    | Arquivo              | Foco                          |
|-----------|----------------------|-------------------------------|
| Architect | `agents/architect.txt` | Arquitetura e design de software |
| Coder     | `agents/coder.txt`     | Implementação e código        |
| Reviewer  | `agents/reviewer.txt`  | Revisão e qualidade           |

O agente padrão é **Coder**. Detalhes em [docs/AGENTS.md](docs/AGENTS.md).

## Roadmap

Consulte [docs/ROADMAP.md](docs/ROADMAP.md) para versões planejadas (scanner, contexto automático, UI assíncrona, v1.0).

## Documentação adicional

- [CHANGELOG.md](CHANGELOG.md) — histórico de versões
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) — estrutura e fluxo do código
- [docs/AGENTS.md](docs/AGENTS.md) — perfis de agentes

## Privacidade e execução local

O CortexForge **roda inteiramente na sua máquina**. Não envia dados automaticamente para repositórios remotos nem realiza **push** automático no Git. Commits e publicação no GitHub são responsabilidade do desenvolvedor.

## Licença

Definir conforme política do repositório no GitHub.
