import streamlit as st
import boto3
import pandas as pd
from io import StringIO
import time

# Initialize S3 client
s3_client = boto3.client('s3')

# Replace with your S3 bucket name
BUCKET_NAME = 'risk-assessment-bucket'

def list_folders():
    """List the timestamped folders in the S3 bucket."""
    response = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix='uploads/', Delimiter='/')
    return [prefix['Prefix'].split('/')[1] for prefix in response.get('CommonPrefixes', [])]

def fetch_results(folder_name):
    """Fetch the aggregated and predicted data stored in the S3 folder."""
    file_key = f"outputs/{folder_name}/results.csv"
    try:
        # Fetch the file from S3
        response = s3_client.get_object(Bucket=BUCKET_NAME, Key=file_key)
        data = response['Body'].read().decode('utf-8')
        
        # Read the data into a Pandas DataFrame
        df = pd.read_csv(StringIO(data))
        return df
    except Exception as e:
        st.error(f"Error fetching results: {str(e)}")
        return None

def upload_files_to_s3(files):
    """Upload files to the S3 bucket in a timestamped folder."""
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    folder_name = f"uploads/{timestamp}"

    # Upload files
    for uploaded_file in files:
        file_path = f"{folder_name}/{uploaded_file.name}"
        s3_client.upload_fileobj(uploaded_file, BUCKET_NAME, file_path)
        st.write(f"Uploaded {uploaded_file.name} to {file_path}")
    
    return folder_name

# def poll_for_results(folder_name, progress_bar):
#     """Poll S3 bucket for the results file until it is available."""
#     results_found = False
#     while not results_found:
#         try:
#             # Check if results file exists
#             s3_client.head_object(Bucket=BUCKET_NAME, Key=f"outputs/{folder_name}/results.csv")
#             results_found = True
#         except s3_client.exceptions.ClientError:
#             progress_bar.progress(50)  # Polling in progress
#             st.write("Results not yet available. Waiting for completion...")
#             time.sleep(10)  # Polling delay (10 seconds)
#             progress_bar.progress(75)  # Update progress bar as polling continues
#     return True

def main():
    # Streamlit UI
    st.title("Risk Assessment Results")

    # File Upload UI
    uploaded_files = st.file_uploader("Choose files to upload", accept_multiple_files=True)
    
    # if uploaded_files:
    #     # Upload the files to S3 in a timestamped folder
    #     # folder_name = upload_files_to_s3(uploaded_files)
    #     # st.write(f"Files uploaded to folder: {folder_name}")
    #     st.write("Triggering Lambda to start Step Functions execution...")

    #     # Inform the user to wait for results to be processed and stored in S3
    #     st.write("Waiting for processing to complete. Please refresh to view results.")


    #     # Polling to check if the results are available in the S3 output folder
    #     if poll_for_results():
    #         # Once results are available, fetch and display the results from the selected folder
    #         st.write("### Processed Results")

    #     # Automatically refresh the app after polling
    #     st.rerun()

if __name__ == "__main__":
    main()
