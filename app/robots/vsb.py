from __future__ import annotations

import zipfile
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

import requests


class VsbRobotError(Exception):
    """Erros de execução do robô VSB."""


def _default_competencia() -> str:
    """Retorna o mês anterior no formato YYYY.MM."""
    hoje = datetime.utcnow()
    mes_anterior = (hoje.replace(day=1) - timedelta(days=1)).replace(day=1)
    return mes_anterior.strftime("%Y.%m")


def _request_zip_metadata(codigo_ons: str, competencia: str) -> Dict[str, str]:
    url = f"https://www.vsbtrans.com.br/getFiles.php?codigo={codigo_ons}&data={competencia}"
    headers = {
        "accept": "*/*",
        "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "priority": "u=1, i",
        "referer": "https://www.vsbtrans.com.br/",
        "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
        ),
    }

    response = requests.get(url, headers=headers, timeout=30)
    if response.status_code != 200:
        raise VsbRobotError(
            f"Falha ao consultar metadados para {codigo_ons} ({competencia}). "
            f"Status {response.status_code}"
        )

    try:
        return response.json()
    except ValueError as exc:
        raise VsbRobotError(
            f"Resposta inválida do endpoint VSB para {codigo_ons}: {response.text[:200]}"
        ) from exc


def _download_zip(download_url: str, destino_zip: Path) -> None:
    response = requests.get(download_url, timeout=60)
    if response.status_code != 200:
        raise VsbRobotError(
            f"Falha ao baixar ZIP ({download_url}). Status {response.status_code}"
        )

    content_type = response.headers.get("Content-Type", "")
    if "zip" not in content_type:
        raise VsbRobotError(
            f"Conteúdo inesperado ao baixar ZIP ({download_url}): {content_type}"
        )

    destino_zip.parent.mkdir(parents=True, exist_ok=True)
    destino_zip.write_bytes(response.content)


def _extract_zip(zip_path: Path, extract_dir: Path) -> List[Path]:
    arquivos: List[Path] = []
    try:
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_dir)
            arquivos = [extract_dir / name for name in zip_ref.namelist()]
    except zipfile.BadZipFile as exc:
        raise VsbRobotError(f"Arquivo ZIP corrompido: {zip_path}") from exc
    finally:
        if zip_path.exists():
            zip_path.unlink()
    return arquivos


def run_vsb_robot(
    codigo_ons: str,
    competencia: Optional[str] = None,
    download_dir: Optional[Path] = None,
) -> Dict[str, object]:
    """Executa o robô VSB para o código informado."""
    competencia_final = competencia or _default_competencia()

    base_dir = Path(download_dir or Path("data") / "vsb")
    destino = base_dir / competencia_final / codigo_ons
    destino.mkdir(parents=True, exist_ok=True)

    metadata = _request_zip_metadata(codigo_ons, competencia_final)
    zip_url = metadata.get("zipUrl")
    if not zip_url:
        raise VsbRobotError(
            f"'zipUrl' não encontrado para {codigo_ons} na competência {competencia_final}."
        )

    if zip_url.startswith("http"):
        download_url = zip_url
    else:
        download_url = f"https://www.vsbtrans.com.br{zip_url}"

    zip_path = destino / f"{competencia_final}_{codigo_ons}_faturas.zip"
    _download_zip(download_url, zip_path)
    arquivos = _extract_zip(zip_path, destino)

    return {
        "codigo_ons": codigo_ons,
        "competencia": competencia_final,
        "destino": destino,
        "arquivos": arquivos,
        "metadata": metadata,
    }


__all__ = ["run_vsb_robot", "VsbRobotError"]
