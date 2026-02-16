# Installation & Setup Guide

## Prerequisites

- Python 3.8 or higher
- pip (comes with Python)
- 2GB free disk space
- ~5-10 minutes for first-time setup and training

## Step-by-Step Installation

### Option 1: Windows (Easiest)

1. **Download Project**
   ```bash
   git clone <repo-url>
   cd online-payments-fraud-detection
   ```

2. **Run the Batch Script**
   - Double-click `run_windows.bat`
   - The script will automatically:
     - Create virtual environment
     - Install dependencies
     - Train the model
     - Start the Flask app

3. **Open Browser**
   - Navigate to `http://127.0.0.1:5000`

### Option 2: macOS/Linux

1. **Download Project**
   ```bash
   git clone <repo-url>
   cd online-payments-fraud-detection
   ```

2. **Make Script Executable**
   ```bash
   chmod +x run_linux_mac.sh
   ```

3. **Run the Script**
   ```bash
   ./run_linux_mac.sh
   ```

4. **Open Browser**
   - Navigate to `http://127.0.0.1:5000`

### Option 3: Manual Setup (All Platforms)

1. **Create Virtual Environment**
   ```bash
   python -m venv venv
   ```

2. **Activate Virtual Environment**
   
   **Windows:**
   ```bash
   venv\Scripts\activate
   ```
   
   **macOS/Linux:**
   ```bash
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Train the Model**
   ```bash
   python training_script.py
   ```
   
   This will take 2-5 minutes. You should see:
   ```
   Step 1: Loading Data...
   Step 2: Data Preprocessing...
   Step 3: Data Analysis and Visualization...
   Step 4: Preparing Data for Modeling...
   Step 5: Training Multiple Models...
   Step 6: Hyperparameter Tuning...
   Step 7: Final Model Evaluation...
   Step 8: Saving the Model...
   Training Complete!
   ```

5. **Start Flask App**
   ```bash
   cd app
   python main.py
   ```
   
   You should see:
   ```
   WARNING in werkzeug: ...
    * Serving Flask app 'main'
    * Debug mode: on
    * Running on http://127.0.0.1:5000
   ```

6. **Open Browser**
   - Navigate to `http://127.0.0.1:5000`

## Verify Installation

After installation, check these files exist:

```
models/
├── fraud_detection_model.pkl       ✓ Model file (~100MB)
├── label_encoder.pkl               ✓ Encoder file
└── feature_names.pkl               ✓ Features file
```

If these don't exist, run:
```bash
python training_script.py
```

## First Run Checklist

- [ ] Python 3.8+ installed
- [ ] All dependencies installed (pip list shows Flask, pandas, scikit-learn, etc.)
- [ ] Model files exist in `models/` folder
- [ ] Flask app starts without errors
- [ ] Can access `http://127.0.0.1:5000` in browser
- [ ] Home page loads successfully
- [ ] Can access `/predict` form
- [ ] Can submit a transaction and see prediction result

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'flask'"
**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: "FileNotFoundError: fraud_detection_model.pkl"
**Solution:**
```bash
python training_script.py
```

### Issue: "Address already in use"
**Solution:**
- Close other Flask instances, or
- Change port in `app/main.py`:
```python
app.run(debug=True, host='127.0.0.1', port=5001)  # Use 5001
```

### Issue: Data file not found
**Ensure `data/raw_data.csv` exists** - it should be included with the project

### Issue: Virtual environment not activating
**Windows:**
```bash
venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

## System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| Python | 3.8 | 3.10+ |
| RAM | 2GB | 8GB+ |
| Storage | 2GB | 5GB+ |
| OS | Windows/Mac/Linux | Windows/Mac/Linux |

## Performance Notes

- **First Training**: 3-5 minutes (model training, evaluation, tuning)
- **Subsequent Runs**: <1 second (model already trained)
- **Prediction**: ~10-50ms per transaction
- **Web Response**: <500ms average

## Optional: GPU Support

For faster training with GPU (NVIDIA only):

```bash
pip install xgboost[gpu]
```

## Security Setup

For production deployment:

1. **Generate Secret Key**
   ```python
   import secrets
   print(secrets.token_hex(16))
   ```

2. **Set Environment Variable**
   ```bash
   set SECRET_KEY=<generated-key>  # Windows
   export SECRET_KEY=<generated-key>  # Linux/Mac
   ```

3. **Update config.py**
   ```python
   SECRET_KEY = os.environ.get('SECRET_KEY', 'default-key')
   ```

4. **Disable Debug Mode**
   ```python
   DEBUG = False  # In config.py for production
   ```

## Next Steps

1. Read `README.md` for detailed documentation
2. Check `QUICKSTART.md` for usage examples
3. Explore `data_analysis.png` to understand your data
4. Customize transaction types as needed
5. Deploy to production (see README.md)

---

**Need Help?**
- Check README.md for API documentation
- See QUICKSTART.md for usage examples
- Review app/main.py for application logic
- Check training_script.py for model training details
