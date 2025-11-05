from sqlalchemy import Column, DateTime, Integer, Numeric, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class RsmTustProcessoImportacao(Base):
    __tablename__ = "RSM_TUSTPROCESSOIMPORTACAO"

    id_processoimportacao = Column(
        "ID_PROCESSOIMPORTACAO", Integer, primary_key=True, autoincrement=True
    )
    datainclusao = Column("DATAINCLUSAO", DateTime)
    dataalteracao = Column("DATAALTERACAO", DateTime)
    usuarioalteracao = Column("USUARIOALTERACAO", String(30))
    inativo = Column("INATIVO", String(1))
    excluido = Column("EXCLUIDO", String(1))
    dataexclusao = Column("DATAEXCLUSAO", DateTime)
    identificador = Column("IDENTIFICADOR", Integer)


class RsmTustImpAutomatica(Base):
    __tablename__ = "RSM_TUSTIMPAUTOMATICA"

    id_impautomatica = Column(
        "ID_IMPOAUTOMATICA", Integer, primary_key=True, autoincrement=True
    )
    datainclusao = Column("DATAINCLUSAO", DateTime)
    dataalteracao = Column("DATAALTERACAO", DateTime)
    usuarioalteracao = Column("USUARIOALTERACAO", String(30))
    inativo = Column("INATIVO", String(1))
    excluido = Column("EXCLUIDO", String(1))
    dataexclusao = Column("DATAEXCLUSAO", DateTime)
    identificador = Column("IDENTIFICADOR", Integer)
    identificadorprocessoimportacao = Column("IDENTIFICADORPROCESSOIMPORTACAO", Integer)
    horaexecucao = Column("HORAEXECUCAO", DateTime)
    status = Column("STATUS", String(20))
    statusimportacao = Column("STATUSIMPORTACAO", String(20))
    dataultimaexecucao = Column("DATAULTIMAEXECUCAO", DateTime)
    datafimultimaexecucao = Column("DATAFIMULTIMAEXECUCAO", DateTime)
    duracaoultimaexecucao = Column("DURACAOULTIMAEXECUCAO", String(20))


class RsmTustImpAutExecucao(Base):
    __tablename__ = "RSM_TUSTIMPAUTEXECUCAO"

    id_impautexecucao = Column(
        "ID_IMPAUTEXECUCAO", Integer, primary_key=True, autoincrement=True
    )
    datainclusao = Column("DATAINCLUSAO", DateTime)
    dataalteracao = Column("DATAALTERACAO", DateTime)
    inativo = Column("INATIVO", String(1))
    excluido = Column("EXCLUIDO", String(1))
    dataexclusao = Column("DATAEXCLUSAO", DateTime)
    identificador = Column("IDENTIFICADOR", Integer)
    identificadorimportacaoautomatica = Column(
        "IDENTIFICADORIMPORTACAOAUTOMATICA", Integer
    )
    identificadorimportacaodestino = Column(
        "IDENTIFICADORIMPORTACAODESTINO", Integer
    )
    dataexecucao = Column("DATAEXECUCAO", DateTime)
    status = Column("STATUS", String(30))
    qtderros = Column("QTDERROS", Integer)
    identificadorprocessoimportacao = Column("IDENTIFICADORPROCESSOIMPORTACAO", Integer)


class RsmTustImpAutDocumento(Base):
    __tablename__ = "RSM_TUSTIMPAUTDOCUMENTO"

    id_impautdocumento = Column(
        "ID_IMPAUTDOCUMENTO", Integer, primary_key=True, autoincrement=True
    )
    identificador_doc = Column("IDENTIFICADOR_DOC", Integer)
    identificadorimportacaoautomatica = Column(
        "IDENTIFICADORIMPORTACAOAUTOMATICA", Integer
    )
    identificadorimportacaoautomaticaexecucao = Column(
        "IDENTIFICADORIMPORTACAOAUTOMATICAEXECUCAO", Integer
    )
    tipodocumento = Column("TIPODOCUMENTO", String(50))
    datainclusao = Column("DATAINCLUSAO", DateTime)
    dataalteracao = Column("DATAALTERACAO", DateTime)
    inativo = Column("INATIVO", String(1))
    excluido = Column("EXCLUIDO", String(1))
    dataexclusao = Column("DATAEXCLUSAO", DateTime)
    identificador = Column("IDENTIFICADOR", Integer)
    identificadoravisodebitotransmissao = Column(
        "IDENTIFICADORAVISODEBITOTRANSMISSAO", Integer
    )
    identificadoravisodebitotransmissaoitem = Column(
        "IDENTIFICADORAVISODEBITOTRANSMISSAOITEM", Integer
    )
    identificadortransmissora = Column("IDENTIFICADORTRANSMISSORA", Integer)
    identificadorfaturatransmissaopai = Column("IDENTIFICADORFATURATRANSMISSAOPAI", Integer)
    formapagamento = Column("FORMAPAGAMENTO", String(30))
    codigotransmissoraons = Column("CODIGOTRANSMISSORAONS", String(10))
    codigoempresaons = Column("CODIGOEMPRESAONS", String(10))
    codigoempresa = Column("CODIGOEMPRESA", String(10))
    codigofilial = Column("CODIGOFILIAL", String(10))
    datacompetencia = Column("DATACOMPETENCIA", DateTime)
    codigofatura = Column("CODIGOFATURA", String(20))
    datafatura = Column("DATAFATURA", DateTime)
    datavencimento = Column("DATAVENCIMENTO", DateTime)
    valorons = Column("VALORONS", Numeric(18, 2))
    valorfatura = Column("VALORFATURA", Numeric(18, 2))
    isfaturaagrupada = Column("ISFATURAAGRUPADA", String(1))
    numeronotafiscal = Column("NUMERONOTAFISCAL", String(20))
    qtdarquivosxml = Column("QTDARQUIVOSXML", Integer)
    qtdarquivosdanfe = Column("QTDARQUIVOSDANFE", Integer)
    qtdarquivosboleto = Column("QTDARQUIVOSBOLETO", Integer)
    qtdarquivosfatura = Column("QTDARQUIVOSFATURA", Integer)
    qtdnotasfiscais = Column("QTDNOTASFISCAIS", Integer)
    qtdboletos = Column("QTDBOLETOS", Integer)
    qtdtituloscontaspagar = Column("QTDTITULOSCONTASPAGAR", Integer)
    valortotalnotasfiscais = Column("VALORTOTALNOTASFISCAIS", Numeric(18, 2))
    valortotalboletos = Column("VALORTOTALBOLETOS", Numeric(18, 2))
    tiposituacaofaturatransmissao = Column("TIPOSITUACAOFATURATRANSMISSAO", String(30))
    tipointegracaoerp = Column("TIPOINTEGRACAOERP", String(30))
    codigotipodobranca = Column("CODIGOTIPODOBRANCA", String(10))
    codigotipopagamento = Column("CODIGOTIPOPAGAMENTO", String(10))
    codigofornecedorcontacorrente = Column("CODIGOFORNECEDORCONTACORRENTE", String(30))


class RsmTustTransmissora(Base):
    __tablename__ = "RSM_TUSTTRANSMISSORA"

    id_transmissora = Column(
        "ID_TRANSMISSORA", Integer, primary_key=True, autoincrement=True
    )
    datainclusao = Column("DATAINCLUSAO", DateTime)
    dataalteracao = Column("DATAALTERACAO", DateTime)
    usuarioalteracao = Column("USUARIOALTERACAO", String(30))
    inativo = Column("INATIVO", String(1))
    excluido = Column("EXCLUIDO", String(1))
    dataexclusao = Column("DATAEXCLUSAO", DateTime)
    identificador = Column("IDENTIFICADOR", Integer)
    codigoons = Column("CODIGOONS", String(10))
    nome = Column("NOME", String(100))
    identificadorprocessoimportacao = Column("IDENTIFICADORPROCESSOIMPORTACAO", Integer)
    formapagamento = Column("FORMAPAGAMENTO", String(30))
    isemitenotafiscal = Column("ISEMITENOTAFISCAL", String(1))
    ispossuiimpostoretido = Column("ISPOSSUIIMPOSTORETIDO", String(1))
    codigofornecedor = Column("CODIGOFORNECEDOR", String(20))
    codigotipodobranca = Column("CODIGOTIPODOBRANCA", String(10))
    codigotipopagamento = Column("CODIGOTIPOPAGAMENTO", String(10))
    codigofornecedorcontacorrente = Column("CODIGOFORNECEDORCONTACORRENTE", String(10))
    cnpj = Column("CNPJ", String(20))
    razaosocial = Column("RAZAOSOCIAL", String(100))
    inscricaoestadual = Column("INSCRICAOESTADUAL", String(30))
    classificacaoempresa = Column("CLASSIFICACAOEMPRESA", String(20))
    regiao = Column("REGIAO", String(20))
    nomebanco = Column("NOMEBANCO", String(50))
    numerobanco = Column("NUMEROBANCO", String(10))
    agencia = Column("AGENCIA", String(10))
    conta = Column("CONTA", String(20))
    formaencaminhamentofaturas = Column("FORMAENCAMINHAMENTOFATURAS", String(30))
    urlsite = Column("URLSITE", String(200))
    percentualaliquotapiscofins = Column("PERCENTUALALIQUOTAPISCOFINS", Numeric(10, 2))
    codigoconcessao = Column("CODIGOCONCESSAO", String(20))
    dataconcessao = Column("DATACONCESSAO", DateTime)
    codigocontrato = Column("CODIGOCONTRATO", String(30))
    datainiciocontabil = Column("DATAINICIOCONTABIL", DateTime)
    datainiciooperacao = Column("DATAINICIOOPERACAO", DateTime)
    endereco_cep = Column("ENDERECO_CEP", String(10))
    endereco_logradouro = Column("ENDERECO_LOGRADOURO", String(100))
    endereco_numero = Column("ENDERECO_NUMERO", String(20))
    endereco_complemento = Column("ENDERECO_COMPLEMENTO", String(100))
    endereco_bairro = Column("ENDERECO_BAIRRO", String(50))
    endereco_cidade = Column("ENDERECO_CIDADE", String(50))
    endereco_estado = Column("ENDERECO_ESTADO", String(2))


class RsmTustEmpresa(Base):
    __tablename__ = "RSM_TUSTEMPRESA"

    id_empresatust = Column(
        "ID_EMPRESATUST", Integer, primary_key=True, autoincrement=True
    )
    datainclusao = Column("DATAINCLUSAO", DateTime)
    usuarioinclusao = Column("USUARIOINCLUSAO", String(30))
    dataalteracao = Column("DATAALTERACAO", DateTime)
    usuarioalteracao = Column("USUARIOALTERACAO", String(30))
    inativo = Column("INATIVO", String(1))
    excluido = Column("EXCLUIDO", String(1))
    dataexclusao = Column("DATAEXCLUSAO", DateTime)
    identificador = Column("IDENTIFICADOR", Integer)
    codigoempresa = Column("CODIGOEMPRESA", String(10))
    codigogrupopagamento = Column("CODIGOGRUPOPAGAMENTO", String(20))
    codigocentrocusto = Column("CODIGOCENTROCUSTO", String(20))
    codigoprojetocontabil = Column("CODIGOPROJETOCONTABIL", String(20))


class RsmTustEmpresaFilial(Base):
    __tablename__ = "RSM_TUSTEMPRESAFILIAL"

    id_empresafilialtust = Column(
        "ID_EMPRESAFILIALTUST", Integer, primary_key=True, autoincrement=True
    )
    identificador = Column("IDENTIFICADOR", Integer)
    identificadorempresatust = Column("IDENTIFICADOREMPRESATUST", Integer)
    codigofilial = Column("CODIGOFILIAL", String(10))
    codigoons = Column("CODIGOONS", String(10))


class RsmTustAvisoDebito(Base):
    __tablename__ = "RSM_TUSTAVISODEBITO"

    id_avisodebito = Column(
        "ID_AVISODEBITO", Integer, primary_key=True, autoincrement=True
    )
    identificador = Column("IDENTIFICADOR", Integer)
    codigoempresa = Column("CODIGOEMPRESA", String(10))
    codigofilial = Column("CODIGOFILIAL", String(10))
    codigoons = Column("CODIGOONS", String(10))
    nomeempresa = Column("NOMEEMPRESA", String(100))
    numeroavd = Column("NUMEROAVD", String(20))
    datacompetencia = Column("DATACOMPETENCIA", DateTime)
    datavencimentoparcela1 = Column("DATAVENCIMENTOPARCELA1", DateTime)
    datavencimentoparcela2 = Column("DATAVENCIMENTOPARCELA2", DateTime)
    datavencimentoparcela3 = Column("DATAVENCIMENTOPARCELA3", DateTime)


class RsmTustAvisoDebitoItem(Base):
    __tablename__ = "RSM_TUSTAVISODEBITOITEM"

    id_avisodebitoitem = Column(
        "ID_AVISODEBITOITEM", Integer, primary_key=True, autoincrement=True
    )
    identificador = Column("IDENTIFICADOR", Integer)
    identificadoravisodebitotransmissao = Column(
        "IDENTIFICADORAVISODEBITOTRANSMISSAO", Integer
    )
    codigoons = Column("CODIGOONS", String(10))
    nometransmissora = Column("NOMETRANSMISSORA", String(100))
    cnpjtransmissora = Column("CNPJTRANSMISSORA", String(20))
    percentual_rede_basica = Column("PERCENTUALREDEBASICA", Numeric(10, 2))
    valor_rede_basica = Column("VALORREDEBASICA", Numeric(18, 2))
    valorparcela1 = Column("VALORPARCELA1", Numeric(18, 2))
    valorparcela2 = Column("VALORPARCELA2", Numeric(18, 2))
    valorparcela3 = Column("VALORPARCELA3", Numeric(18, 2))
    valortotal = Column("VALORTOTAL", Numeric(18, 2))


class RsmTustFaturaTransmissao(Base):
    __tablename__ = "RSM_TUSTFATURATRANSMISSAO"

    id_faturatransmissao = Column(
        "ID_FATURATRANSMISSAO", Integer, primary_key=True, autoincrement=True
    )
    datainclusao = Column("DATAINCLUSAO", DateTime)
    dataalteracao = Column("DATAALTERACAO", DateTime)
    inativo = Column("INATIVO", String(1))
    excluido = Column("EXCLUIDO", String(1))
    dataexclusao = Column("DATAEXCLUSAO", DateTime)
    identificador = Column("IDENTIFICADOR", Integer)
    identificadoravisodebitotransmissao = Column(
        "IDENTIFICADORAVISODEBITOTRANSMISSAO", Integer
    )
    identificadoravisodebitotransmissaoitem = Column(
        "IDENTIFICADORAVISODEBITOTRANSMISSAOITEM", Integer
    )
    identificadortransmissora = Column("IDENTIFICADORTRANSMISSORA", Integer)
    identificadorfaturatransmissaopai = Column("IDENTIFICADORFATURATRANSMISSAOPAI", Integer)
    formapagamento = Column("FORMAPAGAMENTO", String(30))
    codigotransmissoraons = Column("CODIGOTRANSMISSORAONS", String(10))
    codigoempresaons = Column("CODIGOEMPRESAONS", String(10))
    codigoempresa = Column("CODIGOEMPRESA", String(10))
    codigofilial = Column("CODIGOFILIAL", String(10))
    datacompetencia = Column("DATACOMPETENCIA", DateTime)
    datafatura = Column("DATAFATURA", DateTime)
    datavencimento = Column("DATAVENCIMENTO", DateTime)
    valorons = Column("VALORONS", Numeric(18, 2))
    valorfatura = Column("VALORFATURA", Numeric(18, 2))
    isfaturaagrupada = Column("ISFATURAAGRUPADA", String(1))
    numeronotafiscal = Column("NUMERONOTAFISCAL", String(20))
    qtdarquivosxml = Column("QTDARQUIVOSXML", Integer)
    qtdarquivosdanfe = Column("QTDARQUIVOSDANFE", Integer)
    qtdarquivosboleto = Column("QTDARQUIVOSBOLETO", Integer)
    qtdarquivosfatura = Column("QTDARQUIVOSFATURA", Integer)
    qtdnotasfiscais = Column("QTDNOTASFISCAIS", Integer)
    qtdboletos = Column("QTDBOLETOS", Integer)
    qtdtituloscontaspagar = Column("QTDTITULOSCONTASPAGAR", Integer)
    valortotalnotasfiscais = Column("VALORTOTALNOTASFISCAIS", Numeric(18, 2))
    valortotalboletos = Column("VALORTOTALBOLETOS", Numeric(18, 2))
    tiposituacaofaturatransmissao = Column("TIPOSITUACAOFATURATRANSMISSAO", String(30))
    tipointegracaoerp = Column("TIPOINTEGRACAOERP", String(30))
    codigotipodobranca = Column("CODIGOTIPODOBRANCA", String(10))
    codigotipopagamento = Column("CODIGOTIPOPAGAMENTO", String(10))
    codigofornecedorcontacorrente = Column("CODIGOFORNECEDORCONTACORRENTE", String(10))


class RsmTustFatTransmissaoArquivo(Base):
    __tablename__ = "RSM_TUSTFATTRANSMISSAOARQUIVO"

    id_faturatransmissaoarquivo = Column(
        "ID_FATURATRANSMISSAOARQUIVO", Integer, primary_key=True, autoincrement=True
    )
    datainclusao = Column("DATAINCLUSAO", DateTime)
    dataalteracao = Column("DATAALTERACAO", DateTime)
    inativo = Column("INATIVO", String(1))
    excluido = Column("EXCLUIDO", String(1))
    dataexclusao = Column("DATAEXCLUSAO", DateTime)
    identificador = Column("IDENTIFICADOR", Integer)
    id_faturatransmissao = Column("ID_FATURATRANSMISSAO", Integer)
    id_arquivo = Column("ID_ARQUIVO", String(50))
    tp_arquivo = Column("TP_ARQUIVO", String(20))
    nomearquivo = Column("NOMEARQUIVO", String(100))
    iscancelado = Column("ISCANCELADO", String(1))
    datacancelamento = Column("DATACANCELAMENTO", DateTime)


class RsmTustFatTransmissaoBoleto(Base):
    __tablename__ = "RSM_TUSTFATTRANSMISSAOBOLETO"

    id_faturatransmissaoboleto = Column(
        "ID_FATURATRANSMISSAOBOLETO", Integer, primary_key=True, autoincrement=True
    )
    datainclusao = Column("DATAINCLUSAO", DateTime)
    dataalteracao = Column("DATAALTERACAO", DateTime)
    inativo = Column("INATIVO", String(1))
    excluido = Column("EXCLUIDO", String(1))
    dataexclusao = Column("DATAEXCLUSAO", DateTime)
    cnpj_beneficiario = Column("CNPJ_BENEFICIARIO", String(20))
    cnpj_pagador = Column("CNPJ_PAGADOR", String(20))
    datadocumento = Column("DATADOCUMENTO", DateTime)
    datavencimento = Column("DATAVENCIMENTO", DateTime)
    valortotal = Column("VALORTOTAL", Numeric(18, 2))
    linhadigitavel = Column("LINHADIGITAVEL", String(60))
    iscancelado = Column("ISCANCELADO", String(1))
    datacancelamento = Column("DATACANCELAMENTO", DateTime)
    identificador = Column("IDENTIFICADOR", Integer)
    identificadorfaturatransmissao = Column("IDENTIFICADORFATURATRANSMISSAO", Integer)
    identificadorarquivo = Column("IDENTIFICADORARQUIVO", String(50))


class RsmTustFatTransmissaoNf(Base):
    __tablename__ = "RSM_TUSTFATTRANSMISSAONF"

    id_faturatransmissaonf = Column(
        "ID_FATURATRANSMISSAONF", Integer, primary_key=True, autoincrement=True
    )
    datainclusao = Column("DATAINCLUSAO", DateTime)
    dataalteracao = Column("DATAALTERACAO", DateTime)
    inativo = Column("INATIVO", String(1))
    excluido = Column("EXCLUIDO", String(1))
    dataexclusao = Column("DATAEXCLUSAO", DateTime)
    identificador = Column("IDENTIFICADOR", Integer)
    identificadorfaturatransmissao = Column("IDENTIFICADORFATURATRANSMISSAO", Integer)
    identificadorarquivo = Column("IDENTIFICADORARQUIVO", String(50))
    cnpj_emissor = Column("CNPJ_EMISSOR", String(20))
    nome_emissor = Column("NOME_EMISSOR", String(100))
    cnpj_destinatario = Column("CNPJ_DESTINATARIO", String(20))
    nome_destinatario = Column("NOME_DESTINATARIO", String(100))
    numeronotafiscal = Column("NUMERONOTAFISCAL", String(20))
    numerofatura = Column("NUMEROFATURA", String(20))
    dataemissao = Column("DATAEMISSAO", DateTime)
    datavencimento = Column("DATAVENCIMENTO", DateTime)
    valortotal = Column("VALORTOTAL", Numeric(18, 2))
    chavenfe = Column("CHAVENFE", String(50))
    iscancelado = Column("ISCANCELADO", String(1))
    datacancelamento = Column("DATACANCELAMENTO", DateTime)


class RsmTustFatTransmissaoTitCp(Base):
    __tablename__ = "RSM_TUSTFATTRANSMISSAOTITCP"

    id_faturatransmissaotitcp = Column(
        "ID_FATURATRANSMISSAOTITCP", Integer, primary_key=True, autoincrement=True
    )
    datainclusao = Column("DATAINCLUSAO", DateTime)
    dataalteracao = Column("DATAALTERACAO", DateTime)
    inativo = Column("INATIVO", String(1))
    excluido = Column("EXCLUIDO", String(1))
    dataexclusao = Column("DATAEXCLUSAO", DateTime)
    identificador = Column("IDENTIFICADOR", Integer)
    identificadorfaturatransmissao = Column("IDENTIFICADORFATURATRANSMISSAO", Integer)
    sequencial = Column("SEQUENCIAL", Integer)
    codigofornecedor = Column("CODIGOFORNECEDOR", String(20))
    numerotitulo = Column("NUMEROTITULO", String(50))
    codigoempresa = Column("CODIGOEMPRESA", String(10))
    codigofilial = Column("CODIGOFILIAL", String(10))
    codigotipotitulo = Column("CODIGOTIPOTITULO", String(10))
    dataemissao = Column("DATAEMISSAO", DateTime)
    dataentrada = Column("DATAENTRADA", DateTime)
    datavencimento = Column("DATAVENCIMENTO", DateTime)
    dataprogramacaopagamento = Column("DATAPROGRAMACAOPAGAMENTO", DateTime)
    datacompetencia = Column("DATACOMPETENCIA", DateTime)
    valortitulo = Column("VALORTITULO", Numeric(18, 2))
    valorcorrigido = Column("VALORCORRIGIDO", Numeric(18, 2))
    codigomoeda = Column("CODIGOMOEDA", String(5))
    codigotipocobranca = Column("CODIGOTIPOCOBRANCA", String(10))
    codigotipopagamento = Column("CODIGOTIPOPAGAMENTO", String(10))
    codigosistema = Column("CODIGOSISTEMA", String(10))
    idportador = Column("IDPORTADOR", String(50))
    codigogrupopagamento = Column("CODIGOGRUPOPAGAMENTO", String(20))
    codigocentrocusto = Column("CODIGOCENTROCUSTO", String(20))
    codigoprojeto = Column("CODIGOPROJETO", String(30))
    iscancelado = Column("ISCANCELADO", String(1))
    datacancelamento = Column("DATACANCELAMENTO", DateTime)


class RsmTustAnexo(Base):
    __tablename__ = "RSM_TUSTANEXO"

    id_anexo = Column("ID_ANEXO", Integer, primary_key=True, autoincrement=True)
    identificador = Column("IDENTIFICADOR", Integer)
    identificadorarquivo = Column("IDENTIFICADORARQUIVO", String(50))
    model = Column("MODEL", String(50))
    foreignkey = Column("FOREIGNKEY", Integer)
    filename = Column("FILENAME", String(200))
    size = Column("SIZE", Integer)


def create_sqlite_engine(path: str = "sqlite:///tust.db", echo: bool = False):
    """Convenience factory para montar um engine SQLite pronto para `Base.metadata.create_all`."""
    from sqlalchemy import create_engine

    return create_engine(path, echo=echo)


__all__ = [
    "Base",
    "RsmTustProcessoImportacao",
    "RsmTustImpAutomatica",
    "RsmTustImpAutExecucao",
    "RsmTustImpAutDocumento",
    "RsmTustTransmissora",
    "RsmTustEmpresa",
    "RsmTustEmpresaFilial",
    "RsmTustAvisoDebito",
    "RsmTustAvisoDebitoItem",
    "RsmTustFaturaTransmissao",
    "RsmTustFatTransmissaoArquivo",
    "RsmTustFatTransmissaoBoleto",
    "RsmTustFatTransmissaoNf",
    "RsmTustFatTransmissaoTitCp",
    "RsmTustAnexo",
    "create_sqlite_engine",
]
