"""
Janela principal do CortexForge.

Layout em três zonas: painel de projetos (esquerda), área de chat (centro)
e campo de entrada de mensagens (inferior). Barra superior para seleção de modelo Ollama.
"""

from PySide6.QtCore import Qt
from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import (
    QComboBox,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from core.config import (
    AGENT_LABELS,
    DEFAULT_AGENT,
    build_prompt,
    load_agent_prompt,
)
from core.ollama_client import OllamaClient
from core.project_context import ProjectContext
from core.project_scanner import ProjectScanResult, ProjectScanner
from ui.ollama_worker import OllamaGenerateWorker

# Bloco exibido no chat enquanto a geração está em andamento.
_PENDING_RESPONSE_BLOCK = "[CortexForge]\nGerando resposta..."


class MainWindow(QMainWindow):
    """Janela principal da aplicação."""

    def __init__(self) -> None:
        super().__init__()
        self._ollama_client = OllamaClient()
        self._project_context: ProjectContext | None = None
        self._generate_worker: OllamaGenerateWorker | None = None
        self._is_generating = False

        self._setup_window()
        self._build_ui()
        self._refresh_ollama_models()

    def _setup_window(self) -> None:
        """Define título, tamanho e barra de status."""
        self.setWindowTitle("CortexForge v0.7")
        self.resize(960, 640)
        self.statusBar().showMessage("Pronto")

    def _build_ui(self) -> None:
        """Monta o layout: barra Ollama, projetos | chat + entrada."""
        central = QWidget()
        self.setCentralWidget(central)

        outer_layout = QVBoxLayout(central)
        outer_layout.setContentsMargins(8, 8, 8, 8)
        outer_layout.setSpacing(8)

        # --- Barra superior: modelo Ollama ---
        outer_layout.addWidget(self._create_ollama_toolbar())

        # --- Corpo: projetos | chat ---
        body = QWidget()
        root_layout = QHBoxLayout(body)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(8)

        projects_panel = self._create_projects_panel()
        root_layout.addWidget(projects_panel)

        chat_area = self._create_chat_area()
        root_layout.addWidget(chat_area, stretch=1)

        outer_layout.addWidget(body, stretch=1)

    def _create_ollama_toolbar(self) -> QWidget:
        """Barra com seleção de modelo, agente e botão para recarregar modelos."""
        bar = QWidget()
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(QLabel("Modelo:"))

        self._model_combo = QComboBox()
        self._model_combo.setMinimumWidth(200)
        layout.addWidget(self._model_combo, stretch=1)

        layout.addWidget(QLabel("Agente:"))

        self._agent_combo = QComboBox()
        self._agent_combo.setMinimumWidth(140)
        for agent_id, label in AGENT_LABELS.items():
            self._agent_combo.addItem(label, agent_id)
        default_index = self._agent_combo.findData(DEFAULT_AGENT)
        if default_index >= 0:
            self._agent_combo.setCurrentIndex(default_index)
        layout.addWidget(self._agent_combo)

        self._refresh_btn = QPushButton("Atualizar")
        self._refresh_btn.clicked.connect(self._refresh_ollama_models)
        layout.addWidget(self._refresh_btn)

        return bar

    def _create_projects_panel(self) -> QFrame:
        """Painel lateral para listagem de projetos."""
        panel = QFrame()
        panel.setFrameShape(QFrame.Shape.StyledPanel)
        panel.setMinimumWidth(220)
        panel.setMaximumWidth(280)

        layout = QVBoxLayout(panel)
        title = QLabel("Projetos")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        self._open_project_btn = QPushButton("Abrir Pasta")
        self._open_project_btn.clicked.connect(self._open_project_folder)
        layout.addWidget(self._open_project_btn)

        self._project_name_label = QLabel("Nenhum projeto aberto.")
        self._project_name_label.setWordWrap(True)
        self._project_name_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self._project_name_label)

        self._project_path_label = QLabel("")
        self._project_path_label.setWordWrap(True)
        self._project_path_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self._project_path_label.setStyleSheet("color: gray;")
        layout.addWidget(self._project_path_label)

        self._project_stats_label = QLabel("")
        self._project_stats_label.setWordWrap(True)
        self._project_stats_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self._project_stats_label)
        layout.addStretch()

        return panel

    def _open_project_folder(self) -> None:
        """Abre diálogo para selecionar pasta e exibe nome e caminho no painel."""
        folder = QFileDialog.getExistingDirectory(
            self,
            "Abrir Pasta de Projeto",
            "",
        )
        if not folder:
            return

        self._project_context = ProjectContext(folder)
        self._project_name_label.setText(self._project_context.name)
        self._project_path_label.setText(self._project_context.path)

        scan = ProjectScanner(self._project_context.path).scan()
        self._project_stats_label.setText(self._format_scan_stats(scan))

        self._append_system_message(
            f"Projeto aberto: {self._project_context.name} "
            f"({scan.total_files} arquivos, {scan.total_folders} pastas)"
        )

    def _format_scan_stats(self, scan: ProjectScanResult) -> str:
        """Formata estatísticas do scanner para exibição no painel."""
        size = self._format_size(scan.total_size_bytes)
        yes_no = lambda value: "Sim" if value else "Não"

        return (
            "Estatísticas:\n"
            f"Pastas: {scan.total_folders}\n"
            f"Arquivos: {scan.total_files}\n"
            f".py: {scan.py_files}\n"
            f".md: {scan.md_files}\n"
            f".txt: {scan.txt_files}\n"
            f"README.md: {yes_no(scan.has_readme)}\n"
            f"requirements.txt: {yes_no(scan.has_requirements)}\n"
            f"pyproject.toml: {yes_no(scan.has_pyproject)}\n"
            f"Tamanho total: {size}"
        )

    @staticmethod
    def _format_size(size_bytes: int) -> str:
        """Converte bytes em texto legível (B, KB, MB, GB)."""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        if size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        if size_bytes < 1024 * 1024 * 1024:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
        return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"

    def _create_chat_area(self) -> QWidget:
        """Área central de conversa com campo de entrada na parte inferior."""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        self._chat_display = QTextEdit()
        self._chat_display.setReadOnly(True)
        self._chat_display.setPlaceholderText(
            "O histórico de conversa aparecerá aqui."
        )
        layout.addWidget(self._chat_display, stretch=1)

        self._message_input = QLineEdit()
        self._message_input.setPlaceholderText("Digite sua mensagem...")
        self._message_input.returnPressed.connect(self._send_message)
        layout.addWidget(self._message_input)

        return container

    def _refresh_ollama_models(self) -> None:
        """Verifica o Ollama, atualiza o ComboBox e informa o usuário no chat."""
        if self._is_generating:
            return

        self._model_combo.clear()
        self._model_combo.setEnabled(False)

        available, status_message = self._ollama_client.is_available()
        self._append_system_message(status_message)

        if not available:
            self._model_combo.addItem("Ollama indisponível")
            return

        models, error = self._ollama_client.list_models()
        if error:
            self._append_system_message(error)
            self._model_combo.addItem("Erro ao carregar modelos")
            return

        self._model_combo.addItems(models)
        self._model_combo.setEnabled(True)
        self._append_system_message(
            f"{len(models)} modelo(s) carregado(s): {', '.join(models)}"
        )

    def _append_system_message(self, text: str) -> None:
        """Exibe mensagens de status do Ollama na área de chat."""
        self._chat_display.append(f"[Sistema] {text}")

    def _append_chat(self, speaker: str, text: str) -> None:
        """Adiciona uma mensagem formatada ao histórico visível do chat."""
        self._chat_display.append(f"[{speaker}]\n{text}")

    def _show_generating_message(self) -> None:
        """Exibe o bloco temporário de geração no chat."""
        self._append_chat("CortexForge", "Gerando resposta...")

    def _finalize_generating_message(self, content: str) -> None:
        """Substitui o bloco 'Gerando resposta...' pelo texto final."""
        text = self._chat_display.toPlainText()
        if _PENDING_RESPONSE_BLOCK not in text:
            self._append_chat("CortexForge", content)
            return

        updated = text.rsplit(_PENDING_RESPONSE_BLOCK, 1)[0] + (
            f"[CortexForge]\n{content}"
        )
        self._chat_display.setPlainText(updated)
        cursor = self._chat_display.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self._chat_display.setTextCursor(cursor)

    def _set_generation_ui_busy(self, busy: bool) -> None:
        """Habilita ou desabilita controles durante a geração assíncrona."""
        self._is_generating = busy
        self._message_input.setEnabled(not busy)
        self._open_project_btn.setEnabled(not busy)
        self._refresh_btn.setEnabled(not busy)

    def _send_message(self) -> None:
        """Envia o texto digitado ao Ollama de forma assíncrona."""
        if self._is_generating:
            return

        prompt = self._message_input.text().strip()
        if not prompt:
            return

        model = self._model_combo.currentText().strip()
        invalid_labels = {"Ollama indisponível", "Erro ao carregar modelos"}
        if (
            not self._model_combo.isEnabled()
            or not model
            or model in invalid_labels
        ):
            self._append_chat("CortexForge", "Erro: Selecione um modelo válido.")
            self.statusBar().showMessage("Erro")
            return

        agent_id = self._agent_combo.currentData()
        if not agent_id:
            self._append_chat("CortexForge", "Erro: Selecione um agente válido.")
            self.statusBar().showMessage("Erro")
            return

        system_prompt, agent_error = load_agent_prompt(agent_id)
        if agent_error:
            self._append_chat("CortexForge", f"Erro: {agent_error}")
            self.statusBar().showMessage("Erro")
            return

        full_prompt = build_prompt(system_prompt, prompt)

        self._append_chat("Você", prompt)
        self._message_input.clear()
        self._show_generating_message()

        self._set_generation_ui_busy(True)
        self.statusBar().showMessage("Gerando resposta...")

        worker = OllamaGenerateWorker(model, full_prompt, self)
        worker.finished.connect(self._on_generate_finished)
        worker.finished.connect(worker.deleteLater)
        self._generate_worker = worker
        worker.start()

    def _on_generate_finished(
        self, response: object, error: object
    ) -> None:
        """Atualiza o chat e a barra de status quando a thread termina."""
        self._generate_worker = None

        if error:
            self._finalize_generating_message(f"Erro: {error}")
            self.statusBar().showMessage("Erro")
        else:
            self._finalize_generating_message(str(response or ""))
            self.statusBar().showMessage("Pronto")

        self._set_generation_ui_busy(False)
        self._message_input.setFocus()
