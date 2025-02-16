$headers = @{ 
    "Content-Type" = "application/json"
}

# Define the JSON body
$body = '{
  "data": [
    {
      "Medical Paid": 10000,
      "RX Paid": 15000,
      "Ongoing Treatment": 15,
      "Policy Holder": "Policy Holder 3000"
    }
  ]
}'

# Send the POST request
Invoke-WebRequest -Uri http://localhost:5000/predict -Method Post -Headers $headers -Body $body
