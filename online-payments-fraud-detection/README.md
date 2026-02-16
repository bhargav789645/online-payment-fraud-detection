
# Online Payments Fraud Detection System

> A complete, production-ready machine learning web application for detecting fraudulent online payments. Built with Python, Flask, scikit-learn, XGBoost, and a modern UI.

---

## 🚀 Quick Start

**Windows:**
```bash
run_windows.bat
```
**Linux/Mac:**
```bash
chmod +x run_linux_mac.sh
./run_linux_mac.sh
```
**Manual:**
```bash
pip install -r requirements.txt
python training_script.py
cd app
python main.py
```
Then open: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 📦 Project Structure

```
online-payments-fraud-detection/
├── app/
│   ├── main.py, __init__.py, routes/, static/, templates/
├── data/
│   ├── raw_data.csv, processed_data.csv
├── models/
│   ├── fraud_detection_model.pkl, label_encoder.pkl, feature_names.pkl
├── training_script.py
├── config.py
├── requirements.txt
├── run_windows.bat, run_linux_mac.sh
├── README.md (this file)
```

---

## ✅ Features & Requirements Checklist

- [x] Data loading, cleaning, encoding, and analysis
- [x] Univariate, bivariate, and descriptive statistics
- [x] Model training: RandomForest, DecisionTree, ExtraTrees, SVC, XGBoost
- [x] Hyperparameter tuning (GridSearchCV)
- [x] Model evaluation: accuracy, precision, recall, F1, confusion matrix
- [x] Model persistence (pickle)
- [x] Flask web app with modern UI
- [x] HTML templates: home, predict, submit
- [x] REST API endpoint for predictions
- [x] Responsive CSS styling
- [x] Complete documentation in this README

---

## 🏗️ Installation & Setup

1. **Clone the repository**
  ```bash
  git clone <repository-url>
  cd online-payments-fraud-detection
  ```
2. **Create virtual environment**
  ```bash
  python -m venv venv
  ```
3. **Activate virtual environment**
  - Windows: `venv\Scripts\activate`
  - Mac/Linux: `source venv/bin/activate`
4. **Install dependencies**
  ```bash
  pip install -r requirements.txt
  ```
5. **Train the model**
  ```bash
  python training_script.py
  ```
6. **Run the app**
  ```bash
  cd app
  python main.py
  ```
7. **Open browser**
  - Go to [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🧑‍💻 Usage

### Web Interface
1. Home page: Click "Start Prediction"
2. Fill in transaction details (step, type, amount, balances)
3. Click "Analyze Transaction"
4. See result: "Safe" or "Fraudulent" with confidence score

### API Endpoint
**POST** `/api/predict`
```json
{
  "step": 1,
  "type": "TRANSFER",
  "amount": 100.50,
  "oldbalanceOrg": 1000.00,
  "newbalanceOrig": 899.50,
  "oldbalanceDest": 500.00,
  "newbalanceDest": 600.50
}
```
**Response:**
```json
{
  "success": true,
  "prediction": 0,
  "is_fraud": false,
  "fraud_probability": 0.05,
  "message": "Transaction is Safe"
}
```

---

## 📊 Data & Model Pipeline

1. **Data Preprocessing**: Remove `nameOrig`, `nameDest`, handle nulls, encode `type`
2. **Analysis**: Univariate (amount/type), bivariate (amount/type vs isFraud), descriptive stats, correlation heatmap
3. **Model Training**: Train/test split (80/20), 5 models, hyperparameter tuning
4. **Evaluation**: Accuracy, precision, recall, F1, confusion matrix
5. **Persistence**: Save best model, encoder, and feature names as `.pkl`
6. **Web App**: Flask app loads model, serves UI, and provides API

---

## 🖥️ Architecture & Data Flow

```
User (Web Form/API)
  ↓
Flask App (main.py)
  ↓
Model (fraud_detection_model.pkl)
  ↓
Prediction (Safe/Fraud + probability)
  ↓
Result Page or API Response
```

---

## 🧪 Testing

1. Home page loads: [http://127.0.0.1:5000](http://127.0.0.1:5000)
2. Prediction form works for all transaction types
3. Safe transaction returns "Safe"
4. Fraudulent transaction returns "Fraudulent"
5. API endpoint returns correct JSON
6. All fields validated (empty/invalid input shows error)
7. Responsive design on desktop/mobile

---

## 🛠️ Troubleshooting

- **ModuleNotFoundError**: Run `pip install -r requirements.txt`
- **Model not found**: Run `python training_script.py` to generate model files
- **Port in use**: Change port in `app/main.py`
- **Data missing**: Ensure `data/raw_data.csv` exists

---

## 📈 Performance

- Training: 2-5 minutes (one-time)
- Prediction: 10-50ms per transaction
- Model accuracy: 99%+
- API response: <100ms

---

## 🔒 Security & Production

- Validate all input
- Use HTTPS in production
- Store secrets in environment variables
- Disable debug mode in production

---

## 📚 License & Support

MIT License. For issues, open a GitHub issue.
---

## ✨ Credits

Built by: Bhargava Sai Kakumani
Inspired by: PSP Fraud Dataset, scikit-learn, Flask, XGBoost

---

**Last Updated:** February 2026
**Version:** 1.0.0