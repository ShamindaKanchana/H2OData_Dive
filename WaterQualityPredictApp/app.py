from flask import Flask, request, render_template
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import joblib
rf = joblib.load('./Notebook/random_forest_model.pkl')
import joblib
scale_sandard = joblib.load('./Notebook/scaler.pkl')

app = Flask(__name__)


rf= RandomForestClassifier() 
scale_sandard = StandardScaler()           

# Function to predict water potability
def predict_water_potability(input_features):
    features_order = ['ph', 'Hardness', 'Solids', 'Chloramines', 'Sulfate', 
                      'Conductivity', 'Organic_carbon', 'Trihalomethanes', 'Turbidity']
    
    
    input_df = pd.DataFrame([input_features], columns=features_order)
    
    # Scale the input features using the same scaler used during training
    scaled_input = scale_sandard.transform(input_df)
    scaled_input_df = pd.DataFrame(scaled_input, columns=features_order)
    # Predict using the trained Random Forest model
    prediction = rf.predict(scaled_input_df)
    
    # Return whether the water is potable (1) or not (0)
    return 'Portable' if prediction[0] == 1 else 'Not Portable'

# Define a route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# Define a route for form submission
@app.route('/predict', methods=['POST'])
def predict():
    # Extract form data
    features = [
        float(request.form['ph']),
        float(request.form['Hardness']),
        float(request.form['Solids']),
        float(request.form['Chloramines']),
        float(request.form['Sulfate']),
        float(request.form['Conductivity']),
        float(request.form['Organic_carbon']),
        float(request.form['Trihalomethanes']),
        float(request.form['Turbidity'])
    ]
    
    # Predict water potability
    result = predict_water_potability(features)
    #result="THis is the result"
    return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
