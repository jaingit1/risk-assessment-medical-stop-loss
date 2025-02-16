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
Invoke-WebRequest -Uri http://a2272bc632dd4437f97f315bc39623ee-963283982.us-east-1.elb.amazonaws.com/predict -Method Post -Headers $headers -Body $body
