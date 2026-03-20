#if we in pydantic, use a model as a field in another model then it's called nested_model. 
#here in this case the variable address is made up of different data types therefore we make another pydantic model for this!
#this is for :- better organization of related data, reusability, readability and validation

from pydantic import BaseModel

class address(BaseModel):
    city : str
    state : str
    pin : str

class Patient(BaseModel):
    name : str
    gender : str
    age : int 
    address : address

address_dic = {'city': "bremen", 'state': "nothern", 'pin': '234234' }

address_1 = address(**address_dic)

patient_dict = {'name': "rajat", 'gender': "male", 'age': 24, 'address': address_1}

patient_1 = Patient(**patient_dict)

print(patient_1)
print(patient_1.address)