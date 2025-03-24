from sqlalchemy import Column, Integer, Numeric, Text, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class SensorNodoGeneral(Base):
    __tablename__ = "sensor_nodo_general"
    id = Column(Integer, primary_key=True)
    timestamp = Column(TIMESTAMP(timezone=True), server_default=func.now())
    humedad = Column(Numeric)
    temperatura = Column(Numeric)
    lluvia = Column(Integer)
    sol = Column(Integer)


class Parcela(Base):
    __tablename__ = "parcelas"
    id = Column(Integer, primary_key=True)
    parcela_id = Column(Integer, unique=True, index=True)
    nombre = Column(Text)
    ubicacion = Column(Text)
    responsable = Column(Text)
    tipo_cultivo = Column(Text)
    latitud = Column(Numeric)
    longitud = Column(Numeric)


class SensorParcelaHistorico(Base):
    __tablename__ = "sensor_parcela_historico"
    id = Column(Integer, primary_key=True)
    timestamp = Column(TIMESTAMP(timezone=True), server_default=func.now())
    parcela_id = Column(Integer, ForeignKey("parcelas.parcela_id"))
    humedad = Column(Numeric)
    temperatura = Column(Numeric)
    lluvia = Column(Integer)
    sol = Column(Integer)
    ultimo_riego = Column(TIMESTAMP(timezone=True))
