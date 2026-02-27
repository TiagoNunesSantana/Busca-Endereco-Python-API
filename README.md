# 📍 Busca Endereço por CEP — API REST (FastAPI)

API REST desenvolvida em Python utilizando FastAPI para consulta de endereço a partir do CEP.

A API é independente e pode ser consumida por qualquer aplicação que realize chamadas HTTP.

---

## 🚀 Objetivo

Disponibilizar um serviço reutilizável de consulta de endereço, permitindo integração com:

- Sistemas corporativos
- Aplicações web
- Aplicações mobile
- Serviços internos
- Clientes REST (Postman, Browser, etc.)

O projeto também demonstra como sistemas legados podem consumir APIs modernas.

---

## ⚙️ Funcionalidades

- Consulta de CEP via ViaCEP
- Retorno estruturado em JSON
- Registro de histórico de consultas
- Preparação para exportação de dados
- Arquitetura desacoplada do cliente

---

## 🔌 Endpoints

### Consulta de CEP

GET /cep/{cep}

Exemplo:
http://127.0.0.1:8000/cep/04151010

Resposta:
```json
{
  "cep": "04151-010",
  "logradouro": "Rua Massaim",
  "bairro": "Bosque da Saúde",
  "cidade": "São Paulo",
  "uf": "SP",
  "ibge": "3550308"
}

▶️ Como executar localmente
Instale as dependências:
pip install -r requirements.txt

Inicie a API:
uvicorn api.main:app --reload

🧩 Arquitetura
Cliente HTTP
    ↓
FastAPI (Python)
    ↓
ViaCEP

A API foi projetada para ser consumida por qualquer cliente HTTP.

🖥 Demonstração de Consumo
A API pode ser utilizada por:
Browser
Postman
Sistemas corporativos
Aplicações desktop


🛠 Tecnologias
Python
FastAPI
REST
JSON
