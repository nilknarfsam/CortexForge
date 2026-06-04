# Solução de problemas — CortexForge

Problemas comuns e como resolvê-los. O CortexForge registra detalhes de erros HTTP no **terminal** onde `python app.py` foi executado.

## Ollama não conecta

**Sintoma:** `[Sistema] Não foi possível conectar ao Ollama...` ou ComboBox com `Ollama indisponível`.

**Soluções:**

1. Verifique se o Ollama está instalado e em execução.
2. Teste a API:

```powershell
curl http://localhost:11434/api/tags
```

3. Reinicie o serviço Ollama (tray icon no Windows ou `ollama serve`).
4. Confirme que nenhum firewall bloqueia a porta **11434**.

---

## Lista de modelos vazia

**Sintoma:** Após **Atualizar**, nenhum modelo aparece.

**Soluções:**

1. Baixe o modelo recomendado:

```powershell
ollama pull qwen2.5-coder:7b
```

2. Clique em **Atualizar** novamente.
3. Verifique modelos instalados:

```powershell
ollama list
```

---

## Erro HTTP 500

**Sintoma:** No chat: `Erro: Erro HTTP 500`.

**Causas frequentes:**

- Modelo não carregado ou nome incorreto no ComboBox
- **RAM insuficiente** (mínimo 8 GB; recomendado 16 GB para `qwen2.5-coder:7b`)
- Prompt muito longo (projeto grande + contexto + agente)
- Ollama travado ou processo `ollama` com falha interna

**O que fazer:**

1. Leia o terminal da aplicação — após v0.8.1 aparecem:

```text
STATUS
500
BODY
{ ... JSON de erro do Ollama ... }
Modelo utilizado: ...
Tamanho do prompt: ...
Primeiros 500 caracteres do prompt:
...
```

2. Reinicie o Ollama e tente uma mensagem **curta** sem projeto aberto.
3. Feche outros programas que consumam RAM.
4. Teste o modelo direto no terminal:

```powershell
ollama run qwen2.5-coder:7b
```

Se falhar fora do CortexForge, o problema é no Ollama/modelo, não na aplicação.

---

## Erro HTTP 404

**Sintoma:** `Erro: Erro HTTP 404`.

**Soluções:**

- O nome do modelo no ComboBox deve coincidir com `ollama list` (ex.: `qwen2.5-coder:7b`).
- Execute `ollama pull <nome-exato>`.

---

## Geração muito lenta

**Sintoma:** **Gerando resposta...** por muitos minutos.

**Soluções:**

- Normal em CPU sem GPU e com 8 GB de RAM.
- Use modelo menor ou hardware com mais RAM.
- Reduza o tamanho do contexto: feche projeto grande ou use perguntas mais curtas.

---

## `ModuleNotFoundError: PySide6`

**Sintoma:** Erro ao executar `python app.py`.

**Soluções:**

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Confirme que o ambiente virtual está ativo antes de `python app.py`.

---

## Janela não abre (Windows)

**Soluções:**

- Execute a partir do PowerShell com venv ativo.
- Instale dependências visuais do Qt se necessário (reinstalar PySide6: `pip install --force-reinstall PySide6`).

---

## Agente ou perfil não encontrado

**Sintoma:** `Erro: Arquivo do agente não encontrado`.

**Soluções:**

- Verifique se existem `agents/architect.txt`, `agents/coder.txt`, `agents/reviewer.txt`.
- Não apague nem renomeie esses arquivos sem atualizar `core/config.py`.

---

## Projeto aberto sem estatísticas

**Sintoma:** Painel não atualiza após **Abrir Pasta**.

**Soluções:**

- Confirme que selecionou uma **pasta**, não um arquivo.
- Pastas muito grandes podem demorar alguns segundos (varredura síncrona).
- Verifique permissão de leitura no caminho.

---

## Diagnóstico avançado (HTTP)

O `OllamaClient` expõe `debug_generate_payload(prompt, model)` — retorna o JSON exato enviado a `/api/generate`. Útil para depuração em console Python:

```python
from core.ollama_client import OllamaClient
client = OllamaClient()
client.model = "qwen2.5-coder:7b"
print(client.debug_generate_payload("teste"))
```

---

## Ainda com problemas?

1. Consulte [INSTALLATION.md](INSTALLATION.md) — requisitos de hardware.
2. Veja issues no GitHub: [github.com/nilknarfsam/CortexForge](https://github.com/nilknarfsam/CortexForge).
3. Inclua no relato: SO, RAM, modelo Ollama, mensagem do chat e saída `STATUS`/`BODY` do terminal.
