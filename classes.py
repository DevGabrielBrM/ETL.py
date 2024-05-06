from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    ForeignKey,
    Float,
    Boolean
)
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class UNIDADE_PRODUCAO(Base):
    __tablename__ = "UNIDADE_PRODUCAO"

    tipo = "UNIDADE_PRODUCAO"
    numero = Column(Integer(), primary_key=True, autoincrement=False)
    peca_hora_nominal = Column(Float(), nullable=False)


class FRESADORA(Base):
    __tablename__ = "FRESADORA"

    tipo = "FRESADORA"
    numero = Column(Integer(), ForeignKey("UNIDADE_PRODUCAO.numero"), primary_key=True, autoincrement=False)
    velocidade_rotacao = Column(Float(), nullable=False)
    profundidade_corte = Column(Float(), nullable=False)


class IMPRESSORA_3D(Base):
    __tablename__ = "IMPRESSORA_3D"

    tipo = "IMPRESSORA_3D"
    numero = Column(Integer(), ForeignKey("UNIDADE_PRODUCAO.numero"), primary_key=True, autoincrement=False)
    espessura_camada = Column(Float(), nullable=False)
    tipo_material = Column(String(), nullable=False)


class SOPRADORA(Base):
    __tablename__ = "SOPRADORA"

    tipo = "SOPRADORA"
    numero = Column(Integer(), ForeignKey("UNIDADE_PRODUCAO.numero"), primary_key=True, autoincrement=False)
    vazao_sopro = Column(Integer(), nullable=False)
    pressao_sopro = Column(Integer(), nullable=False)


class TORNO_CNC(Base):
    __tablename__ = "TORNO_CNC"

    tipo = "TORNO_CNC"
    numero = Column(Integer(), ForeignKey("UNIDADE_PRODUCAO.numero"), primary_key=True, autoincrement=False)
    velocidade_rotacao = Column(Integer(), nullable=False)
    tolerancia = Column(Float(), nullable=False)


class PECA(Base):
    __tablename__ = "PECA"

    tipo = "PECA"
    numero = Column(Integer(), primary_key=True, autoincrement=False)
    inicio_fabricacao = Column(Date(), nullable=False)
    fim_fabricacao = Column(Date(), nullable=False)
    status = Column(String(), nullable=False)
    numero_unidade_producao = Column(Integer(), ForeignKey("UNIDADE_PRODUCAO.numero"), nullable=False, autoincrement=False)


class REGISTRO_FALHA(Base):
    __tablename__ = "REGISTRO_FALHA"

    tipo = "REGISTRO_FALHA"
    id = Column(Integer(), primary_key=True, autoincrement=False)
    inicio = Column(Date(), nullable=False)
    fim = Column(Date(), nullable=False)
    severidade = Column(Boolean(), nullable=False)
    numero_unidade_producao = Column(Integer(), ForeignKey("UNIDADE_PRODUCAO.numero"), nullable=False)
