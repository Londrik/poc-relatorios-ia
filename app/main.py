from fastapi import FastAPI
from app.api.v1.endpoints.sanitizer import router as sanitizer_router

app = FastAPI(
    title="PoC Relatórios IA - LGPD & OWASP Guardrail API",
    version="1.0.0",
    description="Camada de entrada segura para sanitização de PII e proteção de pipelines GenAI."
)

app.include_router(sanitizer_router, prefix="/api/v1")

@app.get("/health", tags=["Infraestrutura"])
async def health_check():
    return {"status": "ok", "service": "poc-relatorios-ia"}
