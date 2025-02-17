import requests
import json

# Define the API endpoint URL
api_url = 'http://127.0.0.1:5000/predict'

# Read input data from JSON file
with open('./container/input_data.json', 'r') as input_file:
    data = json.load(input_file)

try:
    # Send POST request to the API
    response = requests.post(api_url, headers={'Content-Type': 'application/json'}, data=json.dumps(data))

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        result = response.json()

        # Write the output to a JSON file
        with open('output_data.json', 'w') as output_file:
            json.dump(result, output_file, indent=2)
        
        print("Predictions have been saved to 'output_data.json'.")
    else:
        print(f"Request failed with status code {response.status_code}: {response.text}")

except Exception as e:
    print("Error occurred:", e)
