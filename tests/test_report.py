import pytest
from pathlib import Path
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.schemas.report import ReportQueryRequest
from app.services.mock_db_service import MockDBService
from app.services.pdf_service import PDFService

def test_mock_db_query_cpf_success():
    req = ReportQueryRequest(tipo_documento="CPF", documento_mascarado="***.456.789-**")
    res = MockDBService.query_record(req)
    assert res.found is True
    assert res.dados["nome_titular"] == "JOAO DA SILVA SOUZA"

def test_mock_db_query_not_found():
    req = ReportQueryRequest(tipo_documento="CPF", documento_mascarado="***.000.000-**")
    res = MockDBService.query_record(req)
    assert res.found is False
    assert res.dados is None

def test_pdf_generation_file_creation():
    req = ReportQueryRequest(tipo_documento="CPF", documento_mascarado="***.456.789-**")
    report_data = MockDBService.query_record(req)
    pdf_res = PDFService.generate_pdf(report_data)

    assert pdf_res.success is True
    assert pdf_res.file_size_bytes > 0
    assert Path(pdf_res.file_path).exists()

@pytest.mark.asyncio
async def test_endpoint_report_generate_success():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        payload = {
            "tipo_documento": "CPF",
            "documento_mascarado": "***.456.789-**",
            "tipo_relatorio": "completo"
        }
        response = await ac.post("/api/v1/report/generate", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["file_size_bytes"] > 0
