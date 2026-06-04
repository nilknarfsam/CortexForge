# Roadmap do CortexForge

Planejamento por versões. Escopo sujeito a ajustes conforme o repositório evolui.

## v0.5 — Seleção de projeto ✅

- Botão **Abrir Pasta** no painel de projetos
- Exibir nome e caminho da pasta selecionada
- Classe `ProjectContext` (`name`, `path`)
- Sem scanner, sem leitura de código, sem contexto no Ollama

## v0.6 — Geração assíncrona ✅

- `QThread` para `OllamaClient.generate()`
- Barra de status e bloco `Gerando resposta...` no chat
- UI responsiva durante a inferência

## v0.7 — Scanner simples de projeto ✅

- `ProjectScanner` com estatísticas (pastas, arquivos, extensões, tamanho)
- Exibição automática no painel ao abrir pasta
- Ignora `.git`, `__pycache__`, `node_modules`, etc.
- Sem leitura de conteúdo nem envio ao Ollama

## v0.8 — Contexto automático ✅

- Resumo textual via `ProjectSummaryBuilder` (dados do scanner)
- Prompt com `CONTEXTO DO PROJETO` e `PERGUNTA DO USUÁRIO`
- Resumo exibido no painel lateral; armazenado em memória

## v0.9 — Streaming de respostas ✅

- `generate(stream=True)` e tokens via `token_received`
- Chat atualizado progressivamente; spinner na barra de status

## v0.9b — Melhoria visual (planejado)

- Refinements de layout e painel de projetos

## v1.0 — Propostas de arquivos ✅

- Painel **Propostas**, parse de `# FILE:` / `Arquivo:`
- Visualização somente leitura + copiar conteúdo
- Sem aplicar alterações no disco automaticamente

## v1.1 — Aplicação de propostas (planejado)

- Diff visual e confirmação antes de gravar
- Botões aplicar / descartar

## Fora do escopo imediato

- Multiagentes orquestrados
- Memória vetorial / RAG
- Integração Git dentro da app
- Execução automática de código
- Plugins
- Push ou deploy automático

## Repositório

[github.com/nilknarfsam/CortexForge](https://github.com/nilknarfsam/CortexForge)
