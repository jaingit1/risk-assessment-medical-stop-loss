from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# Load the trained model
model = joblib.load('risk_assessment_model_pipeline.pkl') # for running locall use path to pickle fiule as /contaner/risk_assessment_model_pipeline.pkl

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        print("Received data:", data)  # Debugging statement

        # Convert the input data to a DataFrame
        input_data = pd.DataFrame(data["data"])
        print("Input DataFrame:", input_data)  # Debugging statement

        # Perform prediction
        prediction = model.predict(input_data)
        result = {"prediction": prediction.tolist()}
        return jsonify(result)
    except Exception as e:
        print("Error:", e)  # Debugging statement
        return str(e), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)