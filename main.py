from fastapi import FastAPI, Path, HTTPException, Query
import json
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal
from fastapi.responses import JSONResponse

app = FastAPI()

class Patient(BaseModel):

    id : Annotated[str,Field(..., description="Id of the patient", examples=["P001"])] 
    name : Annotated[str, Field(..., description="name of the patient")]
    age : Annotated[int, Field(..., gt=0, lt=120, description="age of the patient")] 
    city : Annotated[str, Field(..., description="city of the patient", examples=["bremen"])]
    gender : Annotated[Literal['male', 'female', 'others'], Field(..., description="gender of the patient", examples=['male'])]
    height : Annotated[float, Field(..., gt=0, description="height of the patient in mtr")]
    weight : Annotated[float, Field(..., gt=0, lt=200, description="weight of the patient in kgs")]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi

    @computed_field
    @property
    def verdict (self) -> str:
        if self.bmi<18.5:
            return "Underweight"
        elif self.bmi< 25:
            return "Normal"
        elif self.bmi < 30:
            return "Overweight"
        else:
            return "Obese"

def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)
        return data

def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f)

@app.get("/")

def hello():
    return({'message': "Patients Report API System!"})

@app.get("/about")
def about():
    return ({'message': "A functional API to manage the Patients Records!"})

@app.get("/view")
def view():
    data = load_data()
    return data

@app.get("/patient/{patient_id}") #patient_id is a variable 
def view_patient(patient_id: str = Path(..., description= 'ID of the patient in the DB', example= 'P001')):
    # load all the patients
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    else:
        raise HTTPException(status_code= 404, detail= 'Patient ID not found!')
    
@app.get('/sort')
def sort_patients(sort_by: str = Query(..., description= 'Sort on the basis of height, weight or bmi'), order : str = Query('asc', description= 'Sort in ascending or descending order')):

    valid_fields = ['height', 'weight', 'bmi']
    if sort_by not in valid_fields:
        raise HTTPException(status_code= 400, detail= f'Invalid field, select from {valid_fields}')
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code= 400, detail= 'Invalid field, select from asc or desc')
    
    data = load_data()

    sort_order = True if order == 'desc' else False

    sorted_data = sorted(data.values(), key = lambda x: x.get(sort_by,0), reverse= sort_order)

    return sorted_data

@app.post('/create')
def create_patient (patient: Patient):

    #load existing data

    data = load_data()

    #does the given patient id already exist, then raise error

    if patient.id in data:
        raise HTTPException(status_code=400, detail="patient already exists!")

    #new patient is added in the db, as the existing data is in json and the new data will be as pydantic object,so we need to convert the pydantic object into a dictionary 

    data[patient.id] = patient.model_dump(exclude=['id'])

    #save this into json file 

    save_data(data)

    return JSONResponse(status_code=201, content={'message': 'patient created successfully!'})
