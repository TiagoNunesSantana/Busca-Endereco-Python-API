import requests

class ViaCepError(Exception):
    pass

def buscar_cep(cep: str) -> dict:
    url = f"https://viacep.com.br/ws/{cep}/json/"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except requests.RequestException as e:
        raise ViaCepError("Falha ao conectar no ViaCEP.") from e

    if data.get("erro"):
        raise ViaCepError("CEP não encontrado.")

    return data