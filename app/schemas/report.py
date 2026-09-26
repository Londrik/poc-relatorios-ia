from typing import Optional, Dict, Any, Literal
from pydantic import BaseModel, Field

class ReportQueryRequest(BaseModel):
    tipo_documento: Literal["CPF", "CNPJ"] = Field(..., description="Tipo do documento a consultar")
    documento_mascarado: str = Field(..., description="Número do documento mascarado vindo do Dispatcher")
    tipo_relatorio: Literal["completo", "simplificado"] = Field("completo", description="Escopo do relatório")

class ReportDataResponse(BaseModel):
    found: bool = Field(..., description="Indica se o registro foi localizado no banco mockado")
    tipo_documento: str = Field(..., description="Tipo de documento consultado")
    documento_mascarado: str = Field(..., description="Documento consultado")
    dados: Optional[Dict[str, Any]] = Field(None, description="Campos do relatório localizados")

class PDFGenerationResponse(BaseModel):
    success: bool = Field(..., description="Status do processo de geração do PDF")
    file_path: str = Field(..., description="Caminho do arquivo PDF gerado no disco/scratch")
    documento_mascarado: str = Field(..., description="Documento do relatório")
    file_size_bytes: int = Field(..., description="Tamanho do arquivo gerado em bytes")
