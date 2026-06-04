"""
Configuração central do CortexForge.

Define o agente padrão e caminhos dos perfis em agents/.
"""

from pathlib import Path

# Agente selecionado ao iniciar a aplicação (chave interna).
DEFAULT_AGENT = "coder"

# Raiz do projeto (pasta que contém app.py).
PROJECT_ROOT = Path(__file__).resolve().parent.parent
AGENTS_DIR = PROJECT_ROOT / "agents"

# Chave do agente -> arquivo de prompt em agents/.
AGENT_FILES: dict[str, str] = {
    "architect": "architect.txt",
    "coder": "coder.txt",
    "reviewer": "reviewer.txt",
}

# Chave do agente -> rótulo exibido no ComboBox.
AGENT_LABELS: dict[str, str] = {
    "architect": "Architect",
    "coder": "Coder",
    "reviewer": "Reviewer",
}


def load_agent_prompt(agent_id: str) -> tuple[str | None, str | None]:
    """
    Carrega o prompt de sistema do agente a partir de agents/.

    Returns:
        Tupla (texto do prompt, mensagem de erro). Em sucesso, o erro é None.
    """
    filename = AGENT_FILES.get(agent_id)
    if not filename:
        return None, f"Agente desconhecido: {agent_id}"

    path = AGENTS_DIR / filename
    if not path.is_file():
        return None, f"Arquivo do agente não encontrado: {filename}"

    try:
        content = path.read_text(encoding="utf-8").strip()
        if not content:
            return None, f"O perfil do agente está vazio: {filename}"
        return content, None
    except OSError as exc:
        return None, f"Erro ao ler perfil do agente: {exc}"


def build_prompt(agent_system: str, user_message: str) -> str:
    """Concatena o prompt do agente com a mensagem do usuário."""
    return f"{agent_system}\n\n{user_message}"
