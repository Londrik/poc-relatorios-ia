from typing import List, Optional
from pydantic import BaseModel, Field

class SanitizeRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        description="Texto bruto fornecido pelo usuário a ser sanitizado",
        examples=["Gere o relatório para o CPF 123.456.789-00 por favor."]
    )

class SanitizeResponse(BaseModel):
    is_safe: bool = Field(
        ...,
        description="Indica se a entrada passou pelas regras OWASP de segurança"
    )
    sanitized_text: str = Field(
        ...,
        description="Texto resultante com CPFs/CNPJs devidamente mascarados"
    )
    pii_detected: List[str] = Field(
        default_factory=list,
        description="Lista de tipos de PII identificados na análise"
    )
    security_flag: Optional[str] = Field(
        None,
        description="Identificador de ameaça quando detectada (ex: PROMPT_INJECTION_DETECTED)"
    )
