import re

def limpar_cep(valor: str) -> str:
    return re.sub(r"\D", "", valor or "")

def cep_valido(cep: str) -> bool:
    return len(cep) == 8 and cep.isdigit()