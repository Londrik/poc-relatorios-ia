import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.schemas.dispatcher import DispatchRequest
from app.services.dispatcher_service import DispatcherService

@pytest.mark.asyncio
async def test_fallback_cpf_extraction():
    req = DispatchRequest(sanitized_text="Gere o relatório do CPF ***.456.789-** por favor.")
    res = DispatcherService._local_fallback(req.sanitized_text)
    assert res.action == "consultar_relatorio"
    assert res.parameters.tipo_documento == "CPF"
    assert res.parameters.documento_mascarado == "***.456.789-**"

@pytest.mark.asyncio
async def test_fallback_cnpj_extraction():
    req = DispatchRequest(sanitized_text="Consulta para o CNPJ 12.345.***/0001-**.")
    res = DispatcherService._local_fallback(req.sanitized_text)
    assert res.action == "consultar_relatorio"
    assert res.parameters.tipo_documento == "CNPJ"
    assert res.parameters.documento_mascarado == "12.345.***/0001-**"

@pytest.mark.asyncio
async def test_fallback_missing_parameter():
    req = DispatchRequest(sanitized_text="Quero um relatório de vendas.")
    res = DispatcherService._local_fallback(req.sanitized_text)
    assert res.action == "solicitar_parametros"
    assert res.parameters.parametro_faltante == "CPF_OU_CNPJ"

@pytest.mark.asyncio
async def test_endpoint_dispatch_success():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        payload = {"sanitized_text": "Gere o relatório do CPF ***.456.789-** por favor."}
        response = await ac.post("/api/v1/dispatch", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["action"] == "consultar_relatorio"
        assert data["parameters"]["tipo_documento"] == "CPF"
