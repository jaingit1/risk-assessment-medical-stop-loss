# Use the official Python 3.9 image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container at /app
COPY app.py .
COPY risk_assessment_model_pipeline.pkl .

# Expose the port that the Flask app runs on
# Make port 80 available to the world outside this container
EXPOSE 80
EXPOSE 5000

# Define the command to run the Flask app
CMD ["python", "app.py"]