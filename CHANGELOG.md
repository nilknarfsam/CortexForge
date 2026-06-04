# Changelog

Todas as mudanças notáveis do CortexForge são documentadas neste arquivo.

O formato segue [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/).

## [Unreleased]

### Planejado

- Contexto automático no prompt (v0.8)

## [0.7.0] - 2026-06-04

### Adicionado

- `ProjectScanner` e `ProjectScanResult` em `core/project_scanner.py`
- Estatísticas no painel de projetos ao abrir pasta (pastas, arquivos, extensões, flags, tamanho)
- Varredura sem leitura de conteúdo; pastas `.git`, `__pycache__`, etc. ignoradas

## [0.6.0] - 2026-06-04

### Adicionado

- Geração assíncrona com `QThread` (`ui/ollama_worker.py`)
- Barra de status inferior (Pronto / Gerando resposta... / Erro)
- Indicador no chat: `[CortexForge] Gerando resposta...` com substituição ao concluir

### Alterado

- Controles desabilitados durante geração (entrada, Abrir Pasta, Atualizar)
- Removida lógica de remoção de texto via `QTextCursor` (`Pensando...`)

## [0.5.0] - 2026-06-04

### Adicionado

- Seleção de pasta de projeto no painel lateral (**Abrir Pasta**)
- Classe `ProjectContext` em `core/project_context.py`
- Exibição do nome e caminho completo da pasta selecionada

## [0.4.0] - 2026-06-04

### Adicionado

- Perfis de agentes em `agents/*.txt` (Architect, Coder, Reviewer)
- `core/config.py` com `DEFAULT_AGENT` e carregamento de prompts
- ComboBox de agente na barra superior
- Concatenação do prompt do agente com a mensagem do usuário antes de `generate()`

## [0.3.0] - 2026-06-04

### Adicionado

- Envio de mensagens com **Enter**
- Exibição de `[Você]` e `[CortexForge]` no chat
- Indicador `Pensando...` e desabilitação do campo durante a geração
- Tratamento de erros amigável no chat

## [0.2.0] - 2026-06-04

### Adicionado

- `OllamaClient` com `is_available()`, `list_models()` e `generate()`
- Integração HTTP com Ollama via `requests`
- Barra superior com ComboBox de modelos e botão **Atualizar**
- Mensagens de sistema no chat ao conectar/listar modelos

## [0.1.0] - 2026-06-04

### Adicionado

- Estrutura inicial do projeto (PySide6)
- `MainWindow` com painel de projetos, chat e campo de entrada
- `OllamaClient` como stub
- Pastas reservadas `agents/` e `projects/`
