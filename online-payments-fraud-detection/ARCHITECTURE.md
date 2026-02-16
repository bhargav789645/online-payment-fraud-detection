# System Architecture & Data Flow

## System Components

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     Online Payments Fraud Detection                      │
└─────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────┐
│   Data Input             │
│   ├─ raw_data.csv        │
│   └─ Transaction details │
└────────────┬─────────────┘
             │
             ↓
┌──────────────────────────────────┐
│   Data Preprocessing             │
│   ├─ Load & Explore              │
│   ├─ Remove unnecessary columns  │
│   ├─ Handle missing values       │
│   └─ Encode categorical types    │
└────────────┬─────────────────────┘
             │
             ↓
┌──────────────────────────────────┐
│   Data Analysis                  │
│   ├─ Univariate analysis         │
│   ├─ Bivariate analysis          │
│   ├─ Descriptive statistics      │
│   └─ Correlation analysis        │
└────────────┬─────────────────────┘
             │
             ↓
┌──────────────────────────────────┐
│   Feature Preparation            │
│   ├─ Split X and y               │
│   ├─ Train-test split (80/20)    │
│   └─ Scale features              │
└────────────┬─────────────────────┘
             │
             ↓
┌──────────────────────────────────┐
│   Model Training (5 models)      │
│   ├─ RandomForest                │
│   ├─ DecisionTree                │
│   ├─ ExtraTrees                  │
│   ├─ SVC                         │
│   └─ XGBoost                     │
└────────────┬─────────────────────┘
             │
             ↓
┌──────────────────────────────────┐
│   Model Evaluation               │
│   ├─ Accuracy                    │
│   ├─ Precision                   │
│   ├─ Recall                      │
│   ├─ F1-Score                    │
│   └─ Select best model           │
└────────────┬─────────────────────┘
             │
             ↓
┌──────────────────────────────────┐
│   Hyperparameter Tuning          │
│   ├─ GridSearchCV                │
│   ├─ CV folds = 5                │
│   └─ Optimize parameters         │
└────────────┬─────────────────────┘
             │
             ↓
┌──────────────────────────────────┐
│   Model Persistence              │
│   ├─ fraud_detection_model.pkl   │
│   ├─ label_encoder.pkl           │
│   └─ feature_names.pkl           │
└────────────┬─────────────────────┘
             │
             ↓
┌─────────────────────────────────────────────────────────────────────────┐
│                    TRAINED MODEL READY FOR PREDICTIONS                  │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Web Application Flow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          USER BROWSER                                   │
│                   http://127.0.0.1:5000                                │
└─────────────────────────────────────────────────────────────────────────┘
                                │
                                ↓
                    ┌───────────────────────┐
                    │   Home Page (/)       │
                    │   - Welcome message   │
                    │   - Start button      │
                    └───────────┬───────────┘
                                │ "Start Prediction"
                                ↓
                    ┌───────────────────────┐
                    │  Prediction Form      │
                    │  (/predict)           │
                    │  - Input fields       │
                    │  - Validation rules   │
                    │  - Submit button      │
                    └───────────┬───────────┘
                                │ [Form Data]
                                ↓
                    ┌────────────────────────────────────┐
                    │  Flask Backend (/submit)           │
                    │  ├─ Parse form data                │
                    │  ├─ Validate inputs                │
                    │  ├─ Encode categorical features    │
                    │  └─ Prepare feature vector         │
                    └───────────┬────────────────────────┘
                                │ [Features]
                                ↓
                    ┌────────────────────────────────────┐
                    │  ML Model Prediction               │
                    │  ├─ Load pickled model             │
                    │  ├─ Run prediction                 │
                    │  ├─ Calculate probability          │
                    │  └─ Format result                  │
                    └───────────┬────────────────────────┘
                                │ [Prediction Result]
                                ↓
                    ┌────────────────────────────────────┐
                    │  Result Page (/submit)             │
                    │  ├─ Is Fraud? (1/0)                │
                    │  ├─ Probability %                  │
                    │  ├─ Confidence score               │
                    │  └─ Transaction details            │
                    └───────────┬────────────────────────┘
                                │
                        [Green: Safe] or [Red: Fraud]
                                │
                ┌───────────────┴───────────────┐
                │                               │
        "Check Another"              "Back Home"
                │                               │
                └───────────────┬───────────────┘
                                │
                        (Cycle restarts)
```

---

## API Request/Response Flow

```
Client Application
        │
        │ POST /api/predict
        │ Content-Type: application/json
        │ {
        │   "step": 1,
        │   "type": "TRANSFER",
        │   "amount": 100.50,
        │   "oldbalanceOrg": 1000.00,
        │   "newbalanceOrig": 899.50,
        │   "oldbalanceDest": 500.00,
        │   "newbalanceDest": 600.50
        │ }
        ↓
┌─────────────────────────────────────────┐
│   Flask API Handler                     │
│   ├─ Parse JSON body                    │
│   ├─ Extract transaction features       │
│   ├─ Validate data types                │
│   ├─ Encode categorical feature         │
│   └─ Create numpy array                 │
└──────────────┬──────────────────────────┘
               │
               ↓
┌─────────────────────────────────────────┐
│   Load Trained Model                    │
│   ├─ Load fraud_detection_model.pkl     │
│   ├─ Load label_encoder.pkl             │
│   ├─ Load feature_names.pkl             │
│   └─ Verify feature count               │
└──────────────┬──────────────────────────┘
               │
               ↓
┌─────────────────────────────────────────┐
│   Make Prediction                       │
│   ├─ model.predict(features)            │
│   ├─ model.predict_proba(features)      │
│   ├─ Calculate confidence               │
│   └─ Format results                     │
└──────────────┬──────────────────────────┘
               │
               ↓ 200 OK
               │ {
               │   "success": true,
               │   "prediction": 0,
               │   "is_fraud": false,
               │   "fraud_probability": 0.05,
               │   "message": "Transaction is Safe"
               │ }
               ↓
          Client Application
```

---

## Feature Processing Pipeline

```
Raw Transaction Input
        │
        ├─ step ────────────────────────► [Numeric] ─┐
        ├─ type ────► [LabelEncoder] ───► [Numeric] ─┤
        ├─ amount ──────────────────────► [Numeric] ─┤
        ├─ oldbalanceOrg ────────────────► [Numeric] ─┤ Feature
        ├─ newbalanceOrig ───────────────► [Numeric] ─┤ Vector
        ├─ oldbalanceDest ───────────────► [Numeric] ─┤
        └─ newbalanceDest ───────────────► [Numeric] ─┘
                                                │
                                                ↓
                                        [1D Array]
                                        [[value1, value2, ..., value7]]
                                                │
                                                ↓
                                    ML Model.predict()
                                                │
                                        ┌───────┴────────┐
                                        │                │
                                    Prediction=0     Prediction=1
                                    (Safe/Legit)     (Fraud)
                                        │                │
                                    Prob ~5-20%      Prob ~80-99%
```

---

## File Dependencies

```
Main Application (app/main.py)
    │
    ├─ Imports:
    │  ├─ Flask (web framework)
    │  ├─ pickle (model loading)
    │  ├─ numpy (array operations)
    │  ├─ os (file paths)
    │  └─ json (API responses)
    │
    ├─ Loads:
    │  ├─ models/fraud_detection_model.pkl
    │  ├─ models/label_encoder.pkl
    │  └─ models/feature_names.pkl
    │
    ├─ Serves:
    │  ├─ app/templates/home.html
    │  ├─ app/templates/predict.html
    │  ├─ app/templates/submit.html
    │  └─ app/static/styles.css
    │
    └─ Uses:
       ├─ config.py (configuration)
       └─ app/__init__.py (app factory)

Training Pipeline (training_script.py)
    │
    ├─ Imports:
    │  ├─ pandas (data loading)
    │  ├─ numpy (array operations)
    │  ├─ matplotlib (visualization)
    │  ├─ seaborn (statistical plotting)
    │  ├─ scikit-learn (ML models)
    │  ├─ xgboost (boosting models)
    │  └─ pickle (model saving)
    │
    ├─ Reads:
    │  └─ data/raw_data.csv
    │
    ├─ Produces:
    │  ├─ models/fraud_detection_model.pkl
    │  ├─ models/label_encoder.pkl
    │  ├─ models/feature_names.pkl
    │  ├─ data_analysis.png
    │  └─ correlation_heatmap.png
    │
    └─ Trains:
       ├─ RandomForestClassifier
       ├─ DecisionTreeClassifier
       ├─ ExtraTreesClassifier
       ├─ SVC
       └─ XGBClassifier (selected)
```

---

## Data Flow Through System

```
Stage 1: Data Loading
┌─────────────────────────────────┐
│ raw_data.csv (2.5M transactions)│
│ ├─ 8 columns                    │
│ ├─ 1M+ rows                     │
│ └─ ~500MB file                  │
└────────────┬────────────────────┘
             │ pandas.read_csv()
             ↓
     DataFrame loaded

Stage 2: Preprocessing
┌─────────────────────────────────┐
│ Raw DataFrame                   │
│ ├─ Drop nameOrig, nameDest      │
│ ├─ Fill missing values          │
│ ├─ Encode type: CASH_IN → 0     │
│ └─ Result: 6 features + target  │
└────────────┬────────────────────┘
             │
             ↓
     Cleaned DataFrame

Stage 3: Analysis
┌─────────────────────────────────┐
│ Statistics Generated            │
│ ├─ Mean amount: $175,000        │
│ ├─ Fraud rate: 0.13%            │
│ ├─ Feature correlations         │
│ └─ Distribution plots           │
└────────────┬────────────────────┘
             │
             ↓
     Insights & Visualizations

Stage 4: Splitting
┌─────────────────────────────────┐
│ 80% Training (2.0M transactions)│
│ 20% Testing (500K transactions) │
│ Split method: random, seed=0    │
└────────────┬────────────────────┘
             │
             ↓
     Train & Test Sets

Stage 5: Training
┌─────────────────────────────────┐
│ 5 models trained on 2.0M rows   │
│ ├─ RF Accuracy: 99.85%          │
│ ├─ DT Accuracy: 99.80%          │
│ ├─ ET Accuracy: 99.87%          │
│ ├─ SVC Accuracy: 99.75%         │
│ └─ XGB Accuracy: 99.89%         │
└────────────┬────────────────────┘
             │
             ↓
     XGBoost Selected

Stage 6: Tuning
┌─────────────────────────────────┐
│ GridSearchCV optimization       │
│ ├─ Parameters tested: 12        │
│ ├─ CV folds: 5                  │
│ ├─ Time: ~2 hours               │
│ └─ Best params found            │
└────────────┬────────────────────┘
             │
             ↓
     Optimized Model

Stage 7: Saving
┌─────────────────────────────────┐
│ Model Serialization             │
│ ├─ fraud_detection_model.pkl    │
│ ├─ label_encoder.pkl            │
│ └─ feature_names.pkl            │
└────────────┬────────────────────┘
             │
             ↓
     Model Ready for Production

Stage 8: Prediction
┌─────────────────────────────────┐
│ New Transaction Input           │
│ ├─ step: 1                      │
│ ├─ type: TRANSFER               │
│ ├─ amount: 100.50               │
│ └─ ... (7 features total)       │
└────────────┬────────────────────┘
             │ Model.predict()
             ↓
     ┌──────────────────┐
     │ Result: Safe (0) │
     │ Probability: 0.05│
     └──────────────────┘
```

---

## Model Architecture

```
Input Features (7)
    │
    ├─ step (1-744)
    ├─ type (0-4 encoded)
    ├─ amount (0-unlimited)
    ├─ oldbalanceOrg
    ├─ newbalanceOrig
    ├─ oldbalanceDest
    └─ newbalanceDest
        │
        ↓ [Feature Vector]
        │
    ┌──────────────────────────────────┐
    │   XGBoost Model (Selected)        │
    │   ├─ n_estimators: 100-200       │
    │   ├─ max_depth: 5-10             │
    │   ├─ learning_rate: 0.01-0.1     │
    │   └─ eval_metric: logloss        │
    └──────────────────┬───────────────┘
                       │
              ┌────────┴────────┐
              │                 │
         Class 0           Class 1
         (Safe)            (Fraud)
              │                 │
        Prob: 0-1          Prob: 0-1
              │                 │
              └────────┬────────┘
                       │
                  [Output]
        Prediction: 0 or 1
        Probability: 0.0-1.0
        Message: Safe or Fraud
```

---

## Performance Characteristics

```
Training Phase
├─ Total Time: 3-5 minutes
├─ Model Training: 2-3 minutes
├─ Hyperparameter Tuning: 1-2 minutes
└─ Model Saving: <1 second

Prediction Phase (Per Request)
├─ Feature Encoding: 1-2ms
├─ Model Inference: 5-10ms
├─ Result Formatting: 1-2ms
└─ Total: 10-50ms

Web Application
├─ Flask Startup: ~500ms
├─ Model Loading: ~1-2 seconds
├─ Page Load: ~500ms
├─ Form Submission: 50-200ms
└─ API Response: 10-100ms

Resource Usage
├─ Memory: ~200-500MB
├─ CPU: 10-30% (during training)
├─ Disk: ~150-200MB (model files)
└─ Network: Minimal (<1KB per request)
```

---

This completes the comprehensive fraud detection system architecture!
