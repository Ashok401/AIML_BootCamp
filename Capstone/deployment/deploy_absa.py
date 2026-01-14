import boto3
import sagemaker
from sagemaker.sklearn.model import SKLearnModel
import tarfile
import os
import shutil

# Initialize SageMaker session
sagemaker_session = sagemaker.Session()
role = sagemaker.get_execution_role()

# Create model artifact
def create_model_tar():
    # Clean up any existing temp directory
    if os.path.exists('/tmp/model_package'):
        shutil.rmtree('/tmp/model_package')
    
    # Create temporary directory structure
    os.makedirs('/tmp/model_package/code', exist_ok=True)
    
    # Copy model files to root directory
    shutil.copy('/home/sagemaker-user/absa_model/absa_models.pkl', '/tmp/model_package/absa_models.pkl')
    shutil.copy('/home/sagemaker-user/absa_model/absa_vectorizers.pkl', '/tmp/model_package/absa_vectorizers.pkl')
    shutil.copy('/home/sagemaker-user/absa_model/aspect_map.pkl', '/tmp/model_package/aspect_map.pkl')
    
    # Copy inference script
    shutil.copy('/home/sagemaker-user/shared/inference_absa.py', '/tmp/model_package/code/inference_absa.py')
    
    # Copy requirements file
    shutil.copy('/home/sagemaker-user/shared/requirements_enhanced.txt', '/tmp/model_package/code/requirements.txt')
    
    # Create tar file with proper structure
    with tarfile.open('/home/sagemaker-user/shared/model.tar.gz', 'w:gz') as tar:
        # Add model files to root
        tar.add('/tmp/model_package/absa_models.pkl', arcname='absa_models.pkl')
        tar.add('/tmp/model_package/absa_vectorizers.pkl', arcname='absa_vectorizers.pkl')
        tar.add('/tmp/model_package/aspect_map.pkl', arcname='aspect_map.pkl')
        # Add code directory
        tar.add('/tmp/model_package/code', arcname='code')
    
    print("Model artifact created: model.tar.gz")

# Deploy model
def deploy_model():
    create_model_tar()
    
    # Upload to S3
    model_artifacts = sagemaker_session.upload_data(
        path='/home/sagemaker-user/shared/model.tar.gz',
        key_prefix='absa-model'
    )
    
    # Create SKLearn model
    sklearn_model = SKLearnModel(
        model_data=model_artifacts,
        role=role,
        entry_point='inference_absa.py',
        source_dir=None,
        framework_version='1.0-1',
        py_version='py3'
    )
    
    # Deploy
    predictor = sklearn_model.deploy(
        initial_instance_count=1,
        instance_type='ml.t2.medium'
    )
    
    print(f"Model deployed! Endpoint: {predictor.endpoint_name}")
    return predictor

if __name__ == "__main__":
    predictor = deploy_model()