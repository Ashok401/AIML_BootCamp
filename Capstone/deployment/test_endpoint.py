import boto3
import json

# Test the deployed endpoint
endpoint_name = "sagemaker-scikit-learn-2026-01-14-21-46-38-147"
runtime = boto3.client('sagemaker-runtime')

test_review = "Amazing camera quality but terrible battery life"

response = runtime.invoke_endpoint(
    EndpointName=endpoint_name,
    ContentType='application/json',
    Body=json.dumps({"review": test_review})
)

result = json.loads(response['Body'].read().decode())
print(f"Review: {test_review}")
print(f"Result: {json.dumps(result, indent=2)}")