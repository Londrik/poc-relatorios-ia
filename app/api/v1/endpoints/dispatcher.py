from fastapi import APIRouter, status
from app.schemas.dispatcher import DispatchRequest, DispatchResponse
from app.services.dispatcher_service import DispatcherService

router = APIRouter(prefix="", tags=["Orquestrador & Dispatcher"])

@router.post("/dispatch", response_model=DispatchResponse, status_code=status.HTTP_200_OK)
async def dispatch_intent(payload: DispatchRequest):
    """Endpoint para interpretação de intenção e Function Calling"""
    return await DispatcherService.dispatch(payload)
