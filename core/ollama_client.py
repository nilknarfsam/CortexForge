"""
Cliente para comunicação com o Ollama local.

Utiliza a API HTTP em http://localhost:11434 (tags e generate).
"""

from __future__ import annotations

import json
from collections.abc import Iterator
from typing import Any

import requests

# Timeout curto para não travar a interface ao verificar disponibilidade.
_DEFAULT_TIMEOUT = 5
_GENERATE_TIMEOUT = 120


class OllamaGenerationError(Exception):
    """Erro durante geração (HTTP ou resposta inválida)."""


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

    def debug_generate_payload(
        self,
        prompt: str,
        model: str | None = None,
        *,
        stream: bool = False,
    ) -> dict[str, Any]:
        """
        Retorna exatamente o JSON enviado ao endpoint /api/generate.

        Args:
            prompt: Texto do prompt.
            model: Modelo Ollama; usa ``self.model`` se omitido.
            stream: Se True, corresponde ao modo streaming do Ollama.
        """
        resolved_model = model if model is not None else self.model
        return {
            "model": resolved_model or "",
            "prompt": prompt,
            "stream": stream,
        }

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

    def generate(
        self, prompt: str, stream: bool = False
    ) -> tuple[str | None, str | None] | Iterator[str]:
        """
        Gera texto a partir de um prompt (API /api/generate).

        Args:
            prompt: Texto enviado ao modelo.
            stream: Se True, retorna um iterador de tokens; se False, resposta completa.

        Returns:
            Com stream=False: tupla (texto, erro).
            Com stream=True: iterador de fragmentos de texto.
        """
        self._validate_generate_request(prompt)
        if stream:
            return self._generate_stream(prompt)
        return self._generate_blocking(prompt)

    def _validate_generate_request(self, prompt: str) -> None:
        """Valida prompt e modelo antes de chamar a API."""
        if not prompt.strip():
            raise OllamaGenerationError("O prompt não pode estar vazio.")
        if not self.model or not self.model.strip():
            raise OllamaGenerationError("Selecione um modelo antes de gerar.")

    def _generate_blocking(self, prompt: str) -> tuple[str | None, str | None]:
        """Geração sem streaming (resposta única)."""
        payload = self.debug_generate_payload(prompt, stream=False)

        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=_GENERATE_TIMEOUT,
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
            return None, self._http_error_message(exc, prompt)
        except requests.exceptions.RequestException as exc:
            return None, f"Erro ao gerar resposta: {exc}"
        except (KeyError, TypeError, ValueError):
            return None, "Resposta inesperada do Ollama ao gerar texto."

    def _generate_stream(self, prompt: str) -> Iterator[str]:
        """Geração com streaming (um yield por token/chunk da API)."""
        payload = self.debug_generate_payload(prompt, stream=True)

        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                stream=True,
                timeout=_GENERATE_TIMEOUT,
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as exc:
            message = self._http_error_message(exc, prompt)
            raise OllamaGenerationError(message) from exc
        except requests.exceptions.ConnectionError as exc:
            raise OllamaGenerationError(
                "Conexão perdida com o Ollama. Verifique se o serviço ainda está ativo."
            ) from exc
        except requests.exceptions.Timeout as exc:
            raise OllamaGenerationError(
                "A geração demorou demais e foi cancelada por tempo limite."
            ) from exc
        except requests.exceptions.RequestException as exc:
            raise OllamaGenerationError(f"Erro ao gerar resposta: {exc}") from exc

        for line in response.iter_lines(decode_unicode=True):
            if not line:
                continue
            try:
                data: dict[str, Any] = json.loads(line)
            except json.JSONDecodeError:
                continue

            chunk = data.get("response")
            if chunk:
                yield str(chunk)

            if data.get("done"):
                break

    def _http_error_message(
        self, exc: requests.exceptions.HTTPError, prompt: str
    ) -> str:
        """Monta mensagem amigável e registra diagnóstico no terminal."""
        http_response = exc.response
        status_code = http_response.status_code if http_response is not None else 0
        body = (http_response.text if http_response is not None else "") or ""
        self._log_http_error(status_code, body)
        self._log_generate_context(prompt, self.model)
        return f"Erro HTTP {status_code}"

    @staticmethod
    def _log_http_error(status_code: int, body: str) -> None:
        """Registra status e corpo da resposta HTTP no terminal."""
        print(f"STATUS\n{status_code}")
        print(f"BODY\n{body}")

    @staticmethod
    def _log_generate_context(prompt: str, model: str | None) -> None:
        """Registra modelo e trecho do prompt no terminal para diagnóstico."""
        print(f"Modelo utilizado: {model or '(não definido)'}")
        print(f"Tamanho do prompt: {len(prompt)} caracteres")
        preview = prompt[:500]
        print(f"Primeiros 500 caracteres do prompt:\n{preview}")
