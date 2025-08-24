from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Solicitud(Base):
    __tablename__ = 'actividades'

    id = Column(Integer, primary_key=True)
    actividad_num = Column(String(20), nullable=False)
    apellido_paterno = Column(String(100), nullable=False)
    apellido_materno = Column(String(100), nullable=True)
    nombres = Column(String(100), nullable=False)
    carrera = Column(String(100), nullable=False)
    semestre = Column(String(1), nullable=False)
    grupo = Column(String(1), nullable=False)
    pdf_url = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)