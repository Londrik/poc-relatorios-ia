import os
from pathlib import Path
from fpdf import FPDF
from app.schemas.report import ReportDataResponse, PDFGenerationResponse

class PDFReportGenerator(FPDF):
    """Classe customizada FPDF2 para Relatórios Corporativos"""

    def header(self):
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 10, "RELATORIO DE COMPLIANCE E CONSULTA SENSIVEL", border=False, new_x="LMARGIN", new_y="NEXT", align="C")
        self.set_font("Helvetica", "I", 9)
        self.cell(0, 5, "CONFIDENCIAL - USO INTERNO RESTRITO (CONFORMIDADE LGPD)", border=False, new_x="LMARGIN", new_y="NEXT", align="C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 10, f"Pagina {self.page_no()}/{{nb}} - Documento gerado via AI Engine. Link temporario.", align="C")

class PDFService:
    """Serviço de Compilação e Geração do PDF"""

    OUTPUT_DIR = Path("/tmp/reports")

    @classmethod
    def generate_pdf(cls, report_data: ReportDataResponse) -> PDFGenerationResponse:
        cls.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        filename = f"relatorio_{report_data.tipo_documento.lower()}_{report_data.documento_mascarado.replace('*', 'X').replace('.', '_').replace('/', '_').replace('-', '_')}.pdf"
        file_path = cls.OUTPUT_DIR / filename

        pdf = PDFReportGenerator()
        pdf.alias_nb_pages()
        pdf.add_page()
        pdf.set_font("Helvetica", size=10)

        # Seção do Documento
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(0, 8, f"Documento Consultado: {report_data.documento_mascarado} ({report_data.tipo_documento})", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(3)

        if not report_data.found or not report_data.dados:
            pdf.set_font("Helvetica", "", 10)
            pdf.cell(0, 8, "REGISTRO NAO LOCALIZADO NA BASE DE DADOS CORPORATIVA.", new_x="LMARGIN", new_y="NEXT")
        else:
            pdf.set_font("Helvetica", "B", 10)
            pdf.cell(0, 7, "Detalhamento das Informacoes Retornadas:", new_x="LMARGIN", new_y="NEXT")
            pdf.set_font("Helvetica", "", 10)

            for chave, valor in report_data.dados.items():
                chave_fmt = chave.replace("_", " ").title()
                pdf.cell(60, 7, f"{chave_fmt}:", border=1)
                pdf.cell(120, 7, f"{valor}", border=1, new_x="LMARGIN", new_y="NEXT")

        pdf.ln(10)
        pdf.set_font("Helvetica", "I", 8)
        pdf.multi_cell(0, 5, "Aviso Legal: As informacoes constantes neste documento foram processadas de forma segura com mascaramento de PII em conformidade com a Lei Geral de Protecao de Dados (Lei nº 13.709/2018).")

        pdf.output(str(file_path))
        file_size = os.path.getsize(file_path)

        return PDFGenerationResponse(
            success=True,
            file_path=str(file_path),
            documento_mascarado=report_data.documento_mascarado,
            file_size_bytes=file_size
        )
