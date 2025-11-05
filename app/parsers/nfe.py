from __future__ import annotations

import datetime as dt
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from typing import List, Optional
from xml.etree import ElementTree as ET

NFE_NS = {"nfe": "http://www.portalfiscal.inf.br/nfe"}


@dataclass
class NFeInvoice:
    codigo_ons: str
    competencia: dt.date
    cnpj_emitente: str
    nome_emitente: str
    cnpj_destinatario: str
    nome_destinatario: str
    numero_nfe: str
    serie: str
    chave_nfe: str
    numero_fatura: Optional[str]
    valor_total: Decimal
    data_emissao: dt.datetime
    data_vencimento: Optional[dt.date]
    duplicata_numero: Optional[str]
    duplicata_valor: Optional[Decimal]
    arquivo: Path


def _get_text(parent: Optional[ET.Element], path: str) -> Optional[str]:
    if parent is None:
        return None
    element = parent.find(path, NFE_NS)
    if element is None or element.text is None:
        return None
    return element.text.strip()


def _parse_decimal(value: Optional[str]) -> Optional[Decimal]:
    if not value:
        return None
    normalized = value.replace(",", ".")
    return Decimal(normalized)


def parse_nfe_file(xml_path: Path, codigo_ons: str, competencia: dt.date) -> NFeInvoice:
    tree = ET.parse(xml_path)
    root = tree.getroot()

    inf_nfe = root.find("nfe:NFe/nfe:infNFe", NFE_NS)
    if inf_nfe is None:
        raise ValueError(f"Arquivo {xml_path} não contém elemento infNFe.")

    ide = inf_nfe.find("nfe:ide", NFE_NS)
    emit = inf_nfe.find("nfe:emit", NFE_NS)
    dest = inf_nfe.find("nfe:dest", NFE_NS)
    total = inf_nfe.find("nfe:total/nfe:ICMSTot", NFE_NS)
    cobr = inf_nfe.find("nfe:cobr", NFE_NS)

    numero_nfe = _get_text(ide, "nfe:nNF") or ""
    serie = _get_text(ide, "nfe:serie") or ""
    chave = inf_nfe.attrib.get("Id", "")

    dh_emi = _get_text(ide, "nfe:dhEmi")
    data_emissao = (
        dt.datetime.fromisoformat(dh_emi.replace("Z", "+00:00")) if dh_emi else dt.datetime.utcnow()
    )

    numero_fatura = _get_text(cobr, "nfe:fat/nfe:nFat")
    duplicata_numero = _get_text(cobr, "nfe:dup/nfe:nDup")
    duplicata_valor = _parse_decimal(_get_text(cobr, "nfe:dup/nfe:vDup"))
    data_venc_text = _get_text(cobr, "nfe:dup/nfe:dVenc")
    data_vencimento = dt.date.fromisoformat(data_venc_text) if data_venc_text else None

    valor_total = _parse_decimal(_get_text(total, "nfe:vNF")) or Decimal("0")

    return NFeInvoice(
        codigo_ons=codigo_ons,
        competencia=competencia,
        cnpj_emitente=_get_text(emit, "nfe:CNPJ") or "",
        nome_emitente=_get_text(emit, "nfe:xNome") or "",
        cnpj_destinatario=_get_text(dest, "nfe:CNPJ") or "",
        nome_destinatario=_get_text(dest, "nfe:xNome") or "",
        numero_nfe=numero_nfe,
        serie=serie,
        chave_nfe=chave,
        numero_fatura=numero_fatura,
        valor_total=valor_total,
        data_emissao=data_emissao,
        data_vencimento=data_vencimento,
        duplicata_numero=duplicata_numero,
        duplicata_valor=duplicata_valor,
        arquivo=xml_path,
    )


def parse_nfe_directory(destino: Path, codigo_ons: str, competencia: dt.date) -> List[NFeInvoice]:
    notas: List[NFeInvoice] = []
    for xml_path in destino.rglob("*.xml"):
        notas.append(parse_nfe_file(xml_path, codigo_ons, competencia))
    return notas
