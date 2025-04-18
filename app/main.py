# main.py

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .db import models
from .db.database import SessionLocal, engine
from .facade import fhir_mapper

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/fhir/Patient/{patient_id}")
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    patient_db = (
        db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    )
    if not patient_db:
        return {"error": "Patient not found"}
    return fhir_mapper.db_patient_to_fhir(patient_db).as_json()


@app.get("/fhir/Observation/heart_rate/{patient_id}")
def get_heart_rate(patient_id: int, db: Session = Depends(get_db)):
    hr_db = (
        db.query(models.HeartRate)
        .filter(models.HeartRate.patient_id == patient_id)
        .order_by(models.HeartRate.date.desc())
        .first()
    )
    if not hr_db:
        return {"error": "Heart rate not found"}
    return fhir_mapper.heart_rate_to_observation(hr_db).as_json()


@app.get("/fhir/Observation/blood_pressure/{patient_id}")
def get_blood_pressure(patient_id: int, db: Session = Depends(get_db)):
    bp_db = (
        db.query(models.BloodPressure)
        .filter(models.BloodPressure.patient_id == patient_id)
        .order_by(models.BloodPressure.date.desc())
        .first()
    )
    if not bp_db:
        return {"error": "Blood pressure not found"}
    return fhir_mapper.blood_pressure_to_observation(bp_db).as_json()
