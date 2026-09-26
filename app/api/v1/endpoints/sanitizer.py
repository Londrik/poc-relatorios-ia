from fastapi import APIRouter, status
from app.schemas.sanitizer import SanitizeRequest, SanitizeResponse
from app.core.sanitizer import PIISanitizer

router = APIRouter(prefix="/sanitize", tags=["Sanitização & Guardrail"])

@router.post(
    "",
    response_model=SanitizeResponse,
    status_code=status.HTTP_200_OK,
    summary="Sanitizar PII e validar Prompt Injection",
    description="Analisa a entrada de texto, mascara dados sensíveis conforme LGPD e valida regras OWASP GenAI."
)
async def sanitize_input(payload: SanitizeRequest) -> SanitizeResponse:
    result = PIISanitizer.sanitize(payload.text)
    return SanitizeResponse(
        is_safe=result.is_safe,
        sanitized_text=result.sanitized_text,
        pii_detected=result.pii_detected,
        security_flag=result.security_flag
    )
