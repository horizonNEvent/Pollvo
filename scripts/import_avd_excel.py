"""Utilities to load AVD spreadsheets into the SQLite database using SQLAlchemy."""

from __future__ import annotations

import argparse
import zipfile
from datetime import datetime, timedelta
from decimal import Decimal
from pathlib import Path
import sys
from typing import Dict, Iterable, List, Tuple
from xml.etree import ElementTree as ET
import unicodedata

from sqlalchemy.orm import Session, sessionmaker

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from models.tust_models import (
    Base,
    RsmTustAvisoDebito,
    RsmTustAvisoDebitoItem,
    create_sqlite_engine,
)

XL_NS = {"main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
EXCEL_EPOCH = datetime(1899, 12, 30)
PT_BR_MONTHS = {
    "janeiro": 1,
    "fevereiro": 2,
    "marco": 3,
    "abril": 4,
    "maio": 5,
    "junho": 6,
    "julho": 7,
    "agosto": 8,
    "setembro": 9,
    "outubro": 10,
    "novembro": 11,
    "dezembro": 12,
}


def _load_workbook(path: Path) -> Tuple[List[str], List[Tuple[int, Dict[str, str]]]]:
    """Return (shared_strings, rows) extracted directly from the XLSX XML."""
    with zipfile.ZipFile(path) as zf:
        shared = zf.read("xl/sharedStrings.xml")
        sheet = zf.read("xl/worksheets/sheet1.xml")
    shared_strings = _parse_shared_strings(shared)
    rows = _parse_sheet(sheet, shared_strings)
    return shared_strings, rows


def _parse_shared_strings(data: bytes) -> List[str]:
    root = ET.fromstring(data)
    values: List[str] = []
    for si in root.findall("main:si", XL_NS):
        pieces = []
        for node in si.iterfind(".//main:t", XL_NS):
            pieces.append(node.text or "")
        values.append("".join(pieces))
    return values


def _parse_sheet(
    data: bytes, shared_strings: Iterable[str]
) -> List[Tuple[int, Dict[str, str]]]:
    root = ET.fromstring(data)
    rows: List[Tuple[int, Dict[str, str]]] = []
    for row in root.findall(".//main:sheetData/main:row", XL_NS):
        row_map: Dict[str, str] = {}
        for cell in row.findall("main:c", XL_NS):
            ref = cell.attrib["r"]
            col = "".join(filter(str.isalpha, ref))
            value = None
            if cell.attrib.get("t") == "s":
                v = cell.find("main:v", XL_NS)
                if v is not None:
                    value = shared_strings[int(v.text)]
            else:
                v = cell.find("main:v", XL_NS)
                if v is not None:
                    value = v.text
            if value is not None:
                row_map[col] = value
        if row_map:
            rows.append((int(row.attrib["r"]), row_map))
    return rows


def _excel_serial_to_datetime(serial: str) -> datetime:
    """Convert Excel serial value to datetime (supports fractional time)."""
    value = float(serial)
    days = int(value)
    remainder = value - days
    return EXCEL_EPOCH + timedelta(days=days, seconds=remainder * 86400)


def _parse_period(text: str) -> datetime:
    """Parse strings como 'Outubro/2025' to the first day of that month."""
    month_str, year_str = text.split("/")
    normalized = _normalize_month_name(month_str)
    month = PT_BR_MONTHS[normalized]
    year = int(year_str)
    return datetime(year, month, 1)


def _parse_due(text: str) -> datetime:
    """Parse strings like '1a. Parcela dia 15/11/2025' into a date."""
    try:
        date_part = text.split("dia", 1)[1].strip()
    except IndexError:  # fallback when format is unexpected
        raise ValueError(f"Could not parse due date text: {text}") from None
    return datetime.strptime(date_part, "%d/%m/%Y")


def _decimal_or_none(value: str) -> Decimal | None:
    if value is None or value == "":
        return None
    return Decimal(value)


def _normalize_month_name(text: str) -> str:
    cleaned = "".join(
        ch for ch in unicodedata.normalize("NFKD", text.strip().lower()) if not unicodedata.combining(ch)
    )
    return cleaned


def _build_rows_map(rows: List[Tuple[int, Dict[str, str]]]) -> Dict[int, Dict[str, str]]:
    return {idx: data for idx, data in rows}


def parse_avd(path: Path) -> Tuple[Dict[str, object], List[Dict[str, object]]]:
    """Extract header info and item rows from the spreadsheet."""
    _, rows = _load_workbook(path)
    map_rows = _build_rows_map(rows)

    header = {
        "numero_avd": map_rows[1]["D"],
        "encargo_mensal": _decimal_or_none(map_rows[1].get("G")),
        "codigo_empresa": map_rows[2]["A"],
        "nome_empresa": map_rows[2]["B"],
        "periodo_apuracao": _parse_period(map_rows[2]["D"]),
        "pv_spb": _decimal_or_none(map_rows[2].get("G")),
        "data_disponibilizacao": _excel_serial_to_datetime(map_rows[3]["D"]),
        "total_sem_pis_cofins": _decimal_or_none(map_rows[3].get("G")),
        "vencimento_parcela1": _parse_due(map_rows[5]["D"]),
        "vencimento_parcela2": _parse_due(map_rows[5]["E"]),
        "vencimento_parcela3": _parse_due(map_rows[5]["F"]),
    }

    items: List[Dict[str, object]] = []
    for row_idx, data in rows:
        if row_idx <= 5:
            continue
        codigo_ons = data.get("A")
        if not codigo_ons:
            continue
        items.append(
            {
                "codigo_ons": codigo_ons,
                "nome_transmissora": data.get("B"),
                "cnpj": data.get("C"),
                "valor_parcela1": _decimal_or_none(data.get("D")),
                "valor_parcela2": _decimal_or_none(data.get("E")),
                "valor_parcela3": _decimal_or_none(data.get("F")),
                "valor_total": _decimal_or_none(data.get("H")),
                "valor_pis_cofins": _decimal_or_none(data.get("G")),
            }
        )
    return header, items


def import_avd(session: Session, path: Path) -> int:
    header, items = parse_avd(path)
    avd = RsmTustAvisoDebito(
        identificador=int(header["numero_avd"]),
        codigoempresa=header["codigo_empresa"],
        codigofilial=header["nome_empresa"],
        codigoons=items[0]["codigo_ons"] if items else None,
        nomeempresa=header["nome_empresa"],
        numeroavd=str(header["numero_avd"]),
        datacompetencia=header["periodo_apuracao"],
        datavencimentoparcela1=header["vencimento_parcela1"],
        datavencimentoparcela2=header["vencimento_parcela2"],
        datavencimentoparcela3=header["vencimento_parcela3"],
    )
    session.add(avd)
    session.flush()

    for idx, item in enumerate(items, start=1):
        session.add(
            RsmTustAvisoDebitoItem(
                identificador=idx,
                identificadoravisodebitotransmissao=avd.id_avisodebito,
                codigoons=item["codigo_ons"],
                nometransmissora=item["nome_transmissora"],
                cnpjtransmissora=item["cnpj"],
                valorparcela1=item["valor_parcela1"] or Decimal("0"),
                valorparcela2=item["valor_parcela2"] or Decimal("0"),
                valorparcela3=item["valor_parcela3"] or Decimal("0"),
                valortotal=item["valor_total"] or Decimal("0"),
            )
        )

    session.commit()
    return avd.id_avisodebito


def main() -> None:
    parser = argparse.ArgumentParser(description="Import AVD spreadsheet into SQLite DB.")
    parser.add_argument("excel_path", type=Path, help="Path to the .xlsx file to import.")
    parser.add_argument(
        "--db-url",
        default="sqlite:///tust.db",
        help="SQLAlchemy database URL (default: sqlite:///tust.db).",
    )
    parser.add_argument("--echo", action="store_true", help="Enable SQL echo during import.")
    args = parser.parse_args()

    engine = create_sqlite_engine(args.db_url, echo=args.echo)
    Base.metadata.create_all(engine)
    SessionFactory = sessionmaker(bind=engine)

    with SessionFactory() as session:
        avd_id = import_avd(session, args.excel_path)
        print(f"Imported AVD into RSM_TUSTAVISODEBITO with id {avd_id}.")


if __name__ == "__main__":
    main()
