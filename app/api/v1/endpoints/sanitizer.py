from fastapi import APIRouter, Depends, status
from app.schemas.sanitizer import SanitizeRequest, SanitizeResponse
from app.core.gemini_guardrail import GeminiGuardrailService

router = APIRouter(prefix="/sanitize", tags=["Sanitização & Guardrail"])

def get_guardrail_service() -> GeminiGuardrailService:
    return GeminiGuardrailService()

@router.post(
    "",
    response_model=SanitizeResponse,
    status_code=status.HTTP_200_OK,
    summary="Sanitizar PII e validar Prompt Injection",
    description="Analisa entrada via regex local e validação contextual com LLM."
)
async def sanitize_input(
    payload: SanitizeRequest,
    service: GeminiGuardrailService = Depends(get_guardrail_service)
) -> SanitizeResponse:
    result = await service.analyze_and_sanitize(payload.text)
    return SanitizeResponse(
        is_safe=result.is_safe,
        sanitized_text=result.sanitized_text,
        pii_detected=result.pii_detected,
        security_flag=result.security_flag
    )
