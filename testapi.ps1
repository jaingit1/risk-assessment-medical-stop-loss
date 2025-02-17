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
Invoke-WebRequest -Uri http://a152e179fca314ed59e9ab9909e33fdf-1224658285.us-east-1.elb.amazonaws.com/predict -Method Post -Headers $headers -Body $body
