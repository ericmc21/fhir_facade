from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Patient(Base):
    __tablename__ = "patient"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    date_of_birth = Column(DateTime)


class HeartRate(Base):
    __tablename__ = "heart_rate"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patient.id"))
    rate = Column(Integer)
    date = Column(DateTime)


class BloodPressure(Base):
    __tablename__ = "blood_pressure"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patient.id"))
    systolic = Column(Float)
    diastolic = Column(Float)
    date = Column(DateTime)
