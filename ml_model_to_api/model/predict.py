import pandas as pd
import pickle

#stp 1: import the ml model

with open('/Users/rajatgoswami/Downloads/fastAPI/ml_model_to_api/model.pkl','rb') as f:
    model = pickle.load(f)

MODEL_VERSION = '1.1.0' #this is a setup model number and this is usually given by a software like MLFlow

#get class labels from model (important for matching probabilities to class names)
class_labels = model.classes_.tolist()

def predict_output(user_input:dict):
    df = pd.DataFrame([user_input])

    predicted_class = model.predict(df)[0]

    probabilies = model.predict_proba(df)[0]
    confidence = max(probabilies)

    #create mapping : {class_name :probabilities}

    class_probs = dict (zip(class_labels,map(lambda p: round(p,4), probabilies)))

    return {'predicted_category' : predicted_class,
            'confidence': round(confidence,4),
            'class_probabilities': class_probs}