"""
Contexto da pasta de projeto selecionada pelo usuário.

Na v0.5 apenas armazena nome e caminho; sem leitura de arquivos.
"""

from pathlib import Path


class ProjectContext:
    """Representa a pasta de projeto aberta na aplicação."""

    def __init__(self, path: str | Path) -> None:
        """
        Args:
            path: Caminho da pasta selecionada pelo usuário.
        """
        resolved = Path(path).expanduser().resolve()
        self.path: str = str(resolved)
        self.name: str = resolved.name
