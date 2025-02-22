import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import json

# Utility function to generate random dates
def random_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))

# Set seeds for reproducibility
np.random.seed(42)
random.seed(42)

# Number of records
num_records = 2000
num_policy_holders = 500

# List of valid ICD-10 codes and descriptions
icd10_codes = [
    {'Code': 'E11.9', 'Description': 'Type 2 diabetes mellitus without complications'},
    {'Code': 'I10', 'Description': 'Essential (primary) hypertension'},
    {'Code': 'J45.909', 'Description': 'Unspecified asthma, uncomplicated'},
    {'Code': 'M54.5', 'Description': 'Low back pain'},
    {'Code': 'R51', 'Description': 'Headache'},
    {'Code': 'K21.9', 'Description': 'Gastro-esophageal reflux disease without esophagitis'},
    {'Code': 'N39.0', 'Description': 'Urinary tract infection, site not specified'},
    {'Code': 'F32.9', 'Description': 'Major depressive disorder, single episode, unspecified'},
    {'Code': 'I25.10', 'Description': 'Atherosclerotic heart disease of native coronary artery without angina pectoris'},
    {'Code': 'C34.90', 'Description': 'Malignant neoplasm of unspecified part of unspecified bronchus or lung'},
    {'Code': 'C50.911', 'Description': 'Malignant neoplasm of unspecified site of right female breast'},
    {'Code': 'C61', 'Description': 'Malignant neoplasm of prostate'},
    {'Code': 'C18.9', 'Description': 'Malignant neoplasm of colon, unspecified'},
    {'Code': 'C20', 'Description': 'Malignant neoplasm of rectum'},
    {'Code': 'C92.00', 'Description': 'Acute myeloid leukemia, not having achieved remission'},
]

# List of valid CPT/HCPCS codes and descriptions
cpt_codes = [
    {'Code': '99213', 'Description': 'Office or other outpatient visit for the evaluation and management of an established patient'},
    {'Code': '93000', 'Description': 'Electrocardiogram, routine ECG with at least 12 leads'},
    {'Code': '90471', 'Description': 'Immunization administration (single vaccine)'},
    {'Code': '81002', 'Description': 'Urinalysis, automated, without microscopy'},
    {'Code': '86580', 'Description': 'Skin test; tuberculosis, intradermal'},
]

# Generate Basic Claimant Data
def generate_claimant_data(num_claimants):
    data = []
    for i in range(1, num_claimants + 1):
        policy_holder = f'Policy Holder {i % num_policy_holders}'
        claimant_dob = random_date(datetime(1950, 1, 1), datetime(2003, 1, 1))
        effective_date = datetime(2024, 1, 1)
        term_date = datetime(2024, 12, 31)

        row = {
            'ID': i,
            'Claimant Name': f'Claimant {i}',
            'Claimant DOB': claimant_dob,
            'Relationship': np.random.choice(['EE', 'SPS', 'CHILD']),
            'Policy Holder': policy_holder,
            'Effective Date': effective_date,
            'Term Date': term_date,
        }
        data.append(row)
    return pd.DataFrame(data)

# Split Claimant Data into Categories
def split_claimants(df, proportions):
    num_claimants = len(df)
    indices = np.arange(num_claimants)
    np.random.shuffle(indices)
    
    laser_size = int(num_claimants * proportions['Laser'])
    high_risk_size = int(num_claimants * proportions['High Risk'])
    cleared_size = num_claimants - laser_size - high_risk_size
    
    laser_indices = indices[:laser_size]
    high_risk_indices = indices[laser_size:laser_size + high_risk_size]
    cleared_indices = indices[laser_size + high_risk_size:]
    
    df_laser = df.iloc[laser_indices]
    df_high_risk = df.iloc[high_risk_indices]
    df_cleared = df.iloc[cleared_indices]
    
    return df_laser, df_high_risk, df_cleared

# Generate Trigger Report Data
def generate_trigger_reports(df_main):
    trigger_records = []
    for idx, row in df_main.iterrows():
        num_triggers = random.randint(1, 3)
        for _ in range(num_triggers):
            trigger_date = random_date(row['Effective Date'], row['Term Date'])
            trigger_type = np.random.choice(['High blood sugar', 'ER visit', 'Hospitalization'])
            trigger_records.append({
                'ID': row['ID'],
                'Trigger Event ID': f'TR{random.randint(1000, 9999)}',
                'Trigger Date': trigger_date,
                'Trigger Type': trigger_type
            })
    return pd.DataFrame(trigger_records)

# Generate Visits for Category
def generate_visits(df_main, df_trigger, visit_type, category):
    visits = []
    for idx, row in df_main.iterrows():
        claimant_triggers = df_trigger[df_trigger['ID'] == row['ID']]
        for _, trigger_row in claimant_triggers.iterrows():
            num_visits = random.randint(1, 3)
            for _ in range(num_visits):
                visit_date = trigger_row['Trigger Date'] + timedelta(days=random.randint(0, 10))
                icd10 = random.choice(icd10_codes)
                if visit_type == 'Inpatient':
                    if category == 'Laser':
                        length_of_stay = np.random.choice([5, 7, 10])
                        billed = round(np.random.uniform(15000, 30000), 2)
                    elif category == 'High Risk':
                        length_of_stay = np.random.choice([3, 5, 7])
                        billed = round(np.random.uniform(8000, 15000), 2)
                    else:  # Cleared - No Risk
                        length_of_stay = np.random.choice([1, 2, 3])
                        billed = round(np.random.uniform(3000, 8000), 2)
                    paid = round(billed * np.random.uniform(0.6, 0.9), 2)
                    visits.append({
                        'ID': row['ID'],
                        'Visit ID': f'IP{random.randint(1000,9999)}',
                        'Visit Date': visit_date,
                        'Length of Stay': length_of_stay,
                        'Provider': np.random.choice(['Hospital A', 'Hospital B', 'Hospital C']),
                        'ICD10 Code': icd10['Code'],
                        'ICD10 Description': icd10['Description'],
                        'Billed': billed,
                        'Paid': paid
                    })
                elif visit_type == 'Outpatient':
                    if category == 'Laser':
                        billed = round(np.random.uniform(1000, 1500), 2)
                    elif category == 'High Risk':
                        billed = round(np.random.uniform(2000, 4000), 2)
                    else:  # Cleared - No Risk
                        billed = round(np.random.uniform(1000, 2000), 2)
                    paid = round(billed * np.random.uniform(0.6, 0.9), 2)
                    cpt = random.choice(cpt_codes)
                    visits.append({
                        'ID': row['ID'],
                        'Visit ID': f'OP{random.randint(1000,9999)}',
                        'Visit Date': visit_date,
                        'Treatment Type': np.random.choice(['Therapy', 'Consultation', 'Minor Procedure']),
                        'Provider': np.random.choice(['Clinic A', 'Clinic B', 'Clinic C']),
                        'CPT Code': cpt['Code'],
                        'CPT Description': cpt['Description'],
                        'ICD10 Code': icd10['Code'],
                        'ICD10 Description': icd10['Description'],
                        'Billed': billed,
                        'Paid': paid
                    })
    return pd.DataFrame(visits)

# Generate Medical and RX Claims (continuation)
def generate_medical_rx_claims(df_main):
    claims = []
    for idx, row in df_main.iterrows():
        num_claims = random.randint(2, 5)
        for _ in range(num_claims):
            service_date = random_date(row['Effective Date'], row['Term Date'])
            rx_claim = np.random.choice([True, False])
            if rx_claim:
                rx_name = np.random.choice(['Lipitor', 'Amoxicillin', 'Metformin'])
                quantity = np.random.choice([30, 60, 90])
                billed = round(quantity * np.random.choice([10, 20, 30]), 2)
                paid = round(billed * np.random.uniform(0.6, 0.9), 2)
                claims.append({
                    'ID': row['ID'],
                    'Claim ID': f'CL{random.randint(1000,9999)}',
                    'Service Date': service_date,
                    'RX Name': rx_name,
                    'Quantity': quantity,
                    'Provider': '',  # Not applicable
                    'Billed': billed,
                    'Paid': paid,
                    'Claim Type': 'RX',
                })
            else:
                provider = np.random.choice(['Provider A', 'Provider B', 'Provider C'])
                billed = round(np.random.uniform(1000, 5000), 2)
                paid = round(billed * np.random.uniform(0.6, 0.9), 2)
                icd10 = random.choice(icd10_codes)
                claims.append({
                    'ID': row['ID'],
                    'Claim ID': f'CL{random.randint(1000,9999)}',
                    'Service Date': service_date,
                    'Provider': provider,
                    'ICD10 Code': icd10['Code'],
                    'ICD10 Description': icd10['Description'],
                    'Billed': billed,
                    'Paid': paid,
                    'Claim Type': 'Medical',
                })
    return pd.DataFrame(claims)

# Generate Case Management Data
def generate_case_management(df_main):
    case_mgmt_records = []
    for idx, row in df_main.iterrows():
        num_cases = random.randint(1, 2)  # Each claimant can have 1 to 2 case management records
        for _ in range(num_cases):
            case_start = random_date(row['Effective Date'], row['Term Date'])
            intervention_type = np.random.choice(['Medication Review', 'Lifestyle Coaching', 'Regular Check-ups'])
            ongoing_treatment = np.random.choice([True, False], p=[0.7, 0.3])
            case_mgmt_records.append({
                'ID': row['ID'],
                'Case Management ID': f'CM{random.randint(1000,9999)}',
                'Case Start Date': case_start,
                'Intervention Type': intervention_type,
                'Ongoing Treatment': ongoing_treatment
            })
    return pd.DataFrame(case_mgmt_records)

# Generate Data for Claimants
df_claimants = generate_claimant_data(num_records)

# Split Claimants into Categories
proportions = {'Laser': 0.33, 'High Risk': 0.33, 'Cleared - No Risk': 0.34}
df_laser, df_high_risk, df_cleared = split_claimants(df_claimants, proportions)

# Generate Related Datasets for Each Category
df_trigger_laser = generate_trigger_reports(df_laser)
df_inpatient_visits_laser = generate_visits(df_laser, df_trigger_laser, 'Inpatient', 'Laser')
df_outpatient_visits_laser = generate_visits(df_laser, df_trigger_laser, 'Outpatient', 'Laser')

df_trigger_high_risk = generate_trigger_reports(df_high_risk)
df_inpatient_visits_high_risk = generate_visits(df_high_risk, df_trigger_high_risk, 'Inpatient', 'High Risk')
df_outpatient_visits_high_risk = generate_visits(df_high_risk, df_trigger_high_risk, 'Outpatient', 'High Risk')

df_trigger_cleared = generate_trigger_reports(df_cleared)
df_inpatient_visits_cleared = generate_visits(df_cleared, df_trigger_cleared, 'Inpatient', 'Cleared - No Risk')
df_outpatient_visits_cleared = generate_visits(df_cleared, df_trigger_cleared, 'Outpatient', 'Cleared - No Risk')

# Combine all related datasets
df_trigger = pd.concat([df_trigger_laser, df_trigger_high_risk, df_trigger_cleared], ignore_index=True)
df_inpatient_visits = pd.concat([df_inpatient_visits_laser, df_inpatient_visits_high_risk, df_inpatient_visits_cleared], ignore_index=True)
df_outpatient_visits = pd.concat([df_outpatient_visits_laser, df_outpatient_visits_high_risk, df_outpatient_visits_cleared], ignore_index=True)

# Generate medical and RX claims for all claimants
df_medical_rx_claims = generate_medical_rx_claims(df_claimants)

# Generate case management data for all claimants
df_case_mgmt = generate_case_management(df_claimants)

# Function to update main data with aggregated values 
def update_main_data():
    # Aggregate Medical Paid and RX Paid
    medical_paid = df_medical_rx_claims[df_medical_rx_claims['Claim Type'] == 'Medical'].groupby('ID')['Paid'].sum().reset_index(name='Medical Paid')
    rx_paid = df_medical_rx_claims[df_medical_rx_claims['Claim Type'] == 'RX'].groupby('ID')['Paid'].sum().reset_index(name='RX Paid')
    
    # Merge with main data
    df_main_updated = df_claimants.merge(medical_paid, on='ID', how='left')
    df_main_updated = df_main_updated.merge(rx_paid, on='ID', how='left')
    
    # Fill NaN values with 0
    df_main_updated['Medical Paid'] = df_main_updated['Medical Paid'].fillna(0).round(2)
    df_main_updated['RX Paid'] = df_main_updated['RX Paid'].fillna(0).round(2)
    
    # Round to 2 decimal places
    df_main_updated['Medical Paid'] = df_main_updated['Medical Paid'].round(2)
    df_main_updated['RX Paid'] = df_main_updated['RX Paid'].round(2)

    # Calculate total inpatient and outpatient visits
    inpatient_visits = df_inpatient_visits.groupby('ID').size().reset_index(name='Inpatient Visits')
    outpatient_visits = df_outpatient_visits.groupby('ID').size().reset_index(name='Outpatient Visits')
    
    df_main_updated = df_main_updated.merge(inpatient_visits, on='ID', how='left')
    df_main_updated = df_main_updated.merge(outpatient_visits, on='ID', how='left')
    
    df_main_updated['Inpatient Visits'] = df_main_updated['Inpatient Visits'].fillna(0)
    df_main_updated['Outpatient Visits'] = df_main_updated['Outpatient Visits'].fillna(0)
    
    # Ongoing Treatment
    case_mgmt_ongoing = df_case_mgmt[df_case_mgmt['Ongoing Treatment'] == True]['ID'].unique()
    df_main_updated['Ongoing Treatment'] = df_main_updated['ID'].isin(case_mgmt_ongoing).astype(int)
    
    # Ensure no NaN in 'Ongoing Treatment'
    df_main_updated['Ongoing Treatment'] = df_main_updated['Ongoing Treatment'].fillna(0)

    # Primary ICD Code and Description
    primary_icd = df_medical_rx_claims[df_medical_rx_claims['Claim Type'] == 'Medical'].groupby('ID').first().reset_index()[['ID', 'ICD10 Code', 'ICD10 Description']]
    df_main_updated = df_main_updated.merge(primary_icd, on='ID', how='left')
    
    
    return df_main_updated

# Update main data
df_main_updated = update_main_data()


# Ensure no NaN values in any of the datasets
datasets = [df_main_updated, df_trigger, df_inpatient_visits, df_outpatient_visits, df_case_mgmt, df_medical_rx_claims]
for df in datasets:
    if df.isnull().values.any():
        print("Warning: NaN values found in dataset")
    else:
        print("No NaN values in dataset")

# Create a directory to save CSV files
import os
output_dir = './container/input_test_data'
os.makedirs(output_dir, exist_ok=True)

# File paths
main_data_path = os.path.join(output_dir, 'main_claimant_data.csv')
main_data_updated_path = os.path.join(output_dir, 'main_claimant_updated_data.csv')
trigger_data_path = os.path.join(output_dir, 'trigger_report_data.csv')
inpatient_data_path = os.path.join(output_dir, 'inpatient_visits_data.csv')
outpatient_data_path = os.path.join(output_dir, 'outpatient_visits_data.csv')
case_mgmt_data_path = os.path.join(output_dir, 'case_management_data.csv')
claims_data_path = os.path.join(output_dir, 'medical_rx_claims_data.csv')

# Save DataFrames to CSV files
df_claimants.to_csv(main_data_path, index=False)
df_main_updated.to_csv(main_data_updated_path, index=False)
df_trigger.to_csv(trigger_data_path, index=False)
df_inpatient_visits.to_csv(inpatient_data_path, index=False)
df_outpatient_visits.to_csv(outpatient_data_path, index=False)
df_case_mgmt.to_csv(case_mgmt_data_path, index=False)
df_medical_rx_claims.to_csv(claims_data_path, index=False)

print("Data generation complete and saved to CSV files.")

print("Data generation and saving complete.")


policy_summary_data_path = os.path.join(output_dir, 'policy_summary_data.json')

# Group by Policy Holder and calculate summary fields
df_policy_summary = df_main_updated.groupby('Policy Holder').agg({
    'Medical Paid': 'sum',
    'RX Paid': 'sum',
    # 'Inpatient Visits': 'sum',
    # 'Outpatient Visits': 'sum',
    'Ongoing Treatment': 'sum',
}).reset_index()

# Display the new dataframe
print(df_policy_summary)
# Convert DataFrame to JSON format
input_data = df_policy_summary.to_dict(orient='records')

# Save JSON data to a local file
with open(policy_summary_data_path, 'w') as json_file:
    json.dump({"data": input_data}, json_file, indent=2)

# # Save the new dataframe to a CSV file if needed
# df_policy_summary.to_csv(policy_summary_data_path, index=False)