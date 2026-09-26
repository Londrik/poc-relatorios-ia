from app.schemas.chat import ChatMessageRequest, ChatMessageResponse
from app.core.sanitizer import PIISanitizer
from app.services.dispatcher_service import DispatcherService
from app.schemas.dispatcher import DispatchRequest
from app.services.mock_db_service import MockDBService
from app.schemas.report import ReportQueryRequest
from app.services.pdf_service import PDFService

class ChatOrchestrator:
    """Orquestrador do Pipeline de Atendimento (Tarefas 1, 2, 3 e 4)"""

    @classmethod
    async def process_message(cls, request: ChatMessageRequest) -> ChatMessageResponse:
        # 1. Sanitização e Guardrail de PII (Tarefa 1)
        sanitized_res = PIISanitizer.sanitize(request.message)
        if not sanitized_res.is_safe:
            return ChatMessageResponse(
                is_safe=False,
                sanitized_text=request.message,
                action_taken="bloqueado",
                response_text="Sua solicitação foi bloqueada pelos nossos sistemas de segurança devido a conteúdo suspeito.",
                pdf_file_path=None,
                pii_detected=sanitized_res.pii_detected,
                is_fallback=True
            )

        # 2. Orquestração e Function Calling (Tarefa 2)
        dispatch_req = DispatchRequest(sanitized_text=sanitized_res.sanitized_text)
        dispatch_res = await DispatcherService.dispatch(dispatch_req)

        # Trata cenário onde faltam parâmetros
        if dispatch_res.action == "solicitar_parametros":
            orientacao = dispatch_res.parameters.mensagem_orientacao or "Por favor, informe um CPF ou CNPJ válido para consulta."
            return ChatMessageResponse(
                is_safe=True,
                sanitized_text=sanitized_res.sanitized_text,
                action_taken="solicitar_parametros",
                response_text=f"Olá! {orientacao}",
                pdf_file_path=None,
                pii_detected=sanitized_res.pii_detected,
                is_fallback=dispatch_res.is_fallback
            )

        # 3. Consulta à Base de Dados Mockada e Produção do PDF (Tarefa 3)
        doc_tipo = dispatch_res.parameters.tipo_documento or "CPF"
        doc_mascarado = dispatch_res.parameters.documento_mascarado or ""

        report_req = ReportQueryRequest(
            tipo_documento=doc_tipo,
            documento_mascarado=doc_mascarado,
            tipo_relatorio=dispatch_res.parameters.tipo_relatorio or "completo"
        )
        report_data = MockDBService.query_record(report_req)

        if not report_data.found:
            return ChatMessageResponse(
                is_safe=True,
                sanitized_text=sanitized_res.sanitized_text,
                action_taken="consultar_relatorio",
                response_text=f"Não foram localizados registros cadastrais para o documento *{doc_mascarado}* em nossa base corporativa.",
                pdf_file_path=None,
                pii_detected=sanitized_res.pii_detected,
                is_fallback=dispatch_res.is_fallback
            )

        # Gerar o PDF
        pdf_res = PDFService.generate_pdf(report_data)

        # 4. Formatação no estilo WhatsApp Corporativo (Tarefa 4)
        msg_final = (
            f"Olá! Seu *Relatório de Compliance* foi gerado com sucesso para o documento *{doc_mascarado}*.\n\n"
            f"*Resumo da Consulta:*\n"
            f"- Tipo: {doc_tipo}\n"
            f"- Documento: {doc_mascarado}\n"
            f"- Status do PDF: Prontamente Gerado\n\n"
            f"Você pode realizar o download do arquivo PDF através do botão abaixo na tela.\n\n"
            f"_Aviso de Segurança (LGPD): Por medidas de privacidade, este documento temporário será mantido por 15 minutos._"
        )

        return ChatMessageResponse(
            is_safe=True,
            sanitized_text=sanitized_res.sanitized_text,
            action_taken="consultar_relatorio",
            response_text=msg_final,
            pdf_file_path=pdf_res.file_path,
            pii_detected=sanitized_res.pii_detected,
            is_fallback=dispatch_res.is_fallback
        )
