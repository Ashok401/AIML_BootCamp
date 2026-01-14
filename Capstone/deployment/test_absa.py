#!/usr/bin/env python3
"""
Test ABSA models locally
"""

import json
import os
import sys
from inference_absa import model_fn, input_fn, predict_fn, output_fn

def test_absa_model(model_dir="./absa_model"):
    """Test ABSA model locally"""
    print("Testing ABSA model...")
    
    # Load model
    try:
        model_dict = model_fn(model_dir)
        print("✓ ABSA models loaded successfully")
        print(f"Available aspects: {model_dict['aspects']}")
    except Exception as e:
        print(f"✗ Error loading model: {e}")
        return False
    
    # Test cases
    test_cases = [
        {
            "review": "Amazing camera quality but terrible battery life",
            "expected": {"camera": "positive", "battery": "negative"}
        },
        {
            "review": "Great display and fast performance, love this phone",
            "expected": {"display": "positive", "performance": "positive"}
        },
        {
            "review": "Battery drains too quickly and screen is dim",
            "expected": {"battery": "negative", "display": "negative"}
        }
    ]
    
    print("\nRunning test cases...")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest Case {i}:")
        print(f"Review: {test_case['review']}")
        
        try:
            # Process input
            parsed_input = input_fn(json.dumps({"review": test_case['review']}), 'application/json')
            
            # Make prediction
            predictions = predict_fn(parsed_input, model_dict)
            
            # Format output
            output = output_fn(predictions, 'application/json')
            
            result = json.loads(output)[0]
            print(f"Aspects detected: {list(result['aspects'].keys())}")
            
            for aspect, prediction in result['aspects'].items():
                if 'sentiment' in prediction:
                    print(f"  {aspect}: {prediction['sentiment']} (confidence: {prediction['confidence']:.2f})")
                else:
                    print(f"  {aspect}: error - {prediction.get('error', 'unknown')}")
            
        except Exception as e:
            print(f"✗ Test failed with error: {e}")
    
    return True

if __name__ == "__main__":
    model_dir = sys.argv[1] if len(sys.argv) > 1 else "./absa_model"
    
    if not os.path.exists(model_dir):
        print(f"Model directory {model_dir} not found!")
        print("Please train the ABSA model first using: python train_absa.py")
        sys.exit(1)
    
    test_absa_model(model_dir)