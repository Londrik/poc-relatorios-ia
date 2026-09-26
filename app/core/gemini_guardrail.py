import json
from google import genai
from google.genai import types
from app.core.config import settings
from app.core.prompts import SYSTEM_GUARDRAIL_PROMPT
from app.core.sanitizer import PIISanitizer, SanitizerOutput

class GeminiGuardrailService:
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)

    async def analyze_and_sanitize(self, text: str) -> SanitizerOutput:
        # Camada 1: Validação determinística rápida (regex/palavras proibidas)
        local_check = PIISanitizer.sanitize(text)
        if not local_check.is_safe:
            return local_check

        # Camada 2: Validação contextual via Gemini com structured output
        try:
            response = self.client.models.generate_content(
                model=settings.MODEL_NAME,
                contents=text,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_GUARDRAIL_PROMPT,
                    response_mime_type="application/json",
                    temperature=0.0,
                ),
            )
            data = json.loads(response.text)
            return SanitizerOutput(
                is_safe=data.get("is_safe", False),
                sanitized_text=data.get("sanitized_text", local_check.sanitized_text),
                pii_detected=data.get("pii_detected", local_check.pii_detected),
                security_flag=data.get("security_flag")
            )
        except Exception:
            # Fallback seguro para o sanitizador local caso a chamada ao LLM oscile
            return local_check
