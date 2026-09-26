from fastapi import APIRouter, status
from app.schemas.chat import ChatMessageRequest, ChatMessageResponse
from app.services.chat_orchestrator import ChatOrchestrator

router = APIRouter(prefix="/chat", tags=["Atendimento Chat"])

@router.post("/message", response_model=ChatMessageResponse, status_code=status.HTTP_200_OK)
async def process_chat_message(payload: ChatMessageRequest):
    """Endpoint principal de atendimento integrando Sanitização, Dispatcher, DB e PDF"""
    return await ChatOrchestrator.process_message(payload)
