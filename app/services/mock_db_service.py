import json
from pathlib import Path
from typing import Dict, Any
from app.schemas.report import ReportQueryRequest, ReportDataResponse

class MockDBService:
    """Serviço de Consulta ao Banco de Dados Mockado"""

    DB_PATH = Path("app/database/mock_db.json")

    @classmethod
    def _load_db(cls) -> Dict[str, Any]:
        if not cls.DB_PATH.exists():
            return {"cpfs": {}, "cnpjs": {}}
        with open(cls.DB_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    @classmethod
    def query_record(cls, request: ReportQueryRequest) -> ReportDataResponse:
        db = cls._load_db()
        key = "cpfs" if request.tipo_documento == "CPF" else "cnpjs"
        records = db.get(key, {})

        record_data = records.get(request.documento_mascarado)

        if record_data:
            return ReportDataResponse(
                found=True,
                tipo_documento=request.tipo_documento,
                documento_mascarado=request.documento_mascarado,
                dados=record_data
            )

        return ReportDataResponse(
            found=False,
            tipo_documento=request.tipo_documento,
            documento_mascarado=request.documento_mascarado,
            dados=None
        )
