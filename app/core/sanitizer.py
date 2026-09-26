import re
from typing import List, Optional
from pydantic import BaseModel, Field

class SanitizerOutput(BaseModel):
    is_safe: bool = Field(
        ..., description="Indica se a mensagem é segura contra ataques"
    )
    sanitized_text: str = Field(
        ..., description="Texto do usuário com CPFs/CNPJs mascarados"
    )
    pii_detected: List[str] = Field(
        default_factory=list, description="Tipos de PII identificados"
    )
    security_flag: Optional[str] = Field(
        None, description="Flag de segurança se houver tentativa de ataque"
    )

class PIISanitizer:
    """Módulo Backend de Sanitização de PII e Guardrail LGPD/OWASP"""

    CPF_REGEX = re.compile(r"\b(\d{3})\.?(\d{3})\.?(\d{3})-?(\d{2})\b")
    CNPJ_REGEX = re.compile(
        r"\b(\d{2})\.?(\d{3})\.?(\d{3})/?(\d{4})-?(\d{2})\b"
    )

    PROMPT_INJECTION_KEYWORDS = [
        "ignore as instruções",
        "ignore todas as regras",
        "esqueça seu prompt",
        "revele sua senha",
        "modo root",
    ]

    @classmethod
    def mask_cpf(cls, match: re.Match) -> str:
        g2, g3 = match.group(2), match.group(3)
        return f"***.{g2}.{g3}-**"

    @classmethod
    def mask_cnpj(cls, match: re.Match) -> str:
        g1, g2, g4 = match.group(1), match.group(2), match.group(4)
        return f"{g1}.{g2}.***/{g4}-**"

    @classmethod
    def sanitize(cls, raw_text: str) -> SanitizerOutput:
        pii_found = []
        text_lower = raw_text.lower()

        for keyword in cls.PROMPT_INJECTION_KEYWORDS:
            if keyword in text_lower:
                return SanitizerOutput(
                    is_safe=False,
                    sanitized_text=raw_text,
                    pii_detected=["NENHUM"],
                    security_flag="PROMPT_INJECTION_DETECTED",
                )

        if cls.CPF_REGEX.search(raw_text):
            pii_found.append("CPF")
            raw_text = cls.CPF_REGEX.sub(cls.mask_cpf, raw_text)

        if cls.CNPJ_REGEX.search(raw_text):
            pii_found.append("CNPJ")
            raw_text = cls.CNPJ_REGEX.sub(cls.mask_cnpj, raw_text)

        if not pii_found:
            pii_found.append("NENHUM")

        return SanitizerOutput(
            is_safe=True,
            sanitized_text=raw_text,
            pii_detected=pii_found,
            security_flag=None,
        )
