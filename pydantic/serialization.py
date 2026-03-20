#how to export our pydantic models objects as python dictionary or json

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

temp = patient_1.model_dump() #converts existing pydantic model obj to python dictionary
# print(temp)
# print(type(temp))

# temp1 = patient_1.model_dump_json() #converts existing pydantic model obj to json
# print(temp1)
# print(type(temp1))

# temp = patient_1.model_dump(include=['name']) #only name field is shown
temp = patient_1.model_dump(exclude=['name', 'address'])
print(temp)
print(type(temp))