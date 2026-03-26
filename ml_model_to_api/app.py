from fastapi import FastAPI
from fastapi.responses import JSONResponse
import pickle
import pandas as pd
from schema.user_input import User_Input
from model.predict import MODEL_VERSION, model, predict_output
from schema.prediction_response import PredictionResponse

app = FastAPI()



#human readable
@app.get('/')
def home():
    return {'message': 'Premium Insurance Prediction API'}

#machine readable
@app.get('/health')
def health_check():
    return {'status': 'ok', 'version': MODEL_VERSION, 'model_loaded': model is not None}

@app.post('/predict/', response_model=PredictionResponse)
def predict_premium(data: User_Input): #this tells what kind of data will be received by the function, here the type of the object is the User_Input, same as the pydantic model, we'll receive the data from the request body, that data will go to the pydantic model, pydantic model will work on it like validation and making computed fields etc and that will be received as data in this function!

    #creating proper input format, row wise, input will be sent in pandas dataframe
    user_input = {'bmi': data.bmi,
                   'age_group': data.age_group,
                   'lifestyle_risk': data.lifestyle_risk,
                   'city_tier': data.city_tier,
                   'income_lpa': data.income_lpa,
                   'occupation': data.occupation}
   
    try:

        prediction = predict_output(user_input) #here we'll receive a list of ouput and we'll require the 0th item of that list
        return JSONResponse(status_code=200, content={'predicted_category': prediction})
    
    except Exception as e:
        return JSONResponse(status_code=500, content=str(e))