# Instalação do CortexForge

Guia completo para preparar o ambiente e executar o CortexForge em sua máquina.

Repositório: [github.com/nilknarfsam/CortexForge](https://github.com/nilknarfsam/CortexForge)

## Requisitos mínimos

| Componente | Mínimo |
|------------|--------|
| **CPU** | 4 núcleos |
| **RAM** | 8 GB |
| **Disco** | ~5 GB livres (Python, dependências e um modelo Ollama) |
| **Sistema** | Windows 10+, Linux ou macOS |
| **Python** | 3.10 ou superior |
| **Ollama** | Versão recente ([ollama.com](https://ollama.com/)) |

## Hardware recomendado

| Componente | Recomendado |
|------------|-------------|
| **CPU** | 6+ núcleos |
| **RAM** | **16 GB** (modelos locais consomem bastante memória) |
| **GPU** | Opcional; acelera inferência se o Ollama usar CUDA/Metal |

Com 8 GB de RAM, modelos menores podem funcionar, mas respostas lentas ou erros HTTP (ex.: 500 por falta de memória) são mais comuns.

## Modelo recomendado

Para desenvolvimento e programação, o projeto recomenda:

```text
qwen2.5-coder:7b
```

Instalação:

```powershell
ollama pull qwen2.5-coder:7b
```

Outros modelos compatíveis com Ollama podem ser usados; selecione-os no ComboBox **Modelo** dentro da aplicação.

## Instalação do Python

### Windows

1. Baixe o instalador em [python.org/downloads](https://www.python.org/downloads/).
2. Marque **Add python.exe to PATH** durante a instalação.
3. Verifique no terminal:

```powershell
python --version
```

### Linux / macOS

Use o gerenciador do sistema ou [pyenv](https://github.com/pyenv/pyenv). Exemplo (Debian/Ubuntu):

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip
python3 --version
```

## Instalação do Ollama

1. Baixe e instale em [ollama.com/download](https://ollama.com/download).
2. Inicie o serviço (em geral inicia automaticamente após instalar).
3. Confirme que a API responde:

```powershell
curl http://localhost:11434/api/tags
```

Ou, no PowerShell:

```powershell
Invoke-WebRequest -Uri http://localhost:11434/api/tags -UseBasicParsing
```

4. Baixe o modelo recomendado:

```powershell
ollama pull qwen2.5-coder:7b
```

## Instalação do CortexForge

### 1. Clonar o repositório

```powershell
git clone https://github.com/nilknarfsam/CortexForge.git
cd CortexForge
```

### 2. Ambiente virtual

**Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**Linux / macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Dependências

O arquivo `requirements.txt` contém:

- `PySide6` — interface desktop
- `requests` — cliente HTTP para o Ollama

Nenhuma dependência adicional é necessária para uso básico.

## Como iniciar

Com o ambiente virtual ativo e o Ollama em execução:

```powershell
python app.py
```

A janela **CortexForge v0.8** deve abrir. A barra de status inferior inicia em **Pronto**.

## Verificação pós-instalação

1. No chat, deve aparecer `[Sistema] Ollama está disponível.`
2. O ComboBox **Modelo** lista modelos instalados (use **Atualizar** se necessário).
3. Envie uma mensagem de teste com o agente **Coder** e o modelo `qwen2.5-coder:7b`.

## Próximos passos

- Uso rápido: [QUICK_START.md](QUICK_START.md)
- Problemas: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- Desenvolvimento: [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md)

## Compartilhamento do projeto

Para compartilhar com outra pessoa:

1. Envie o link do repositório GitHub ou um clone/arquivo compactado do projeto.
2. Indique que é necessário instalar **Python**, **Ollama** e o modelo **qwen2.5-coder:7b**.
3. Não inclua a pasta `.venv` nem modelos Ollama (ficam na máquina de cada usuário).
4. O CortexForge **não faz push automático** nem envia dados para a nuvem.

## Privacidade

Toda inferência ocorre localmente em `http://localhost:11434`. Seus arquivos de projeto não são enviados a servidores externos pelo CortexForge; apenas um **resumo estatístico** (pastas, contagens, tamanho) pode ser incluído no prompt quando uma pasta está aberta.
