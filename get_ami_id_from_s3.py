import boto3
import pandas as pd
from io import BytesIO

def get_ami_id_from_s3(bucket_name, file_key, region, os):
    s3 = boto3.client('s3')

    # Extract the key path from file_key
    key_path = file_key.replace(f's3://{bucket_name}/', '')

    # Fetch the Excel file from S3
    obj = s3.get_object(Bucket=bucket_name, Key=key_path)

    # Read the Excel file into a pandas DataFrame
    excel_data = obj['Body'].read()
    df = pd.read_excel(BytesIO(excel_data), engine='openpyxl')

    # Filter the DataFrame based on the region and OS
    filtered_df = df[(df['Region'] == region) & (df['OS'] == os)]

    if not filtered_df.empty:
        ami_id = filtered_df.iloc[0]['AMI-ID']
        return ami_id
    else:
        raise ValueError(f"No entry found for Region '{region}' and OS '{os}'")

# Usage example
bucket_name = 'finops-test2'
file_key = 'ami.xlsx' 
region = 'Singapore'
os = 'Windows-2019'

try:
    ami_id = get_ami_id_from_s3(bucket_name, file_key, region, os)
    print(f"AMI ID for Region '{region}' and OS '{os}': {ami_id}")
except ValueError as e:
    print(e)
except Exception as e:
    print(f"Error: {e}")
