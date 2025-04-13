from fhirclient.models import patient as fhir_patient
from fhirclient.models import observation as fhir_observation
from fhirclient.models import humanname, fhirdate, codeableconcept, coding, quantity


def db_patient_to_fhir(patient_db):
    patient = fhir_patient.Patient()
