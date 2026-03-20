#for field_validator we check for eg if the email belongs to an employ of ICICI or HDFC bank or not!
#field validator works in two modes:- 1. before mode 2. after mode 
#by default the mode is after only like here @field_validator('email')
#in before mode the data is passed to field_validator before type coerse that means before, pydantic thinks that this particular value must be in int and not in str and converts the value, the original value is passed to the field_validator! this is useful when u don't want to trust the pydantic for handling the type of every value 

# STEP 1 build pydantic model

from pydantic import BaseModel, EmailStr, Field # field functions are not only for data validation but also for attaching the meta data with combination with Annotated!
from pydantic import field_validator
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):


    name : str
    email : EmailStr
    age : int
    weight : Annotated[float, Field(default=None, gt=0, strict=True)]
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

#STEP2 making object of pydantic class

patient_info = {'name':"rajat", 'email':"abc@icici.com",'age': 24, "married": True , 'patient_allergies': ["pollen", "dust"], 'patient_contacts': { 'phone': "123"}}

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
    print("updated")


update_patient_info(patient_1)

