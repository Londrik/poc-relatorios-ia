from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from app.schemas.report import ReportQueryRequest, PDFGenerationResponse
from app.services.mock_db_service import MockDBService
from app.services.pdf_service import PDFService

router = APIRouter(prefix="/report", tags=["Relatórios & PDF"])

class AdminListRequest(BaseModel):
    password: str

@router.post("/generate", response_model=PDFGenerationResponse, status_code=status.HTTP_200_OK)
async def generate_report_pdf(payload: ReportQueryRequest):
    """Endpoint para busca no banco mockado e geração do PDF do relatório"""
    report_data = MockDBService.query_record(payload)
    if not report_data.found:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Registro para o documento {payload.documento_mascarado} não foi encontrado na base."
        )
    return PDFService.generate_pdf(report_data)

@router.post("/admin/list-all", status_code=status.HTTP_200_OK)
async def admin_list_all(payload: AdminListRequest) -> Dict[str, Any]:
    """Endpoint administrativo para listar todos os registros mediante senha"""
    try:
        return MockDBService.list_all_records(payload.password)
    except PermissionError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Senha administrativa inválida."
        )
