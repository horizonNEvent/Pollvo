from __future__ import annotations

import datetime as dt
from decimal import Decimal
from typing import List, Optional

from sqlalchemy.orm import Session

from models.tust_models import (
    RsmTustAvisoDebito,
    RsmTustAvisoDebitoItem,
    RsmTustFatTransmissaoNf,
    RsmTustTransmissora,
)

from app.parsers.nfe import NFeInvoice


class AVDValidationError(Exception):
    """Erro ao conciliar notas com AVD."""


def _find_avd(session: Session, codigo_empresa: str, competencia: dt.datetime) -> Optional[RsmTustAvisoDebito]:
    return (
        session.query(RsmTustAvisoDebito)
        .filter(
            RsmTustAvisoDebito.codigoempresa == codigo_empresa,
            RsmTustAvisoDebito.datacompetencia == competencia,
        )
        .one_or_none()
    )


def _find_transmissora_por_cnpj(session: Session, cnpj: str) -> Optional[RsmTustTransmissora]:
    return (
        session.query(RsmTustTransmissora)
        .filter(RsmTustTransmissora.cnpj == cnpj)
        .one_or_none()
    )


def _find_avd_item(session: Session, avd_id: int, codigo_transmissora: str) -> Optional[RsmTustAvisoDebitoItem]:
    return (
        session.query(RsmTustAvisoDebitoItem)
        .filter(
            RsmTustAvisoDebitoItem.identificadoravisodebitotransmissao == avd_id,
            RsmTustAvisoDebitoItem.codigoons == codigo_transmissora,
        )
        .one_or_none()
    )


def _persist_notas_fiscais(
    session: Session, avd: RsmTustAvisoDebito, invoices: List[NFeInvoice]
) -> List[RsmTustFatTransmissaoNf]:
    registros: List[RsmTustFatTransmissaoNf] = []
    for invoice in invoices:
        nf = RsmTustFatTransmissaoNf(
            datainclusao=dt.datetime.utcnow(),
            identificador=avd.identificador,
            identificadorfaturatransmissao=avd.id_avisodebito,
            cnpj_emissor=invoice.cnpj_emitente,
            nome_emissor=invoice.nome_emitente,
            cnpj_destinatario=invoice.cnpj_destinatario,
            nome_destinatario=invoice.nome_destinatario,
            numeronotafiscal=invoice.numero_nfe,
            numerofatura=invoice.numero_fatura,
            dataemissao=invoice.data_emissao,
            datavencimento=invoice.data_vencimento,
            valortotal=invoice.valor_total,
            chavenfe=invoice.chave_nfe,
        )
        session.add(nf)
        registros.append(nf)
    session.flush()
    return registros


def _avaliar_divergencia(item: Optional[RsmTustAvisoDebitoItem], invoice: NFeInvoice) -> Optional[str]:
    if item is None:
        return "Item da transmissora não encontrado na AVD."

    soma_parcelas = (
        (item.valorparcela1 or Decimal("0"))
        + (item.valorparcela2 or Decimal("0"))
        + (item.valorparcela3 or Decimal("0"))
    )
    if invoice.valor_total != soma_parcelas:
        return f"Valor da NF ({invoice.valor_total}) diferente da soma de parcelas ({soma_parcelas})."

    return None


def conciliar_notas_com_avd(
    session: Session,
    codigo_empresa: str,
    competencia: dt.date,
    invoices: List[NFeInvoice],
) -> dict:
    competencia_dt = dt.datetime.combine(competencia, dt.time())
    avd = _find_avd(session, codigo_empresa, competencia_dt)
    if not avd:
        raise AVDValidationError(f"Não existe AVD para código {codigo_empresa} e competência {competencia}.")

    if not invoices:
        return {"status": "sem_notas", "avd": avd.numeroavd}

    transmissora = _find_transmissora_por_cnpj(session, invoices[0].cnpj_emitente)
    if not transmissora:
        raise AVDValidationError(f"Transmissora com CNPJ {invoices[0].cnpj_emitente} não cadastrada.")

    item = _find_avd_item(session, avd.id_avisodebito, transmissora.codigoons)

    _persist_notas_fiscais(session, avd, invoices)

    validacoes = []
    for invoice in invoices:
        divergencia = _avaliar_divergencia(item, invoice)
        validacoes.append(
            {
                "numero_nfe": invoice.numero_nfe,
                "valor_nf": float(invoice.valor_total),
                "codigo_transmissora": transmissora.codigoons,
                "competencia": competencia.isoformat(),
                "divergencia": divergencia,
            }
        )

    return {
        "status": "ok",
        "avd": avd.numeroavd,
        "transmissora_codigo": transmissora.codigoons,
        "validations": validacoes,
    }
