import os
import streamlit as st
import asyncio
from app.schemas.chat import ChatMessageRequest
from app.services.chat_orchestrator import ChatOrchestrator
from app.services.mock_db_service import MockDBService

st.set_page_config(page_title="POC Relatórios IA - WhatsApp Demo", page_icon="💬", layout="centered")

st.title("💬 Bot de Relatórios Corporativos")
st.caption("Demonstração Executiva: Clean Architecture, Sanitização LGPD e Function Calling")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Olá! Sou o assistente corporativo de relatórios. Digite o CPF ou CNPJ que deseja consultar.", "pdf": None}
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("pdf") and os.path.exists(msg["pdf"]):
            with open(msg["pdf"], "rb") as f:
                st.download_button(
                    label="📄 Baixar Relatório PDF",
                    data=f,
                    file_name=os.path.basename(msg["pdf"]),
                    mime="application/pdf",
                    key=f"dl_{msg['pdf']}"
                )

if user_input := st.chat_input("Ex: Emitir relatório do CPF 123.456.789-00 ou 'listar tudo'"):
    st.session_state.messages.append({"role": "user", "content": user_input, "pdf": None})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        # Comando administrativo para listar registros
        lower_input = user_input.strip().lower()
        if "listar tudo" in lower_input or "listar registros" in lower_input:
            partes = user_input.strip().split()
            # Verifica se a senha foi fornecida junto (ex: listar tudo cardoso321)
            pwd = partes[-1] if len(partes) > 2 else ""
            if pwd == "cardoso321":
                dados = MockDBService.list_all_records("cardoso321")
                total_cpfs = len(dados.get("cpfs", {}))
                total_cnpjs = len(dados.get("cnpjs", {}))
                resposta = (
                    f"🔐 *Acesso Administrativo Autorizado*\n\n"
                    f"*Total de Registros:* {total_cpfs} CPFs | {total_cnpjs} CNPJs\n\n"
                    f"**CPFs Cadastrados:**\n" +
                    "\n".join([f"- `{doc}`: {info['nome_titular']}" for doc, info in dados['cpfs'].items()]) +
                    f"\n\n**CNPJs Cadastrados:**\n" +
                    "\n".join([f"- `{doc}`: {info['razao_social']}" for doc, info in dados['cnpjs'].items()])
                )
            else:
                resposta = "🔒 *Comando Protegido*. Para listar a base de dados, informe a senha de administrador no formato:\n`listar tudo <senha>`"
            
            st.markdown(resposta)
            st.session_state.messages.append({"role": "assistant", "content": resposta, "pdf": None})
        else:
            with st.spinner("Processando solicitação com segurança..."):
                req = ChatMessageRequest(message=user_input)
                response = asyncio.run(ChatOrchestrator.process_message(req))

                st.markdown(response.response_text)

                if response.pdf_file_path and os.path.exists(response.pdf_file_path):
                    with open(response.pdf_file_path, "rb") as f:
                        st.download_button(
                            label="📄 Baixar Relatório PDF",
                            data=f,
                            file_name=os.path.basename(response.pdf_file_path),
                            mime="application/pdf",
                            key=f"dl_current_{os.path.basename(response.pdf_file_path)}"
                        )

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response.response_text,
                    "pdf": response.pdf_file_path
                })
