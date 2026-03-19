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
from pydantic import BaseModel

class Patient(BaseModel):
    name : str
    age : int

#STEP2 making object of pydantic class


patient_info = {'name':"rajat", 'age': 24}
patient_1 = Patient(**patient_info) #unpacking dictonary


#STEP3 pass this object to the function or the code 

def insert_patient_info (patient_1: Patient):
    print(patient_1.name)
    print(patient_1.age)
    print("inserted")

def update_patient_info (patient_1: Patient):
    print(patient_1.name)
    print(patient_1.age)
    print("updated")

insert_patient_info(patient_1)
print("****************")
update_patient_info(patient_1)