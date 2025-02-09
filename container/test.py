'''
'''
import joblib
import pandas as pd

# Load the model pipeline
model_pipeline = joblib.load('risk_assessment_model_pipeline.pkl')

# Example new data for prediction
new_data = pd.DataFrame({
    'Medical Paid': [10000],
    'RX Paid': [15000],
    'Ongoing Treatment': [15],
    'Policy Holder': ['Policy Holder 3000']
})

# Make predictions
predictions = model_pipeline.predict(new_data)
print(predictions)
