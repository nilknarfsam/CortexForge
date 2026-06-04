"""
Scanner simples de projeto — apenas estatísticas de pastas e arquivos.

Não lê conteúdo dos arquivos nem usa IA/Ollama.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

# Pastas ignoradas na varredura (metadados, caches, ambientes virtuais).
_SKIP_DIR_NAMES = {
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    "node_modules",
    ".idea",
    ".vscode",
}


@dataclass
class ProjectScanResult:
    """Estatísticas coletadas de uma pasta de projeto."""

    total_folders: int
    total_files: int
    py_files: int
    md_files: int
    txt_files: int
    has_readme: bool
    has_requirements: bool
    has_pyproject: bool
    total_size_bytes: int


class ProjectScanner:
    """Varre a árvore de diretórios e coleta estatísticas do projeto."""

    def __init__(self, project_path: str | Path) -> None:
        """
        Args:
            project_path: Caminho da pasta raiz do projeto.
        """
        self._root = Path(project_path).expanduser().resolve()

    def scan(self) -> ProjectScanResult:
        """
        Percorre o projeto e retorna contagens e flags de arquivos na raiz.

        Não abre nem analisa o conteúdo dos arquivos.
        """
        if not self._root.is_dir():
            return ProjectScanResult(
                total_folders=0,
                total_files=0,
                py_files=0,
                md_files=0,
                txt_files=0,
                has_readme=False,
                has_requirements=False,
                has_pyproject=False,
                total_size_bytes=0,
            )

        total_folders = 0
        total_files = 0
        py_files = 0
        md_files = 0
        txt_files = 0
        total_size_bytes = 0

        for dirpath, dirnames, filenames in self._walk_dirs():
            total_folders += 1
            for name in filenames:
                file_path = dirpath / name
                if not file_path.is_file():
                    continue
                total_files += 1
                try:
                    total_size_bytes += file_path.stat().st_size
                except OSError:
                    pass

                suffix = file_path.suffix.lower()
                if suffix == ".py":
                    py_files += 1
                elif suffix == ".md":
                    md_files += 1
                elif suffix == ".txt":
                    txt_files += 1

        return ProjectScanResult(
            total_folders=total_folders,
            total_files=total_files,
            py_files=py_files,
            md_files=md_files,
            txt_files=txt_files,
            has_readme=(self._root / "README.md").is_file(),
            has_requirements=(self._root / "requirements.txt").is_file(),
            has_pyproject=(self._root / "pyproject.toml").is_file(),
            total_size_bytes=total_size_bytes,
        )

    def _walk_dirs(self):
        """Gera (dirpath, dirnames, filenames) ignorando pastas irrelevantes."""
        stack: list[Path] = [self._root]
        while stack:
            current = stack.pop()
            try:
                entries = list(current.iterdir())
            except OSError:
                continue

            dirnames: list[str] = []
            filenames: list[str] = []
            for entry in entries:
                if entry.is_dir():
                    if entry.name not in _SKIP_DIR_NAMES:
                        dirnames.append(entry.name)
                        stack.append(entry)
                elif entry.is_file():
                    filenames.append(entry.name)

            yield current, dirnames, filenames
