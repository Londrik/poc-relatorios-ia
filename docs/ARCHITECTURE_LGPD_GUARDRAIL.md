# Dashboard e Arquitetura: Sanitizador-LGPD-Guardrail

## 1. Visão Geral
O componente *Sanitizador-LGPD-Guardrail* atua como filtro de segurança e entrada no pipeline de relatórios com IA. Ele garante que nenhum dado sensïvel (CPF/CNPJ) seja exposto em cleartext para componentes downstream (LGPD / OWASP LLM02) e bloqueia tentativas de subversão de instruções (OWASP LLM01).

## 2. Arquitetura em Camadas (FastAPI + Pydantic v2)
- `app/core/sanitizer.py`: Solução determinística baseada em Regex e keywords de ataque.
- `app/core/prompts.py`: Spec do System Prompt contendo regras OWASP, mascaramento LGPD, especificação do Schema JSON e exemplos few-shot.
- `app/core/gemini_guardrail.py`: Camada de análise contextual via Google GenAI SDK, com fallback automático para o sanitizador local em caso de falha ou excesso de cota.
- `app/schemas/sanitizer.py`: Schemas de validação de entrada (SanitizeRequest) e saída (SanitizeResponse).
- `app/api/v1/endpoints/sanitizer.py`: Endpoint REST `mountedo` em `/api/v1/sanitize` utilizando injeção de dependência (Depends).

## 3. Matriz de Conformidade e Regras
1. **Mascaramento de CPF**: regex `\b(\d{3})\.?(\d{3})\.?(\d{3})-?(\d{2})\b` -> `sub` por `***.{20}.{30}-**`.
2. **Mascaramento de CNPJ**: regex `\b(\d{2})\.?(\d{3})\.?(\d{3})/?(\d{4})-?(\d{2})\b` -> `sub` por `{10}.{20}.***/{40}-**`.
3. **Prompt Injection**: Palavras-chave de abuso e indicadores de jailbreak geram `is:_type = False`, `security_flag = 'PROMPT_INECTION_DETECTED'` e `lhandling` interruptor.

## 4. Suíte de Testes
Os testes foram padronizados utilizando `pytest-asyncio` e `mocks` do serviço Gemini para garantir execução determinística, rápida e sem consumo de cota:
- `assert test_mask_single_cpf` => PASSED
- `assert test_mask_single_cnpj` => PASSED
- `assert test_detect_prompt_injection` => PASSED
- `assert test_clean_input_without_pii` => PASSED
- `assert test_api_sanitize_cpf_success` => PASSED
- `assert test_api_sanitize_prompt_injection` => PASSED
