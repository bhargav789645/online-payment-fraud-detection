# Quick Start Guide

## Getting Started in 5 Minutes

### Step 1: Install Dependencies (1 minute)
```bash
pip install -r requirements.txt
```

### Step 2: Train the Model (2-3 minutes)
```bash
python training_script.py
```

This will:
- Process your data
- Train 5 different ML models
- Evaluate and select the best one
- Save the model to `models/fraud_detection_model.pkl`
- Generate visualization charts

### Step 3: Run the Flask App (30 seconds)
```bash
cd app
python main.py
```

### Step 4: Open in Browser (10 seconds)
Navigate to: `http://127.0.0.1:5000`

---

## What You'll See

1. **Home Page** - Welcome screen with project info
2. **Prediction Form** - Enter transaction details
3. **Result Page** - Shows if transaction is fraud or safe with confidence score

---

## Example Transaction (SAFE)

```
Step: 1
Type: TRANSFER
Amount: 100.50
Old Balance Origin: 1000.00
New Balance Origin: 899.50
Old Balance Destination: 500.00
New Balance Destination: 600.50
```

Expected Result: ✅ SAFE TRANSACTION

---

## Example Transaction (FRAUD)

```
Step: 500
Type: CASH_OUT
Amount: 999999.00
Old Balance Origin: 1000000.00
New Balance Origin: 1.00
Old Balance Destination: 0.00
New Balance Destination: 999999.00
```

Expected Result: 🚨 FRAUDULENT TRANSACTION

---

## File Structure After Training

```
models/
├── fraud_detection_model.pkl       ← Best ML model
├── label_encoder.pkl               ← Type encoder
└── feature_names.pkl               ← Feature list
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Module not found | Run `pip install -r requirements.txt` |
| Model not found | Run `python training_script.py` |
| Port 5000 in use | Change port in `app/main.py` line 133 |
| Data not found | Ensure `data/raw_data.csv` exists |

---

## API Usage (Optional)

```bash
curl -X POST http://127.0.0.1:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "step": 1,
    "type": "TRANSFER",
    "amount": 100.50,
    "oldbalanceOrg": 1000.00,
    "newbalanceOrig": 899.50,
    "oldbalanceDest": 500.00,
    "newbalanceDest": 600.50
  }'
```

---

## Next Steps

- Explore `README.md` for detailed documentation
- Check `data_analysis.png` for data insights
- Review model performance in console output
- Customize transaction types in `predict.html`
