import io
from typing import List
import pandas as pd

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from services.viacep import buscar_cep, ViaCepError
from utils.validators import limpar_cep, cep_valido
from storage.history import load_history, add_history

app = FastAPI(title="Busca CEP API", version="1.0.0")


class SaveAddress(BaseModel):
    cep: str
    logradouro: str = ""
    bairro: str = ""
    cidade: str = ""
    uf: str = ""
    numero: str = ""
    complemento: str = ""
    ibge: str = ""


@app.get("/cep/{cep}")
def get_cep(cep: str):
    cep_clean = limpar_cep(cep)
    if not cep_valido(cep_clean):
        raise HTTPException(status_code=400, detail="CEP inválido (precisa ter 8 números).")

    try:
        data = buscar_cep(cep_clean)
        mapped = {
            "cep": data.get("cep", ""),
            "logradouro": data.get("logradouro", ""),
            "bairro": data.get("bairro", ""),
            "cidade": data.get("localidade", ""),
            "uf": data.get("uf", ""),
            "ibge": data.get("ibge", ""),
        }
        add_history(mapped)
        return mapped
    except ViaCepError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/history")
def get_history():
    return load_history()


@app.post("/save")
def save_address(payload: SaveAddress):
    add_history(payload.model_dump())
    return {"ok": True}


def _excel_bytes(registros: List[dict]) -> bytes:
    df = pd.DataFrame(registros)
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Enderecos")
    return buf.getvalue()


def _pdf_bytes(registros: List[dict]) -> bytes:
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    w, h = A4

    y = h - 50
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Histórico de Endereços")
    y -= 30
    c.setFont("Helvetica", 10)

    for i, r in enumerate(registros, start=1):
        linha = f"{i}. {r.get('cep','')} - {r.get('logradouro','')}, {r.get('numero','')} {r.get('complemento','') or ''} - {r.get('bairro','')} - {r.get('cidade','')}/{r.get('uf','')}"
        c.drawString(50, y, linha[:110])
        y -= 14
        if y < 60:
            c.showPage()
            y = h - 50
            c.setFont("Helvetica", 10)

    c.save()
    return buf.getvalue()


@app.get("/export/excel")
def export_excel():
    registros = load_history()
    content = _excel_bytes(registros)
    return StreamingResponse(
        io.BytesIO(content),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=historico_enderecos.xlsx"},
    )


@app.get("/export/pdf")
def export_pdf():
    registros = load_history()
    content = _pdf_bytes(registros)
    return StreamingResponse(
        io.BytesIO(content),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=historico_enderecos.pdf"},
    )