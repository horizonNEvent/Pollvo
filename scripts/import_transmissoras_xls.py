from __future__ import annotations

import argparse
import unicodedata
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import Dict, Iterable, Tuple

import sys

import xlrd  # type: ignore
from sqlalchemy.orm import Session, sessionmaker

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from models.tust_models import (  # noqa: E402
    Base,
    RsmTustTransmissora,
    create_sqlite_engine,
)

HEADER_MAP = {
    "codigo": "codigo_ons",
    "código": "codigo_ons",
    "sigla_do_agente": "sigla_agente",
    "sigla do agente": "sigla_agente",
    "tipo_do_agente": "tipo_agente",
    "razão_social": "razao_social",
    "razao_social": "razao_social",
    "cnpj": "cnpj",
    "inscrição_estadual": "inscricao_estadual",
    "inscricao_estadual": "inscricao_estadual",
    "classificação_empresa": "classificacao_empresa",
    "classificacao_empresa": "classificacao_empresa",
    "logradouro": "logradouro",
    "numero": "numero",
    "número": "numero",
    "complemento": "complemento",
    "bairro": "bairro",
    "cidade": "cidade",
    "uf": "uf",
    "cep": "cep",
    "região": "regiao",
    "regiao": "regiao",
    "banco": "banco",
    "numero_do_banco": "numero_do_banco",
    "numero do banco": "numero_do_banco",
    "agencia": "agencia",
    "agência": "agencia",
    "conta": "conta",
    "forma_de_encaminhamento_das_fat": "forma_encaminhamento_faturas",
    "forma de encaminhamento das fat": "forma_encaminhamento_faturas",
    "url_do_site": "url_site",
    "url do site": "url_site",
    "%_aliquota_pis_confins": "aliquota_pis_confins",
    "% aliquota pis confins": "aliquota_pis_confins",
    "concessão": "concessao",
    "concessao": "concessao",
    "dt_concessão": "dt_concessao",
    "dt concessão": "dt_concessao",
    "dt_concessao": "dt_concessao",
    "contrato": "contrato",
    "dt_inicio_contábil": "dt_inicio_contabil",
    "dt inicio contábil": "dt_inicio_contabil",
    "dt_inicio_contabil": "dt_inicio_contabil",
    "dt_inicio_operação": "dt_inicio_operacao",
    "dt inicio operação": "dt_inicio_operacao",
    "dt_inicio_operacao": "dt_inicio_operacao",
    "idai": "idai",
}


def normalize_header(text: str) -> str:
    cleaned = "".join(
        ch
        for ch in unicodedata.normalize("NFKD", text.strip().lower())
        if not unicodedata.combining(ch)
    )
    return cleaned.replace(" ", "_")


def load_sheet(path: Path) -> Tuple[xlrd.book.Book, xlrd.sheet.Sheet]:
    workbook = xlrd.open_workbook(path, encoding_override="utf-8")
    sheet = workbook.sheet_by_index(0)
    return workbook, sheet


def extract_header_indexes(sheet: xlrd.sheet.Sheet) -> Dict[str, int]:
    headers: Dict[str, int] = {}
    for col_idx in range(sheet.ncols):
        raw_header = sheet.cell_value(0, col_idx)
        header_key = HEADER_MAP.get(normalize_header(str(raw_header)))
        if header_key:
            headers[header_key] = col_idx
    return headers


def get_cell_value(
    book: xlrd.book.Book, sheet: xlrd.sheet.Sheet, row: int, col: int
) -> str | Decimal | datetime | None:
    if col < 0:
        return None
    cell = sheet.cell(row, col)
    if cell.ctype == xlrd.XL_CELL_EMPTY:
        return None
    if cell.ctype == xlrd.XL_CELL_NUMBER:
        # Tenta converter valores numéricos em datas; xlrd levanta ValueError se não for data.
        try:
            return xlrd.xldate.xldate_as_datetime(cell.value, book.datemode)
        except (ValueError, TypeError, AttributeError):
            pass
        if float(cell.value).is_integer():
            return Decimal(str(int(cell.value)))
        return Decimal(str(cell.value))
    if cell.ctype == xlrd.XL_CELL_DATE:
        return xlrd.xldate.xldate_as_datetime(cell.value, book.datemode)
    value = str(cell.value).strip()
    return value or None


def decimal_or_none(value: str | Decimal | None) -> Decimal | None:
    if value is None:
        return None
    if isinstance(value, Decimal):
        return value
    value_str = (
        str(value)
        .strip()
        .replace("%", "")
        .replace(".", "")
        .replace(",", ".")
        .replace(" ", "")
    )
    if not value_str or value_str in {"-", "--"}:
        return None
    try:
        return Decimal(value_str)
    except Exception:
        return None


def str_or_none(value: str | Decimal | None) -> str | None:
    if value is None:
        return None
    if isinstance(value, Decimal):
        # manter representacao sem .0 quando inteiro
        if value == value.to_integral():
            return str(int(value))
        return format(value, "f").rstrip("0").rstrip(".")
    text = str(value).strip()
    return text or None


def date_or_none(value: str | Decimal | datetime | None) -> datetime | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value
    text = str(value).strip()
    if not text or text in {"########"}:
        return None
    for fmt in ("%d/%m/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            continue
    return None


def import_transmissoras(session: Session, path: Path) -> int:
    book, sheet = load_sheet(path)
    headers = extract_header_indexes(sheet)
    if "codigo_ons" not in headers:
        raise ValueError("Cabeçalho 'CÓDIGO' não encontrado no arquivo XLS.")

    inserted = 0
    for row_idx in range(1, sheet.nrows):
        codigo_ons = str_or_none(
            get_cell_value(book, sheet, row_idx, headers["codigo_ons"])
        )
        if not codigo_ons:
            continue

        data = {
            "codigoons": codigo_ons,
            "nome": str_or_none(
                get_cell_value(book, sheet, row_idx, headers.get("sigla_agente", -1))
            ),
            "razaosocial": str_or_none(
                get_cell_value(book, sheet, row_idx, headers.get("razao_social", -1))
            ),
            "cnpj": str_or_none(
                get_cell_value(book, sheet, row_idx, headers.get("cnpj", -1))
            ),
            "inscricaoestadual": str_or_none(
                get_cell_value(
                    book, sheet, row_idx, headers.get("inscricao_estadual", -1)
                )
            ),
            "classificacaoempresa": str_or_none(
                get_cell_value(
                    book, sheet, row_idx, headers.get("classificacao_empresa", -1)
                )
            ),
            "endereco_logradouro": str_or_none(
                get_cell_value(book, sheet, row_idx, headers.get("logradouro", -1))
            ),
            "endereco_numero": str_or_none(
                get_cell_value(book, sheet, row_idx, headers.get("numero", -1))
            ),
            "endereco_complemento": str_or_none(
                get_cell_value(book, sheet, row_idx, headers.get("complemento", -1))
            ),
            "endereco_bairro": str_or_none(
                get_cell_value(book, sheet, row_idx, headers.get("bairro", -1))
            ),
            "endereco_cidade": str_or_none(
                get_cell_value(book, sheet, row_idx, headers.get("cidade", -1))
            ),
            "endereco_estado": str_or_none(
                get_cell_value(book, sheet, row_idx, headers.get("uf", -1))
            ),
            "endereco_cep": str_or_none(
                get_cell_value(book, sheet, row_idx, headers.get("cep", -1))
            ),
            "regiao": str_or_none(
                get_cell_value(book, sheet, row_idx, headers.get("regiao", -1))
            ),
            "nomebanco": str_or_none(
                get_cell_value(book, sheet, row_idx, headers.get("banco", -1))
            ),
            "numerobanco": str_or_none(
                get_cell_value(book, sheet, row_idx, headers.get("numero_do_banco", -1))
            ),
            "agencia": str_or_none(
                get_cell_value(book, sheet, row_idx, headers.get("agencia", -1))
            ),
            "conta": str_or_none(
                get_cell_value(book, sheet, row_idx, headers.get("conta", -1))
            ),
            "formaencaminhamentofaturas": str_or_none(
                get_cell_value(
                    book,
                    sheet,
                    row_idx,
                    headers.get("forma_encaminhamento_faturas", -1),
                )
            ),
            "urlsite": str_or_none(
                get_cell_value(book, sheet, row_idx, headers.get("url_site", -1))
            ),
            "percentualaliquotapiscofins": decimal_or_none(
                get_cell_value(
                    book, sheet, row_idx, headers.get("aliquota_pis_confins", -1)
                )
            ),
            "codigoconcessao": str_or_none(
                get_cell_value(book, sheet, row_idx, headers.get("concessao", -1))
            ),
            "dataconcessao": date_or_none(
                get_cell_value(book, sheet, row_idx, headers.get("dt_concessao", -1))
            ),
            "codigocontrato": str_or_none(
                get_cell_value(book, sheet, row_idx, headers.get("contrato", -1))
            ),
            "datainiciocontabil": date_or_none(
                get_cell_value(
                    book, sheet, row_idx, headers.get("dt_inicio_contabil", -1)
                )
            ),
            "datainiciooperacao": date_or_none(
                get_cell_value(
                    book, sheet, row_idx, headers.get("dt_inicio_operacao", -1)
                )
            ),
        }

        existing = (
            session.query(RsmTustTransmissora)
            .filter_by(codigoons=data["codigoons"])
            .one_or_none()
        )
        if existing:
            for attr, value in data.items():
                setattr(existing, attr, value)
        else:
            session.add(RsmTustTransmissora(**data))  # type: ignore[arg-type]
            inserted += 1

    session.commit()
    return inserted


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Importa transmissoras para RSM_TUSTTRANSMISSORA a partir de XLS."
    )
    parser.add_argument("xls_path", type=Path, help="Caminho do arquivo .xls de transmissoras.")
    parser.add_argument(
        "--db-url",
        default="sqlite:///tust.db",
        help="URL do banco suportada pelo SQLAlchemy (padrão: sqlite:///tust.db).",
    )
    parser.add_argument("--echo", action="store_true", help="Ativa echo SQL.")
    args = parser.parse_args()

    engine = create_sqlite_engine(args.db_url, echo=args.echo)
    Base.metadata.create_all(engine)
    SessionFactory = sessionmaker(bind=engine)

    with SessionFactory() as session:
        count = import_transmissoras(session, args.xls_path)
        print(f"Import concluiu com {count} novas transmissoras inseridas/atualizadas.")


if __name__ == "__main__":
    main()
