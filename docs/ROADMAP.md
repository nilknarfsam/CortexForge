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

## v0.9 — Melhoria visual

- Pequenos refinements de layout e usabilidade
- Ajustes na barra de status e no painel de projetos

## v1.0 — Primeira versão utilizável

- Fluxo estável: abrir projeto → escolher agente/modelo → chat com contexto útil
- Documentação e CHANGELOG alinhados
- Experiência consistente para uso diário em desenvolvimento local
- Critérios de “utilizável” definidos e validados manualmente

## Fora do escopo imediato

- Multiagentes orquestrados
- Memória vetorial / RAG
- Integração Git dentro da app
- Execução automática de código
- Plugins
- Push ou deploy automático

## Repositório

[github.com/nilknarfsam/CortexForge](https://github.com/nilknarfsam/CortexForge)
