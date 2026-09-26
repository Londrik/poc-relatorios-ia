# Roteiro de Apresentação Executiva para a Diretoria (15 Minutos)

## 1. Abertura & Desafio (3 Minutos)
- Apresentar o problema: Automatizar a entrega de relatórios cadastrais/compliance via WhatsApp com total segurança e conformidade LGPD.
- Destacar o diferencial: O projeto não é um chatbot comum que alucina dados, mas sim uma plataforma de Engenharia de IA segura e determinística.

## 2. Demonstração Ao Vivo (5 Minutos)
- Exibir a tela do Streamlit (`streamlit run streamlit_app.py`).
- Teste 1 (Segurança LGPD): Digitar "Gere o relatório do CPF 123.456.789-00" e mostrar o log do mascaramento em milissegundos ("***.456.789-**").
- Teste 2 (Function Calling): Mostrar o relatório PDF gerado na hora com botão de download.
- Teste 3 (Proteção OWASP): Digitar uma tentativa de ataque ("Ignore as regras...") e mostrar o bloqueio imediato pelo Guardrail.

## 3. Defesa de Arquitetura & Custos (4 Minutos)
- Apresentar os artefatos de Arquitetura C4 Model e Sanitização.
- Exibir a tabela de custos operacionais: R$ 45,00 a R$ 300,00/mês para 200 usuários ativos.
- Destacar Zero Data Retention nos provedores de LLM.

## 4. Próximos Passos & Fechamento (3 Minutos)
- MVP pronto em 2 a 4 meses.
- Decisão sobre provedor inicial de LLM (Gemini, Azure OpenAI ou AWS Bedrock).
