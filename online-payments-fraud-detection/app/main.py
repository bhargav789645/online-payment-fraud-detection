"""
Flask Application for Online Payments Fraud Detection
"""

from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
import os
import sys

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'fraud_detection_secret_key'

# Get the directory of the current file
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)

# Load the model and encoder
try:
    model_path = os.path.join(project_root, 'models', 'fraud_detection_model.pkl')
    encoder_path = os.path.join(project_root, 'models', 'label_encoder.pkl')
    features_path = os.path.join(project_root, 'models', 'feature_names.pkl')
    
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    
    with open(encoder_path, 'rb') as f:
        label_encoder = pickle.load(f)
    
    with open(features_path, 'rb') as f:
        feature_names = pickle.load(f)
    
    print(f"Model loaded successfully from {model_path}")
    print(f"Features: {feature_names}")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None
    label_encoder = None
    feature_names = None


@app.route('/')
def home():
    """Home page route"""
    return render_template('home.html')


@app.route('/predict', methods=['GET'])
def predict_page():
    """Display prediction form"""
    return render_template('predict.html')


@app.route('/submit', methods=['POST'])
def submit():
    """Handle form submission and make prediction"""
    try:
        # Get form data
        step = float(request.form.get('step', 0))
        transaction_type = request.form.get('type', 'TRANSFER')
        amount = float(request.form.get('amount', 0))
        oldbalanceOrg = float(request.form.get('oldbalanceOrg', 0))
        newbalanceOrig = float(request.form.get('newbalanceOrig', 0))
        oldbalanceDest = float(request.form.get('oldbalanceDest', 0))
        newbalanceDest = float(request.form.get('newbalanceDest', 0))
        
        # Validate inputs
        if None in [step, transaction_type, amount, oldbalanceOrg, newbalanceOrig, oldbalanceDest, newbalanceDest]:
            return render_template('submit.html', 
                                 prediction=None, 
                                 error="Please fill in all fields")
        
        # Encode transaction type
        try:
            encoded_type = label_encoder.transform([transaction_type])[0]
        except:
            return render_template('submit.html', 
                                 prediction=None, 
                                 error=f"Invalid transaction type: {transaction_type}")
        
        # Create feature array in correct order
        features = np.array([[step, encoded_type, amount, oldbalanceOrg, newbalanceOrig, oldbalanceDest, newbalanceDest]])
        
        # Make prediction
        prediction = model.predict(features)[0]
        prediction_proba = model.predict_proba(features)[0]
        
        # Prepare result
        result = {
            'prediction': int(prediction),
            'probability': float(prediction_proba[1]),
            'is_fraud': prediction == 1,
            'confidence': f"{max(prediction_proba) * 100:.2f}%"
        }
        
        return render_template('submit.html', 
                             prediction=result,
                             step=step,
                             transaction_type=transaction_type,
                             amount=amount,
                             oldbalanceOrg=oldbalanceOrg,
                             newbalanceOrig=newbalanceOrig,
                             oldbalanceDest=oldbalanceDest,
                             newbalanceDest=newbalanceDest)
    
    except Exception as e:
        return render_template('submit.html', 
                             prediction=None, 
                             error=f"An error occurred: {str(e)}")


@app.route('/api/predict', methods=['POST'])
def api_predict():
    """API endpoint for predictions (JSON)"""
    try:
        data = request.get_json()
        
        # Extract features
        step = float(data.get('step', 0))
        transaction_type = data.get('type', 'TRANSFER')
        amount = float(data.get('amount', 0))
        oldbalanceOrg = float(data.get('oldbalanceOrg', 0))
        newbalanceOrig = float(data.get('newbalanceOrig', 0))
        oldbalanceDest = float(data.get('oldbalanceDest', 0))
        newbalanceDest = float(data.get('newbalanceDest', 0))
        
        # Encode type
        encoded_type = label_encoder.transform([transaction_type])[0]
        
        # Create feature array
        features = np.array([[step, encoded_type, amount, oldbalanceOrg, newbalanceOrig, oldbalanceDest, newbalanceDest]])
        
        # Predict
        prediction = model.predict(features)[0]
        probability = model.predict_proba(features)[0]
        
        return jsonify({
            'success': True,
            'prediction': int(prediction),
            'is_fraud': bool(prediction == 1),
            'fraud_probability': float(probability[1]),
            'message': 'Fraudulent Transaction Detected!' if prediction == 1 else 'Transaction is Safe'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)