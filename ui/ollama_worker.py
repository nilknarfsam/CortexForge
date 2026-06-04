"""
Worker em QThread para geração de respostas do Ollama sem bloquear a UI.
"""

from PySide6.QtCore import QThread, Signal

from core.ollama_client import OllamaClient, OllamaGenerationError


class OllamaGenerateWorker(QThread):
    """Executa OllamaClient.generate(stream=True) e emite tokens progressivamente."""

    token_received = Signal(str)
    generation_finished = Signal()
    generation_error = Signal(str)

    def __init__(self, model: str, full_prompt: str, parent=None) -> None:
        super().__init__(parent)
        self._model = model
        self._full_prompt = full_prompt

    def run(self) -> None:
        """Consome o stream da API e repassa cada token à thread principal."""
        client = OllamaClient()
        client.model = self._model
        try:
            stream = client.generate(self._full_prompt, stream=True)
            for token in stream:
                self.token_received.emit(token)
            self.generation_finished.emit()
        except OllamaGenerationError as exc:
            self.generation_error.emit(str(exc))
        except Exception as exc:
            self.generation_error.emit(f"Erro inesperado: {exc}")
