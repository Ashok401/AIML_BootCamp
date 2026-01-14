import json
import joblib
import numpy as np
import pandas as pd
import os
import re
import logging
from typing import List, Dict, Any, Union

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def model_fn(model_dir: str) -> Dict[str, Any]:
    """Load ABSA models and vectorizers"""
    try:
        models_path = os.path.join(model_dir, "absa_models.pkl")
        vectorizers_path = os.path.join(model_dir, "absa_vectorizers.pkl")
        aspect_map_path = os.path.join(model_dir, "aspect_map.pkl")
        
        logger.info(f"Loading models from: {model_dir}")
        
        models = joblib.load(models_path)
        vectorizers = joblib.load(vectorizers_path)
        aspect_map = joblib.load(aspect_map_path)
        
        aspects = list(models.keys())
        logger.info(f"Loaded ABSA models for aspects: {aspects}")
        
        return {
            "models": models,
            "vectorizers": vectorizers,
            "aspects": aspects,
            "aspect_map": aspect_map
        }
    except Exception as e:
        logger.error(f"Error loading ABSA models: {str(e)}")
        raise

def preprocess_text(text: str) -> str:
    """Clean and preprocess phone review text"""
    if not text or pd.isna(text):
        return ""
    
    text = str(text).lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    text = ' '.join([word for word in text.split() if len(word) > 1])
    return text

def input_fn(request_body: Union[str, bytes], request_content_type: str) -> List[str]:
    """Parse input data"""
    try:
        if request_content_type == 'application/json':
            if isinstance(request_body, bytes):
                request_body = request_body.decode('utf-8')
            
            input_data = json.loads(request_body)
            
            if isinstance(input_data, dict):
                if 'review' in input_data:
                    return [str(input_data['review'])]
                elif 'reviews' in input_data:
                    return [str(review) for review in input_data['reviews']]
            elif isinstance(input_data, list):
                return [str(item) for item in input_data]
            else:
                return [str(input_data)]
        else:
            if isinstance(request_body, bytes):
                request_body = request_body.decode('utf-8')
            return [str(request_body)]
    except Exception as e:
        logger.error(f"Error parsing input: {str(e)}")
        return [str(request_body) if request_body else ""]

def predict_fn(input_data: List[str], model_dict: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Run ABSA prediction on phone reviews"""
    try:
        models = model_dict["models"]
        vectorizers = model_dict["vectorizers"]
        
        results = []
        for review in input_data:
            cleaned_review = preprocess_text(review)
            
            if not cleaned_review:
                results.append({"review": review, "aspects": {}, "error": "Empty review"})
                continue
            
            # Find relevant aspects with enhanced keyword matching
            text_lower = review.lower()
            
            # Enhanced aspect map with additional keywords
            enhanced_aspect_map = {
                'llm_Battery': ['battery', 'charge', 'drain', 'backup', 'power', 'life'],
                'llm_Display': ['screen', 'oled', 'brightness', 'refresh', 'hz', 'pixel', 'display'],
                'llm_Camera': ['photo', 'video', 'lens', 'zoom', 'selfie', 'night mode', 'camera', 'picture'],
                'llm_Performance': ['fast', 'lag', 'speed', 'processor', 'gaming', 'hang', 'performance', 'slow']
            }
            
            found_aspects = [aspect for aspect, keywords in enhanced_aspect_map.items() 
                           if any(keyword in text_lower for keyword in keywords)]
            
            if not found_aspects:
                results.append({"review": review, "aspects": {}, "note": "No specific aspects detected"})
                continue
            
            aspect_predictions = {}
            
            # Use separate vectorizer and model
            for aspect in found_aspects:
                if aspect in models:
                    vectorizer = vectorizers[aspect]
                    model = models[aspect]
                    
                    X = vectorizer.transform([cleaned_review])
                    prediction = model.predict(X)[0]
                    probabilities = model.predict_proba(X)[0]
                    
                    sentiment = "positive" if prediction == 1 else "negative"
                    confidence = float(max(probabilities))
                    
                    aspect_predictions[aspect.replace('llm_', '').lower()] = {
                        "sentiment": sentiment,
                        "confidence": confidence
                    }
            
            results.append({"review": review, "aspects": aspect_predictions})
        
        return results
        
    except Exception as e:
        logger.error(f"Error in ABSA prediction: {str(e)}")
        return [{"review": review, "error": str(e)} for review in input_data]

def output_fn(prediction: List[Dict[str, Any]], content_type: str) -> str:
    """Format the prediction output"""
    return json.dumps(prediction, indent=2, ensure_ascii=False)