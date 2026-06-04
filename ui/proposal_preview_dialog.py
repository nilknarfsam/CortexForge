"""
Diálogo somente leitura para visualizar uma proposta de arquivo.
"""

from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
)

from core.proposed_changes import ProposedFile


class ProposalPreviewDialog(QDialog):
    """Exibe nome e conteúdo da proposta; permite copiar para a área de transferência."""

    def __init__(self, proposed: ProposedFile, parent=None) -> None:
        super().__init__(parent)
        self._proposed = proposed
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Monta layout do diálogo."""
        self.setWindowTitle(f"Proposta: {self._proposed.file_name}")
        self.resize(640, 480)

        layout = QVBoxLayout(self)

        name_label = QLabel(f"Arquivo: {self._proposed.file_name}")
        name_label.setWordWrap(True)
        layout.addWidget(name_label)

        path_label = QLabel(f"Caminho: {self._proposed.relative_path}")
        path_label.setWordWrap(True)
        path_label.setStyleSheet("color: gray;")
        layout.addWidget(path_label)

        action_label = QLabel(f"Ação: {self._proposed.action_type.value}")
        layout.addWidget(action_label)

        content_view = QTextEdit()
        content_view.setReadOnly(True)
        content_view.setPlainText(self._proposed.content)
        layout.addWidget(content_view, stretch=1)

        buttons = QHBoxLayout()
        copy_btn = QPushButton("Copiar Conteúdo")
        copy_btn.clicked.connect(self._copy_content)
        buttons.addWidget(copy_btn)

        close_btn = QPushButton("Fechar")
        close_btn.clicked.connect(self.accept)
        buttons.addWidget(close_btn)
        buttons.addStretch()

        layout.addLayout(buttons)

    def _copy_content(self) -> None:
        """Copia o conteúdo proposto para a área de transferência."""
        QGuiApplication.clipboard().setText(self._proposed.content)
