"""
Cliente para comunicação com o Ollama local.

Utiliza a API HTTP em http://localhost:11434 (tags e generate).
"""

from __future__ import annotations

from typing import Any

import requests

# Timeout curto para não travar a interface ao verificar disponibilidade.
_DEFAULT_TIMEOUT = 5


class OllamaClient:
    """Encapsula chamadas ao servidor Ollama local."""

    def __init__(self, base_url: str = "http://localhost:11434") -> None:
        """
        Args:
            base_url: URL base do servidor Ollama (padrão local).
        """
        self.base_url = base_url.rstrip("/")
        # Modelo usado por generate(); a UI definirá na versão do chat.
        self.model: str | None = None

    def is_available(self) -> tuple[bool, str]:
        """
        Verifica se o Ollama responde na URL configurada.

        Returns:
            Tupla (disponível, mensagem). A mensagem descreve sucesso ou erro amigável.
        """
        try:
            response = requests.get(
                f"{self.base_url}/api/tags",
                timeout=_DEFAULT_TIMEOUT,
            )
            if response.status_code == 200:
                return True, "Ollama está disponível."
            return (
                False,
                f"Ollama respondeu com status {response.status_code}. "
                "Tente reiniciar o serviço.",
            )
        except requests.exceptions.ConnectionError:
            return (
                False,
                "Não foi possível conectar ao Ollama. "
                f"Verifique se o serviço está em execução em {self.base_url}.",
            )
        except requests.exceptions.Timeout:
            return (
                False,
                "O tempo de conexão com o Ollama esgotou. "
                "O servidor pode estar sobrecarregado ou indisponível.",
            )
        except requests.exceptions.RequestException as exc:
            return False, f"Erro ao comunicar com o Ollama: {exc}"

    def list_models(self) -> tuple[list[str], str | None]:
        """
        Lista os nomes dos modelos instalados no Ollama.

        Returns:
            Tupla (lista de nomes, mensagem de erro). Em sucesso, o erro é None.
        """
        available, message = self.is_available()
        if not available:
            return [], message

        try:
            response = requests.get(
                f"{self.base_url}/api/tags",
                timeout=_DEFAULT_TIMEOUT,
            )
            response.raise_for_status()
            payload: dict[str, Any] = response.json()
            models = [
                item["name"]
                for item in payload.get("models", [])
                if isinstance(item, dict) and "name" in item
            ]
            if not models:
                return [], "Nenhum modelo instalado. Use 'ollama pull <modelo>'."
            return models, None
        except requests.exceptions.HTTPError:
            return [], "Não foi possível obter a lista de modelos do Ollama."
        except requests.exceptions.RequestException as exc:
            return [], f"Erro ao listar modelos: {exc}"
        except (KeyError, TypeError, ValueError):
            return [], "Resposta inesperada do Ollama ao listar modelos."

    def generate(self, prompt: str) -> tuple[str | None, str | None]:
        """
        Gera texto a partir de um prompt (API /api/generate).

        Ainda não utilizado pela interface na v0.2; preparado para versões futuras.
        Usa o atributo ``model`` do cliente (nome do modelo no Ollama).

        Args:
            prompt: Texto enviado ao modelo.

        Returns:
            Tupla (texto gerado, mensagem de erro). Em sucesso, o erro é None.
        """
        if not prompt.strip():
            return None, "O prompt não pode estar vazio."

        if not self.model or not self.model.strip():
            return None, "Selecione um modelo antes de gerar."

        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                },
                timeout=120,
            )
            response.raise_for_status()
            data: dict[str, Any] = response.json()
            text = data.get("response")
            if text is None:
                return None, "O Ollama não retornou texto na resposta."
            return str(text), None
        except requests.exceptions.ConnectionError:
            return (
                None,
                "Conexão perdida com o Ollama. Verifique se o serviço ainda está ativo.",
            )
        except requests.exceptions.Timeout:
            return None, "A geração demorou demais e foi cancelada por tempo limite."
        except requests.exceptions.HTTPError as exc:
            status = exc.response.status_code if exc.response is not None else "?"
            return None, f"O Ollama recusou a requisição (HTTP {status})."
        except requests.exceptions.RequestException as exc:
            return None, f"Erro ao gerar resposta: {exc}"
        except (KeyError, TypeError, ValueError):
            return None, "Resposta inesperada do Ollama ao gerar texto."
