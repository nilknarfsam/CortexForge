"""
Gera resumo textual do projeto a partir do resultado do scanner.

Sem IA, sem leitura de conteúdo de arquivos — apenas estatísticas.
"""

from __future__ import annotations

from core.project_scanner import ProjectScanResult


class ProjectSummaryBuilder:
    """Monta um resumo em texto a partir de ProjectScanResult."""

    def __init__(self, project_name: str, project_path: str) -> None:
        """
        Args:
            project_name: Nome da pasta do projeto.
            project_path: Caminho absoluto do projeto.
        """
        self._project_name = project_name
        self._project_path = project_path

    def build(self, scan: ProjectScanResult) -> str:
        """
        Gera o resumo textual para contexto dos agentes e exibição na UI.

        Args:
            scan: Resultado de ProjectScanner.scan().
        """
        yes_no = lambda value: "sim" if value else "não"
        size = self._format_size(scan.total_size_bytes)

        return (
            f"Nome: {self._project_name}\n"
            f"Caminho: {self._project_path}\n"
            f"Pastas: {scan.total_folders}\n"
            f"Arquivos: {scan.total_files}\n"
            f"Arquivos Python: {scan.py_files}\n"
            f"Arquivos Markdown: {scan.md_files}\n"
            f"README presente: {yes_no(scan.has_readme)}\n"
            f"requirements.txt presente: {yes_no(scan.has_requirements)}\n"
            f"Tamanho total: {size}"
        )

    @staticmethod
    def _format_size(size_bytes: int) -> str:
        """Converte bytes em texto legível."""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        if size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        if size_bytes < 1024 * 1024 * 1024:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
        return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"


def build_prompt_with_context(
    agent_system: str,
    project_summary: str | None,
    user_message: str,
) -> str:
    """
    Monta o prompt completo: agente + contexto do projeto (se houver) + pergunta.

    Args:
        agent_system: Prompt do agente selecionado.
        project_summary: Resumo em memória ou None se nenhum projeto aberto.
        user_message: Texto digitado pelo usuário.
    """
    if project_summary:
        body = (
            f"CONTEXTO DO PROJETO\n{project_summary}\n\n"
            f"PERGUNTA DO USUÁRIO\n{user_message}"
        )
    else:
        body = user_message

    return f"{agent_system}\n\n{body}"
