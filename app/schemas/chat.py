from typing import Optional, List
from pydantic import BaseModel, Field

class ChatMessageRequest(BaseModel):
    message: str = Field(..., description="Mensagem bruta enviada pelo utilizador na interface de chat")

class ChatMessageResponse(BaseModel):
    is_safe: bool = Field(..., description="Indica se a mensagem passou pelo filtro de segurança")
    sanitized_text: str = Field(..., description="Texto processado com PII mascarada")
    action_taken: str = Field(..., description="Ação executada pelo orquestrador (consultar_relatorio | solicitar_parametros | bloqueado)")
    response_text: str = Field(..., description="Resposta formatada final para exibição no chat")
    pdf_file_path: Optional[str] = Field(None, description="Caminho do PDF gerado caso o relatório tenha sido emitido")
    pii_detected: List[str] = Field(default_factory=list, description="PIIs identificadas no processo")
    is_fallback: bool = Field(False, description="Indica se alguma etapa rodou via fallback determinístico local")
