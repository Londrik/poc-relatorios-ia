from typing import Optional, Literal
from pydantic import BaseModel, Field

class DispatchParameters(BaseModel):
    tipo_documento: Optional[Literal["CPF", "CNPJ"]] = Field(None, description="Tipo do documento identificado")
    documento_mascarado: Optional[str] = Field(None, description="Número do documento mascarado")
    tipo_relatorio: Optional[Literal["completo", "simplificado"]] = Field("completo", description="Escopo do relatório solicitado")
    parametro_faltante: Optional[str] = Field(None, description="Indicação de parâmetro ausente se aplicável")
    mensagem_orientacao: Optional[str] = Field(None, description="Mensagem de orientação ao usuário")

class DispatchRequest(BaseModel):
    sanitized_text: str = Field(..., description="Texto higienizado proveniente do sanitizador")

class DispatchResponse(BaseModel):
    action: Literal["consultar_relatorio", "solicitar_parametros"] = Field(..., description="Ação decidida pelo agente")
    parameters: DispatchParameters = Field(..., description="Parâmetros extraídos para a ação")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Grau de confiança da decisão")
    is_fallback: bool = Field(False, description="Indica se a resposta foi gerada pelo fallback heurístico local")
