from __future__ import annotations

from pathlib import Path
import datetime
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.robots.vsb import VsbRobotError, run_vsb_robot
from app.parsers.nfe import parse_nfe_directory
from app.validators.avd import AVDValidationError, conciliar_notas_com_avd
from app.services.database import db_session

app = FastAPI(title="TUST Robots API")


class VsbRequest(BaseModel):
    codigo_ons: str = Field(..., min_length=1, description="Código ONS da transmissora.")
    competencia: Optional[str] = Field(
        None, pattern=r"^\d{4}\.\d{2}$", description="Competência no formato YYYY.MM."
    )
    download_dir: Optional[Path] = Field(
        None, description="Diretório base para salvar os arquivos baixados."
    )
    processar: bool = Field(
        default=False,
        description="Se verdadeiro, extrai dados das NF-es e atualiza o banco com a conciliação.",
    )
    db_url: Optional[str] = Field(
        default=None, description="URL do banco SQLAlchemy (default sqlite:///tust.db)."
    )


class VsbResponse(BaseModel):
    codigo_ons: str
    competencia: str
    arquivos: list[str]
    destino: str
    processamento: Optional[dict] = None


@app.post("/robots/vsb", response_model=VsbResponse, summary="Executa o robô da VSB.")
async def trigger_vsb_robot(payload: VsbRequest) -> VsbResponse:
    try:
        result = run_vsb_robot(
            codigo_ons=payload.codigo_ons,
            competencia=payload.competencia,
            download_dir=payload.download_dir,
        )
    except VsbRobotError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    processamento = None
    if payload.processar:
        competencia_str = result["competencia"]
        destino_path = Path(result["destino"])
        ano, mes = competencia_str.split(".")
        competencia_date = datetime.date(int(ano), int(mes), 1)
        invoices = parse_nfe_directory(destino_path, payload.codigo_ons, competencia_date)
        try:
            with db_session(payload.db_url) as session:
                processamento = conciliar_notas_com_avd(
                    session,
                    payload.codigo_ons,
                    competencia_date,
                    invoices,
                )
        except AVDValidationError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    return VsbResponse(
        codigo_ons=result["codigo_ons"],
        competencia=result["competencia"],
        arquivos=[str(path) for path in result["arquivos"]],
        destino=str(result["destino"]),
        processamento=processamento,
    )

