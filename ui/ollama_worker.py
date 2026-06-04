"""
Worker em QThread para geração de respostas do Ollama sem bloquear a UI.
"""

from PySide6.QtCore import QThread, Signal

from core.ollama_client import OllamaClient


class OllamaGenerateWorker(QThread):
    """Executa OllamaClient.generate() em thread separada."""

    finished = Signal(object, object)  # response: str | None, error: str | None

    def __init__(self, model: str, full_prompt: str, parent=None) -> None:
        super().__init__(parent)
        self._model = model
        self._full_prompt = full_prompt

    def run(self) -> None:
        """Chama a API do Ollama e emite o resultado via sinal."""
        client = OllamaClient()
        client.model = self._model
        response, error = client.generate(self._full_prompt)
        self.finished.emit(response, error)
