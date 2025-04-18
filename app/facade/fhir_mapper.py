from fhirclient.models import patient as Patient
from fhirclient.models import humanname as HumanName
from fhirclient.models.codeableconcept import CodeableConcept
from fhirclient.models.coding import Coding
from fhirclient.models.quantity import Quantity
from fhirclient.models.fhirdate import FHIRDate
from fhirclient.models.fhirdatetime import FHIRDateTime
from fhirclient.models.observation import Observation, ObservationComponent
from fhirclient.models.fhirreference import FHIRReference


def db_patient_to_fhir(patient_db):
    patient = Patient.Patient()
    patient.id = str(patient_db.id)
    name = HumanName.HumanName()
    name.given = [patient_db.first_name]
    name.family = patient_db.last_name
    patient.name = [name]
    # patient.gender = patient_db.gender.lower()
    patient.birthDate = FHIRDate(patient_db.date_of_birth.isoformat())
    return patient


def heart_rate_to_observation(hr_db):
    obs = Observation()
    obs.status = "final"

    # Category: vital-signs
    vital_signs_coding = Coding()
    vital_signs_coding.system = (
        "http://terminology.hl7.org/CodeSystem/observation-category"
    )
    vital_signs_coding.code = "vital-signs"
    vital_signs_coding.display = "Vital Signs"

    category = CodeableConcept()
    category.coding = [vital_signs_coding]

    obs.category = [category]

    # Code: Heart Rate
    heart_rate_coding = Coding()
    heart_rate_coding.system = "http://loinc.org"
    heart_rate_coding.code = "8867-4"
    heart_rate_coding.display = "Heart rate"

    obs.code = CodeableConcept()
    obs.code.coding = [heart_rate_coding]

    # Subject
    ref = FHIRReference()
    ref.reference = f"Patient/{hr_db.patient_id}"
    obs.subject = ref

    # Timestamp
    obs.effectiveDateTime = FHIRDateTime(hr_db.date.date().isoformat())

    # Value: Heart rate in bpm
    quantity = Quantity()
    quantity.value = hr_db.rate
    quantity.unit = "beats/minute"
    quantity.system = "http://unitsofmeasure.org"
    quantity.code = "/min"

    obs.valueQuantity = quantity

    return obs


def blood_pressure_to_observation(bp_db):
    obs = Observation()
    obs.status = "final"

    # Category: Vital Signs
    vital_signs_coding = Coding()
    vital_signs_coding.system = (
        "http://terminology.hl7.org/CodeSystem/observation-category"
    )
    vital_signs_coding.code = "vital-signs"
    vital_signs_coding.display = "Vital Signs"

    category = CodeableConcept()
    category.coding = [vital_signs_coding]
    obs.category = [category]

    # Code: Blood pressure panel
    bp_code = Coding()
    bp_code.system = "http://loinc.org"
    bp_code.code = "85354-9"
    bp_code.display = "Blood pressure panel"

    obs.code = CodeableConcept()
    obs.code.coding = [bp_code]

    # Subject reference
    # Subject
    ref = FHIRReference()
    ref.reference = f"Patient/{bp_db.patient_id}"
    obs.subject = ref

    # Timestamp
    obs.effectiveDateTime = FHIRDateTime(bp_db.date.date().isoformat())

    # Systolic Component
    systolic_code = Coding()
    systolic_code.system = "http://loinc.org"
    systolic_code.code = "8480-6"
    systolic_code.display = "Systolic Blood Pressure"

    systolic_component = ObservationComponent()
    systolic_concept = CodeableConcept()
    systolic_concept.coding = [systolic_code]
    systolic_component.code = systolic_concept
    systolic_quantity = Quantity()
    systolic_quantity.value = bp_db.systolic
    systolic_quantity.unit = "mmHg"
    systolic_quantity.system = "http://unitsofmeasure.org"
    systolic_quantity.code = "mm[Hg]"
    systolic_component.valueQuantity = systolic_quantity

    # Diastolic Component
    diastolic_code = Coding()
    diastolic_code.system = "http://loinc.org"
    diastolic_code.code = "8462-4"
    diastolic_code.display = "Diastolic Blood Pressure"

    diastolic_component = ObservationComponent()
    diastolic_concept = CodeableConcept()
    diastolic_concept.coding = [diastolic_code]
    diastolic_component.code = diastolic_concept
    diastolic_quantity = Quantity()
    diastolic_quantity.value = bp_db.diastolic
    diastolic_quantity.unit = "mmHg"
    diastolic_quantity.system = "http://unitsofmeasure.org"
    diastolic_quantity.code = "mm[Hg]"
    diastolic_component.valueQuantity = diastolic_quantity

    # Assign both components to the observation
    obs.component = [systolic_component, diastolic_component]

    return obs
