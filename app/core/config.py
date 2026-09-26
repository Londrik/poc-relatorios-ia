import os
from pydantic_settings import BaseSettings, SettingsConfigDict

def get_gemini_key() -> str:
    # 1. Verifica variáveis de ambiente
    if key := os.getenv("GEMINI_API_KEY"):
        return key
    # 2. Tenta capturar dos Secrets do Streamlit Cloud
    try:
        import streamlit as st
        if "GEMINI_API_KEY" in st.secrets:
            return st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass
    return ""

class Settings(BaseSettings):
    GEMINI_API_KEY: str = get_gemini_key()
    MODEL_NAME: str = "gemini-2.5-flash"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
