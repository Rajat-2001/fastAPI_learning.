#computed_field is a field whose value is not provided by user but its value is calculated by the other variables!
#example given height and weight by user calculate the BMI based on them!

# STEP 1 build pydantic model

from pydantic import BaseModel, EmailStr, Field # field functions are not only for data validation but also for attaching the meta data with combination with Annotated!
from pydantic import field_validator, model_validator, computed_field
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):


    name : str
    email : EmailStr
    age : int
    weight : Annotated[float, Field(default=None, gt=0, strict=True)]
    height : float
    married : bool
    patient_allergies : List[str]
    patient_contacts : Dict[str,str]

    @field_validator('email') #this is a method in our class
    @classmethod #this tells that the method we made is a class method
    def email_validator (cls, value):
        valid_domains = ['hdfc.com', 'icici.com']
        domain_name = value.split('@')[-1]
        if domain_name not in valid_domains:
            raise ValueError("not a valid domain!")
        return value
    
    @field_validator('name')
    @classmethod
    def transform_name(cls, value):
        return value.upper()
    
    @field_validator('age', mode='before')
    @classmethod
    def validate_age(cls, value):
        if 0<value<100:
            return value
        raise ValueError('age should be in between 0-100!')
    
    @model_validator(mode='after')
    def validate_emergency_contact(cls, model):
        if model.age>60 and 'emergency' not in model.patient_contacts:
            raise ValueError("patients older than 60 must have emergency contact!")
        return model
    
    @computed_field
    @property
    def calculate_bmi (self) -> float:
        bmi = round(self.weight/(self.height ** 2),2)
        return bmi

#STEP2 making object of pydantic class

patient_info = {'name':"rajat",'height':1.8, 'weight': 70, 'email':"abc@icici.com",'age': 64, "married": True , 'patient_allergies': ["pollen", "dust"], 'patient_contacts': { 'phone': "123", 'emergency': "3242342"}}

patient_1 = Patient(**patient_info) #unpacking dictonary validation is also performed here!


#STEP3 pass this object to the function or the code 

def insert_patient_info (patient_1: Patient):
    print(patient_1.name)
    print(patient_1.age)
    print("inserted")

def update_patient_info (patient_1: Patient):
    print(patient_1.name)
    print(patient_1.age)
    print(patient_1.weight)
    print(patient_1.calculate_bmi )
    print("updated")


update_patient_info(patient_1)

