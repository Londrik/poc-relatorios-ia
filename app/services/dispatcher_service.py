import json
import re
from google import genai
from google.genai import types
from app.core.config import settings
from app.core.dispatcher_prompt import DISPATCHER_SYSTEM_PROMPT
from app.schemas.dispatcher import DispatchRequest, DispatchResponse, DispatchParameters

class DispatcherService:
    """Serviço de Orquestração e Function Calling com Fallback Local"""

    CPF_MASKED_REGEX = re.compile(r"\*\*\*\.\d{3}\.\d{3}-\*\*")
    CNPJ_MASKED_REGEX = re.compile(r"\d{2}\.\d{3}\.\*\*\*/\d{4}-\*\*")

    @classmethod
    def _local_fallback(cls, text: str) -> DispatchResponse:
        """Fallback determinístico usando Regex se a API de LLM falhar ou não estiver disponível"""
        cpf_match = cls.CPF_MASKED_REGEX.search(text)
        cnpj_match = cls.CNPJ_MASKED_REGEX.search(text)

        if cpf_match:
            return DispatchResponse(
                action="consultar_relatorio",
                parameters=DispatchParameters(
                    tipo_documento="CPF",
                    documento_mascarado=cpf_match.group(0),
                    tipo_relatorio="completo"
                ),
                confidence_score=1.0,
                is_fallback=True
            )

        if cnpj_match:
            return DispatchResponse(
                action="consultar_relatorio",
                parameters=DispatchParameters(
                    tipo_documento="CNPJ",
                    documento_mascarado=cnpj_match.group(0),
                    tipo_relatorio="completo"
                ),
                confidence_score=1.0,
                is_fallback=True
            )

        return DispatchResponse(
            action="solicitar_parametros",
            parameters=DispatchParameters(
                parametro_faltante="CPF_OU_CNPJ",
                mensagem_orientacao="Por favor, informe o CPF ou CNPJ que deseja consultar."
            ),
            confidence_score=1.0,
            is_fallback=True
        )

    @classmethod
    async def dispatch(cls, request: DispatchRequest) -> DispatchResponse:
        """Processa a intenção via Gemini 2.5 Flash com resposta estruturada JSON"""
        if not settings.GEMINI_API_KEY or settings.GEMINI_API_KEY == "sua_chave_de_api_aqui":
            return cls._local_fallback(request.sanitized_text)

        try:
            client = genai.Client(api_key=settings.GEMINI_API_KEY)
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=request.sanitized_text,
                config=types.GenerateContentConfig(
                    system_instruction=DISPATCHER_SYSTEM_PROMPT,
                    response_mime_type="application/json",
                    temperature=0.0
                )
            )
            data = json.loads(response.text)
            return DispatchResponse(
                action=data["action"],
                parameters=DispatchParameters(**data["parameters"]),
                confidence_score=float(data.get("confidence_score", 0.95)),
                is_fallback=False
            )
        except Exception:
            return cls._local_fallback(request.sanitized_text)
