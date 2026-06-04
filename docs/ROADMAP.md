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

## v0.7 — Scanner simples de projeto

- Varredura básica da árvore de arquivos da pasta aberta
- Ignorar pastas comuns (`.git`, `__pycache__`, `node_modules`, etc.)
- Listar ou resumir arquivos relevantes na UI ou em estrutura interna
- Ainda sem enviar conteúdo completo ao modelo

## v0.8 — Contexto automático

- Incluir trechos ou resumo do projeto no prompt enviado ao Ollama
- Limites de tamanho para caber no contexto do modelo local
- Integração entre `ProjectContext`, scanner e `build_prompt()`

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
