import argparse
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.pipeline import Pipeline
import os
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def train_absa_from_notebook(args):
    """Train ABSA models"""
    
    # aspect mapping
    aspect_map = {
        'llm_Battery': ['battery', 'charge', 'drain', 'backup', 'power'],
        'llm_Display': ['screen', 'oled', 'brightness', 'refresh', 'hz', 'pixel'],
        'llm_Camera': ['photo', 'video', 'lens', 'zoom', 'selfie', 'night mode'],
        'llm_Performance': ['fast', 'lag', 'speed', 'processor', 'gaming', 'hang']
    }
    
    # Load your labeled data 
    csv_file = os.path.join(args.train, "top1000_reviews_with_llm_labels.csv")
    if not os.path.exists(csv_file):
        csv_file = os.path.join(args.train, "top500_reviews_with_llm_labels.csv")
    
    df = pd.read_csv(csv_file)
    logger.info(f"Loaded {len(df)} reviews from {csv_file}")
    
    models = {}
    vectorizers = {}
    
    # Train each aspect model 
    for col in aspect_map.keys():
        if col not in df.columns:
            continue
            
        mask = df[col].notna()
        X = df.loc[mask, 'review']
        y = df.loc[mask, col].values
        
        if len(X) < 10:
            continue
            
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Fit and save vectorizer and model separately
        vectorizer = TfidfVectorizer(stop_words='english', max_features=args.max_features, ngram_range=(1, 2))
        classifier = LogisticRegression(solver='liblinear', class_weight='balanced')
        
        X_train_vec = vectorizer.fit_transform(X_train)
        classifier.fit(X_train_vec, y_train)
        
        X_test_vec = vectorizer.transform(X_test)
        y_pred = classifier.predict(X_test_vec)
        
        accuracy = accuracy_score(y_test, y_pred)
        logger.info(f"{col} accuracy: {accuracy:.3f}")
        
        # Store components separately
        models[col] = classifier
        vectorizers[col] = vectorizer
    
    # Save models and vectorizers
    os.makedirs(args.model_dir, exist_ok=True)
    joblib.dump(models, os.path.join(args.model_dir, "absa_models.pkl"))
    joblib.dump(vectorizers, os.path.join(args.model_dir, "absa_vectorizers.pkl"))
    joblib.dump(aspect_map, os.path.join(args.model_dir, "aspect_map.pkl"))
    
    logger.info(f"ABSA models saved to {args.model_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-dir", type=str, default="./absa_model")
    parser.add_argument("--train", type=str, default="/home/sagemaker-user/shared")
    parser.add_argument("--max-features", type=int, default=1000)
    
    args = parser.parse_args()
    train_absa_from_notebook(args)