import os
import streamlit as st
import asyncio
from app.schemas.chat import ChatMessageRequest
from app.services.chat_orchestrator import ChatOrchestrator

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

if user_input := st.chat_input("Ex: Emitir relatório do CPF 123.456.789-00"):
    st.session_state.messages.append({"role": "user", "content": user_input, "pdf": None})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
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
                        key="dl_current"
                    )

            st.session_state.messages.append({
                "role": "assistant",
                "content": response.response_text,
                "pdf": response.pdf_file_path
            })
