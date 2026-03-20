# def insert_patients_data (name: str, age: int): this is type hinting 
# this method is not scalable!
# therefore we use the pydantic!
# def insert_patients_data (name: str, age: int):
#     if (type(age)== int and type(name) == str):
#         print (name)
#         print (age)
#         print ("inserted into database!")

# insert_patients_data('rajat', 'twenty four')





# STEP 1 build pydantic model

from pydantic import BaseModel, EmailStr, Field # field functions are not only for data validation but also for attaching the meta data with combination with Annotated!
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):
    # all these fields are required! and not skippable

    name : str = Field(max_length=50) #max len of name is 50 charaters now!
    name : Annotated[str, Field(max_length=50, title="name of the function", description="give the name of the patient", examples=["rajat","yes"])]
    email : EmailStr #this datatype is for the data validation for email! so that it doesn't have gibberish data!
    age : int = Field(gt=0, lt=120) # this is again a data validation, here we have put constraint that no one can set the value of age less than 0 and more than 120!
    weight : Annotated[float, Field(default=None,gt=0, strict=True)] #if this field is missing in input data then there will be no error but we have to give a default value to this fielf as None
    married : bool
    patient_allergies : List[str] #why not to type list and why list[str]? this is for 2 level validation that inside this list the items are string too!
    patient_contacts : Dict[str,str]

#STEP2 making object of pydantic class

patient_info = {'name':"rajat", 'email':"abc@gmail.com",'age': 24, "married": True , 'patient_allergies': ["pollen", "dust"], 'patient_contacts': { 'phone': "123"}}

patient_1 = Patient(**patient_info) #unpacking dictonary


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

