"""Batch importer for multiple AVD spreadsheets."""

from __future__ import annotations

import argparse
from decimal import Decimal
from pathlib import Path
from typing import Iterable, List, Tuple

import sys

from sqlalchemy.orm import Session, sessionmaker

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from models.tust_models import (  # noqa: E402
    Base,
    RsmTustAvisoDebito,
    RsmTustAvisoDebitoItem,
    create_sqlite_engine,
)
from scripts.import_avd_excel import parse_avd  # noqa: E402


def _iter_input_paths(paths: Iterable[Path], recursive: bool = False) -> List[Path]:
    resolved: List[Path] = []
    for path in paths:
        if path.is_file():
            resolved.append(path)
        elif path.is_dir():
            pattern = "**/*.xlsx" if recursive else "*.xlsx"
            resolved.extend(sorted(path.glob(pattern)))
    return resolved


def import_single_avd(
    session: Session, path: Path, overwrite: bool = False
) -> Tuple[int, bool]:
    """
    Importa um único arquivo AVD.

    Retorna (id, created) onde created indica se houve inserção nova.
    """
    header, items = parse_avd(path)
    numero_avd = str(header["numero_avd"])

    existing = (
        session.query(RsmTustAvisoDebito)
        .filter_by(numeroavd=numero_avd)
        .one_or_none()
    )

    if existing and not overwrite:
        return existing.id_avisodebito, False

    if existing and overwrite:
        session.query(RsmTustAvisoDebitoItem).filter_by(
            identificadoravisodebitotransmissao=existing.id_avisodebito
        ).delete()
        session.delete(existing)
        session.flush()

    avd = RsmTustAvisoDebito(
        identificador=int(header["numero_avd"]),
        codigoempresa=header["codigo_empresa"],
        codigofilial=header["nome_empresa"],
        codigoons=items[0]["codigo_ons"] if items else None,
        nomeempresa=header["nome_empresa"],
        numeroavd=numero_avd,
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
    return avd.id_avisodebito, True


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Importa múltiplas planilhas AVD em lote."
    )
    parser.add_argument(
        "inputs",
        type=Path,
        nargs="+",
        help="Arquivos .xlsx ou diretórios que contenham planilhas.",
    )
    parser.add_argument(
        "--db-url",
        default="sqlite:///tust.db",
        help="URL do banco compatível com SQLAlchemy (padrão: sqlite:///tust.db).",
    )
    parser.add_argument("--echo", action="store_true", help="Ativa echo SQL.")
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Sobrescreve AVDs já existentes (apaga e reimporta).",
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Ao receber diretórios, procura arquivos .xlsx recursivamente.",
    )
    args = parser.parse_args()

    engine = create_sqlite_engine(args.db_url, echo=args.echo)
    Base.metadata.create_all(engine)
    SessionFactory = sessionmaker(bind=engine)

    targets = _iter_input_paths(args.inputs, recursive=args.recursive)
    if not targets:
        print("Nenhum arquivo .xlsx encontrado no caminho informado.")
        return

    with SessionFactory() as session:
        for path in targets:
            avd_id, created = import_single_avd(session, path, overwrite=args.overwrite)
            if created:
                print(f"{path.name}: importado com id {avd_id}.")
            else:
                print(f"{path.name}: existente (id {avd_id}), não importado.")


if __name__ == "__main__":
    main()
