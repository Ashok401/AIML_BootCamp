# iPhone ABSA (Aspect-Based Sentiment Analysis) Project

A machine learning project that performs aspect-based sentiment analysis on iPhone reviews, deployed on AWS SageMaker for real-time inference.

## 🎯 Project Overview

This project analyzes iPhone reviews to extract sentiment for specific aspects like battery, camera, display, and performance. The model identifies relevant aspects in reviews and classifies sentiment as positive or negative with confidence scores.

## 📊 Results

- **85% accuracy** on unseen test data
- **Real-time inference** via SageMaker endpoint
- **Multi-aspect detection**: Battery, Camera, Display, Performance
- **Confidence scores**: 0.51-0.78 range

## 🏗️ Architecture

```
iPhone Reviews → Data Processing → ABSA Training → SageMaker Deployment → Real-time Inference
```

## 📁 Project Structure

### Core Files

#### `train_absa.py`
**Purpose**: Trains ABSA models for each aspect
- Loads labeled review data
- Creates separate TF-IDF vectorizers and Logistic Regression models for each aspect
- Saves trained models, vectorizers, and aspect mappings
- **Usage**: `python train_absa.py --model-dir ./absa_model`

#### `deploy_absa.py` 
**Purpose**: Deploys trained models to SageMaker
- Packages models into tar.gz format
- Uploads to S3 and creates SageMaker endpoint
- Uses sklearn framework version 1.0-1
- **Output**: SageMaker endpoint for real-time inference

#### `inference_absa.py`
**Purpose**: SageMaker inference script
- Loads models and vectorizers
- Preprocesses input text
- Detects relevant aspects using keyword matching
- Returns sentiment predictions with confidence scores

#### `test_absa.py`
**Purpose**: Local testing of trained models
- Tests models before deployment
- Validates aspect detection and sentiment classification
- **Usage**: `python test_absa.py /path/to/model`

#### `test_endpoint.py`
**Purpose**: Tests deployed SageMaker endpoint
- Sends sample requests to endpoint
- Validates real-time inference
- **Usage**: Update endpoint name and run

### Data Files

#### `iphone.csv`
**Purpose**: Raw iPhone review data from Amazon
- Contains review titles, descriptions, ratings, metadata
- Source data for training and testing

#### `top1000_reviews.csv`
**Purpose**: Top 1000 longest reviews (by word count)
- Filtered high-quality reviews for training
- Created by sorting original data by word count

#### `top1000_reviews_with_llm_labels.csv`
**Purpose**: Labeled training data
- Contains LLM-generated aspect labels (llm_Battery, llm_Display, etc.)
- Used for supervised training of ABSA models

### Model Files

#### `absa_model/`
**Purpose**: Trained model artifacts
- `absa_models.pkl`: Trained classifiers for each aspect
- `absa_vectorizers.pkl`: TF-IDF vectorizers for each aspect  
- `aspect_map.pkl`: Keyword mappings for aspect detection

#### `model.tar.gz`
**Purpose**: SageMaker deployment package
- Contains models, vectorizers, inference script, and requirements
- Uploaded to S3 for SageMaker deployment

### Configuration Files

#### `requirements_enhanced.txt`
**Purpose**: Python dependencies
- Specifies exact versions for reproducibility
- Used in both training and deployment environments
- Key packages: scikit-learn==1.3.0, joblib==1.3.2, pandas==2.0.3

### Test Results

#### `absa_test_20_results.md`
**Purpose**: Comprehensive test results documentation
- 20 unseen reviews tested
- Detailed accuracy analysis
- Performance metrics and insights

#### `absa_test_20_results.json`
**Purpose**: Raw test data
- JSON format test results
- Includes full reviews, predictions, and confidence scores

## 🚀 Quick Start

### 1. Training
```bash
# Train ABSA models
python train_absa.py --model-dir ./absa_model
```

### 2. Local Testing
```bash
# Test trained models locally
python test_absa.py ./absa_model
```

### 3. Deployment
```bash
# Deploy to SageMaker
python deploy_absa.py
```

### 4. Endpoint Testing
```bash
# Test deployed endpoint
python test_endpoint.py
```

## 📋 Requirements

- Python 3.11
- scikit-learn==1.3.0
- pandas==2.0.3
- numpy==1.25.2
- joblib==1.3.2
- boto3 (for AWS deployment)
- sagemaker (for deployment)

## 🔧 Model Details

### Aspects Detected
- **Battery**: battery, charge, drain, backup, power, life
- **Display**: screen, oled, brightness, refresh, hz, pixel, display  
- **Camera**: photo, video, lens, zoom, selfie, night mode, camera, picture
- **Performance**: fast, lag, speed, processor, gaming, hang, performance, slow

### Algorithm
- **Vectorization**: TF-IDF with 1000 max features, 1-2 ngrams
- **Classification**: Logistic Regression with balanced class weights
- **Preprocessing**: Text cleaning, lowercasing, word filtering

### Training Data
- 1000 longest iPhone reviews
- LLM-labeled for aspect sentiment
- Train/test split: 80/20

## 📈 Performance Metrics

- **Overall Accuracy**: 85%
- **Battery Detection**: 77.8% accuracy
- **False Positive Rate**: 11.1%
- **Precision**: High (correctly identifies relevant aspects)
- **Recall**: Good (detects most relevant aspects)

## 🌐 Deployment

### SageMaker Endpoint
- **Framework**: scikit-learn 1.0-1
- **Instance**: ml.t2.medium
- **Input**: JSON with 'review' field
- **Output**: Aspects with sentiment and confidence

### Example Usage
```python
import boto3
import json

runtime = boto3.client('sagemaker-runtime')
response = runtime.invoke_endpoint(
    EndpointName='your-endpoint-name',
    ContentType='application/json',
    Body=json.dumps({"review": "Amazing camera quality but terrible battery life"})
)
```

### Example Output
```json
[{
  "review": "Amazing camera quality but terrible battery life",
  "aspects": {
    "battery": {"sentiment": "negative", "confidence": 0.78},
    "camera": {"sentiment": "positive", "confidence": 0.67}
  }
}]
```

## 🔍 Key Features

- **Multi-aspect Analysis**: Simultaneously analyzes multiple phone aspects
- **Real-time Inference**: Sub-second response times via SageMaker
- **Confidence Scores**: Provides prediction confidence for reliability assessment
- **Keyword-based Detection**: Only analyzes aspects mentioned in reviews
- **Scalable Deployment**: AWS SageMaker for production workloads

## 📝 Notes

- Models trained on iPhone-specific reviews
- Optimized for phone review language and terminology  
- Version compatibility ensured between training and deployment
- Comprehensive testing on unseen data validates production readiness

## 🤝 Contributing

1. Ensure version compatibility (see requirements_enhanced.txt)
2. Test locally before deployment
3. Update documentation for any changes
4. Validate on unseen data

## 📄 License

This project is for educational and research purposes.