from flask import Blueprint, request, jsonify
import pickle

fraud_detection_bp = Blueprint('fraud_detection', __name__)

# Load the trained model
with open('models/fraud_detection_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

@fraud_detection_bp.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    # Assuming data is preprocessed and ready for prediction
    prediction = model.predict([data])
    return jsonify({'prediction': prediction[0]})

@fraud_detection_bp.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    # Logic for handling submission
    return jsonify({'message': 'Prediction submitted successfully.'})