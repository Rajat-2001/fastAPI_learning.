#how to make an api that will serve the machine learning model in front of the users

#importing the libraries

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import OneHotEncoder
import numpy as np
import pickle

df = pd.read_csv('/Users/rajatgoswami/Downloads/fastAPI/ml_model_to_api/insurance.csv')



#stripping all the blank spaces before the column names 
df.columns = df.columns.str.strip()

df_feat = df.copy() #to copy our dataset coz we'll do a lot of feature engineering 



#feature: 1 -> BMI

df_feat["bmi"] = df_feat["weight"]/ (df_feat["height"]**2)


#Feature:2 -> age group

def age_group(age):
    if age <25:
        return "young"
    elif age <45:
        return "adult"
    elif age <60:
        return "middle_aged"
    else:
        return "senior"
    
df_feat["age_group"] = df_feat["age"].apply(age_group)

#Feature3 : lifestyle risk

def lifestyle_risk(row):
    if row["smoker"] and row["bmi"] >30:
        return "high"
    elif row["smoker"] and row["bmi"] >27:
        return "medium"
    else:
        return "low"
    
df_feat["lifestyle_risk"] = df_feat.apply(lifestyle_risk, axis=1) 

tier_1_cities = ["Mumbai", "Delhi", "Chennai", "Kolkata", "Hyderabad", "Pune"]
tier_2_cities = [
    "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
    "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
    "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
    "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
    "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
    "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"
]

#Feature 4: city tier

def city_tier(city):
    if city in tier_1_cities:
        return 1
    elif city in tier_2_cities:
        return 2
    else:
        return 3

df_feat["city_tier"] = df_feat["city"].apply(city_tier)
df_feat = df_feat.apply(lambda col: col.str.strip() if col.dtype == 'object' else col)


df_feat.drop(columns=['age', 'weight', 'height', 'smoker', 'city'])[['income_lpa', 'occupation', 'bmi', 'age_group', 'lifestyle_risk', 'city_tier']]

#Select features and target

x = df_feat[["bmi", "age_group", "lifestyle_risk", "city_tier", "income_lpa", "occupation"]]
y = df_feat["insurance_premium_category"]

#Define categorical and numeric feature

categorical_features = ["age_group", "lifestyle_risk", "occupation"]
numerica_features = ["bmi", "income_lpa", "city_tier"]

#create colum transformer for OHE

preprocessor = ColumnTransformer(transformers=[("cat",OneHotEncoder(), categorical_features),
                                               ("num", "passthrough", numerica_features)])

#create a pipeline with preprocessing and randon forest classifier

pipline = Pipeline(steps=[("preprocessor", preprocessor),
                          ("classifier", RandomForestClassifier(random_state=42))])

#split data and train model 

x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=0.2, random_state=1)


pipline.fit(x_train, y_train)

#predict and evaluate
y_pred = pipline.predict(x_test)
accuracy_score(y_test, y_pred)

#save the pipline and download the model using pickle

pickle_model_path = "model.pkl"
with open(pickle_model_path, "wb") as f:
    pickle.dump(pipline,f)
