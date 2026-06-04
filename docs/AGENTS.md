# Agentes do CortexForge

O CortexForge usa **perfis de agente** definidos em arquivos de texto. Cada perfil adiciona um prompt de sistema antes da mensagem do usuário ao chamar o Ollama.

## Agentes disponíveis

### Architect

- **Arquivo:** `agents/architect.txt`
- **Rótulo na UI:** Architect
- **Papel:** Ajudar na definição de arquitetura de software — estrutura, módulos, responsabilidades, fluxos e trade-offs.
- **Comportamento esperado:** Respostas conceituais, pouco código, suposições explícitas quando faltar contexto.

### Coder

- **Arquivo:** `agents/coder.txt`
- **Rótulo na UI:** Coder
- **Papel:** Ajudar na implementação — código, correções, refatorações e exemplos.
- **Comportamento esperado:** Código claro e direto; agente **padrão** (`DEFAULT_AGENT = "coder"` em `core/config.py`).

### Reviewer

- **Arquivo:** `agents/reviewer.txt`
- **Rótulo na UI:** Reviewer
- **Papel:** Revisar código e propostas técnicas — qualidade, riscos e melhorias.
- **Comportamento esperado:** Feedback priorizado (crítico, importante, sugestão), sem reescrever o projeto inteiro.

## Como o agente é aplicado

1. O usuário seleciona o agente no ComboBox **Agente**.
2. Ao pressionar Enter, `load_agent_prompt()` lê o `.txt` correspondente.
3. `build_prompt()` concatena:

   ```
   <conteúdo do architect.txt | coder.txt | reviewer.txt>

   <mensagem do usuário>
   ```

4. O texto combinado é enviado a `OllamaClient.generate()`.

## Como editar os prompts `.txt`

1. Feche a aplicação (ou edite com cuidado enquanto ela está fechada).
2. Abra o arquivo desejado em `agents/`, por exemplo `agents/coder.txt`.
3. Altere o texto em UTF-8. Mantenha instruções claras e objetivas.
4. Salve o arquivo e reinicie o CortexForge (ou envie uma nova mensagem — o arquivo é lido a cada envio).

**Dicas:**

- Use regras numeradas ou em tópicos para o modelo seguir melhor.
- Evite prompts excessivamente longos se o modelo local tiver limite de contexto.
- Para um novo agente no futuro, será necessário adicionar entrada em `AGENT_FILES` e `AGENT_LABELS` em `core/config.py` e um item no ComboBox (hoje feito automaticamente a partir de `AGENT_LABELS`).

## O que os agentes ainda não fazem

- Não trocam de modelo Ollama automaticamente.
- Não mantêm memória entre mensagens.
- Não leem arquivos do projeto (isso está planejado para v0.6+).
- Não executam código nem comandos de terminal.
