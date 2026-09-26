import sys
import json
import getpass
from app.services.mock_db_service import MockDBService

def main():
    print("=== PAINEL ADMINISTRATIVO: BASE MOCKADA ===")
    
    # Se a senha foi passada como argumento de linha de comando:
    if len(sys.argv) > 1:
        pwd = sys.argv[1]
    else:
        pwd = getpass.getpass("Informe a senha de administrador: ")

    try:
        dados = MockDBService.list_all_records(pwd)
        total_cpfs = len(dados.get("cpfs", {}))
        total_cnpjs = len(dados.get("cnpjs", {}))
        
        print(f"\n[+] Autenticado com sucesso!")
        print(f"[+] Total cadastrado: {total_cpfs} CPFs | {total_cnpjs} CNPJs\n")
        print(json.dumps(dados, indent=2, ensure_ascii=False))
    except PermissionError as e:
        print(f"\n[-] Erro: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
