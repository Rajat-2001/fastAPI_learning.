import pandas as pd
import pickle

#stp 1: import the ml model

with open('/Users/rajatgoswami/Downloads/fastAPI/ml_model_to_api/model.pkl','rb') as f:
    model = pickle.load(f)

MODEL_VERSION = '1.1.0' #this is a setup model number and this is usually given by a software like MLFlow

def predict_output(user_input:dict):
    input_df = pd.DataFrame([user_input])
    prediction =  model.predict(input_df)[0] #here we'll receive a list of ouput and we'll require the 0th item of that list
    return prediction