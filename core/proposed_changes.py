"""
Detecção e armazenamento em memória de arquivos propostos pelo modelo.

Não grava nem altera arquivos no disco — apenas parse da resposta do chat.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class FileActionType(Enum):
    """Tipo de alteração sugerida para o arquivo."""

    CREATE_FILE = "CREATE_FILE"
    MODIFY_FILE = "MODIFY_FILE"


@dataclass
class ProposedFile:
    """Arquivo proposto extraído de uma resposta do modelo."""

    file_name: str
    relative_path: str
    content: str
    action_type: FileActionType


# Marcadores aceitos na resposta do modelo.
_FILE_MARKER_PATTERN = re.compile(
    r"(?:^#\s*FILE:\s*|^Arquivo:\s*)(.+?)\s*$",
    re.MULTILINE | re.IGNORECASE,
)


class ProposedChangesParser:
    """Extrai blocos de arquivo a partir do texto gerado pelo Ollama."""

    def __init__(self, project_root: str | Path | None = None) -> None:
        """
        Args:
            project_root: Pasta do projeto aberto (para CREATE vs MODIFY).
        """
        self._project_root = (
            Path(project_root).resolve() if project_root else None
        )

    def parse(self, response_text: str) -> list[ProposedFile]:
        """
        Identifica propostas no formato ``# FILE:`` ou ``Arquivo:``.

        Returns:
            Lista de ProposedFile (pode estar vazia).
        """
        if not response_text.strip():
            return []

        matches = list(_FILE_MARKER_PATTERN.finditer(response_text))
        if not matches:
            return []

        proposed: list[ProposedFile] = []
        for index, match in enumerate(matches):
            path_raw = match.group(1).strip().strip("\"'")
            content_start = match.end()
            content_end = (
                matches[index + 1].start()
                if index + 1 < len(matches)
                else len(response_text)
            )
            content = _normalize_content(response_text[content_start:content_end])
            file_name, relative_path = _split_path(path_raw)
            action_type = _resolve_action_type(self._project_root, relative_path)

            proposed.append(
                ProposedFile(
                    file_name=file_name,
                    relative_path=relative_path,
                    content=content,
                    action_type=action_type,
                )
            )

        return proposed


def _split_path(path_raw: str) -> tuple[str, str]:
    """Separa nome do arquivo e caminho relativo."""
    normalized = path_raw.replace("\\", "/").lstrip("./")
    path = Path(normalized)
    return path.name, normalized


def _normalize_content(raw: str) -> str:
    """Remove cercas markdown e espaços extras do conteúdo extraído."""
    text = raw.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines).strip()
    return text


def _resolve_action_type(
    project_root: Path | None, relative_path: str
) -> FileActionType:
    """Define CREATE ou MODIFY conforme existência do arquivo no projeto."""
    if project_root is None:
        return FileActionType.CREATE_FILE

    target = project_root / relative_path
    if target.is_file():
        return FileActionType.MODIFY_FILE
    return FileActionType.CREATE_FILE

