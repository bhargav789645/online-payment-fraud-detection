"""
Fraud Detection Model Training Script
This script handles data preprocessing, analysis, model training, and hyperparameter tuning.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split, GridSearchCV, RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, precision_score, recall_score, f1_score
import pickle
import warnings
warnings.filterwarnings('ignore')

# ==================== 1. DATA COLLECTION ====================
print("Step 1: Loading Data...")
df = pd.read_csv('data/raw_data.csv')
print(f"Dataset shape: {df.shape}")
print(f"First few rows:\n{df.head()}")

# ==================== 2. DATA PREPROCESSING ====================
print("\n" + "="*50)
print("Step 2: Data Preprocessing...")
print("="*50)

# Check initial info
print("\nInitial dataset info:")
print(df.info())
print(f"\nNull values:\n{df.isnull().sum()}")

# Remove unnecessary columns
df = df.drop(['nameOrig', 'nameDest'], axis=1)
print(f"\nDataset after removing unnecessary columns: {df.shape}")

# Handle missing values
print(f"Missing values after dropping columns:\n{df.isnull().sum()}")
if df.isnull().sum().sum() > 0:
    df.fillna(df.mean(), inplace=True)

# Encode categorical column 'type'
le = LabelEncoder()
df['type'] = le.fit_transform(df['type'])
print(f"\nEncoded 'type' column mapping:")
for i, label in enumerate(le.classes_):
    print(f"  {label} -> {i}")

# Display processed data
print(f"\nProcessed dataset info:")
print(df.info())
print(f"\nProcessed dataset head:\n{df.head()}")

# ==================== 3. DATA ANALYSIS ====================
print("\n" + "="*50)
print("Step 3: Data Analysis and Visualization...")
print("="*50)

# Descriptive Statistics
print("\nDescriptive Statistics:")
print(df.describe())

# Correlation Matrix
print("\nCorrelation Matrix:")
correlation_matrix = df.corr()
print(correlation_matrix)

# Create visualizations
fig, axes = plt.subplots(2, 2, figsize=(15, 12))

# Univariate Analysis - Distribution of Amount
axes[0, 0].hist(df['amount'], bins=50, edgecolor='black')
axes[0, 0].set_title('Distribution of Amount', fontsize=12, fontweight='bold')
axes[0, 0].set_xlabel('Amount')
axes[0, 0].set_ylabel('Frequency')

# Univariate Analysis - Distribution of Type
type_counts = df['type'].value_counts()
axes[0, 1].bar(type_counts.index, type_counts.values, edgecolor='black')
axes[0, 1].set_title('Distribution of Transaction Type', fontsize=12, fontweight='bold')
axes[0, 1].set_xlabel('Type')
axes[0, 1].set_ylabel('Frequency')

# Bivariate Analysis - Amount vs isFraud
fraud_data = df.groupby('isFraud')['amount'].apply(list)
axes[1, 0].boxplot([fraud_data[0], fraud_data[1]], labels=['Not Fraud', 'Fraud'])
axes[1, 0].set_title('Amount vs isFraud', fontsize=12, fontweight='bold')
axes[1, 0].set_ylabel('Amount')

# Bivariate Analysis - Type vs isFraud
fraud_by_type = pd.crosstab(df['type'], df['isFraud'])
fraud_by_type.plot(kind='bar', ax=axes[1, 1], edgecolor='black')
axes[1, 1].set_title('Transaction Type vs isFraud', fontsize=12, fontweight='bold')
axes[1, 1].set_xlabel('Type')
axes[1, 1].set_ylabel('Count')
axes[1, 1].legend(['Not Fraud', 'Fraud'])

plt.tight_layout()
plt.savefig('data_analysis.png', dpi=300, bbox_inches='tight')
print("\nVisualization saved as 'data_analysis.png'")
plt.close()

# Correlation heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, fmt='.2f')
plt.title('Correlation Matrix Heatmap', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('correlation_heatmap.png', dpi=300, bbox_inches='tight')
print("Correlation heatmap saved as 'correlation_heatmap.png'")
plt.close()

# ==================== 4. PREPARE DATA FOR MODELING ====================
print("\n" + "="*50)
print("Step 4: Preparing Data for Modeling...")
print("="*50)

X = df.drop('isFraud', axis=1)
y = df['isFraud']

print(f"\nFeatures shape: {X.shape}")
print(f"Target shape: {y.shape}")
print(f"Feature names: {list(X.columns)}")
print(f"\nTarget distribution:\n{y.value_counts()}")

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
print(f"\nTraining set size: {X_train.shape[0]}")
print(f"Test set size: {X_test.shape[0]}")

# ==================== 5. TRAIN MULTIPLE MODELS ====================
print("\n" + "="*50)
print("Step 5: Training Multiple Models...")
print("="*50)

models = {
    'RandomForest': RandomForestClassifier(n_estimators=100, random_state=0),
    'DecisionTree': DecisionTreeClassifier(random_state=0),
    'ExtraTrees': ExtraTreesClassifier(n_estimators=100, random_state=0),
    'SVC': SVC(kernel='rbf', random_state=0),
    'XGBoost': XGBClassifier(n_estimators=100, random_state=0, use_label_encoder=False, eval_metric='logloss')
}

trained_models = {}
model_results = {}

for name, model in models.items():
    print(f"\nTraining {name}...")
    model.fit(X_train, y_train)
    
    # Predictions
    y_pred = model.predict(X_test)
    
    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    
    trained_models[name] = model
    model_results[name] = {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'confusion_matrix': confusion_matrix(y_test, y_pred),
        'classification_report': classification_report(y_test, y_pred)
    }
    
    print(f"{name} Results:")
    print(f"  Accuracy: {accuracy:.4f}")
    print(f"  Precision: {precision:.4f}")
    print(f"  Recall: {recall:.4f}")
    print(f"  F1-Score: {f1:.4f}")

# Find best model based on F1-score
best_model_name = max(model_results, key=lambda x: model_results[x]['f1'])
print(f"\n{'='*50}")
print(f"Best Model: {best_model_name} (F1-Score: {model_results[best_model_name]['f1']:.4f})")
print(f"{'='*50}")

# ==================== 6. HYPERPARAMETER TUNING ====================
print("\n" + "="*50)
print("Step 6: Hyperparameter Tuning for Best Model...")
print("="*50)

if best_model_name == 'RandomForest':
    print("\nTuning RandomForestClassifier...")
    param_grid = {
        'n_estimators': [100, 200],
        'max_depth': [10, 20, None],
        'min_samples_split': [2, 5],
        'min_samples_leaf': [1, 2]
    }
    grid_search = GridSearchCV(RandomForestClassifier(random_state=0), param_grid, cv=5, n_jobs=-1)
    grid_search.fit(X_train, y_train)
    best_model = grid_search.best_estimator_
    print(f"Best parameters: {grid_search.best_params_}")
    print(f"Best CV score: {grid_search.best_score_:.4f}")

elif best_model_name == 'XGBoost':
    print("\nTuning XGBClassifier...")
    param_grid = {
        'n_estimators': [100, 200],
        'max_depth': [5, 7, 10],
        'learning_rate': [0.01, 0.1]
    }
    grid_search = GridSearchCV(XGBClassifier(random_state=0, use_label_encoder=False, eval_metric='logloss'), param_grid, cv=5, n_jobs=-1)
    grid_search.fit(X_train, y_train)
    best_model = grid_search.best_estimator_
    print(f"Best parameters: {grid_search.best_params_}")
    print(f"Best CV score: {grid_search.best_score_:.4f}")

else:
    best_model = trained_models[best_model_name]
    print(f"\nUsing {best_model_name} as-is (no tuning applied)")

# ==================== 7. FINAL MODEL EVALUATION ====================
print("\n" + "="*50)
print("Step 7: Final Model Evaluation...")
print("="*50)

y_pred_final = best_model.predict(X_test)
accuracy_final = accuracy_score(y_test, y_pred_final)
precision_final = precision_score(y_test, y_pred_final)
recall_final = recall_score(y_test, y_pred_final)
f1_final = f1_score(y_test, y_pred_final)
conf_matrix = confusion_matrix(y_test, y_pred_final)
class_report = classification_report(y_test, y_pred_final)

print(f"\nFinal Model Performance:")
print(f"Accuracy: {accuracy_final:.4f}")
print(f"Precision: {precision_final:.4f}")
print(f"Recall: {recall_final:.4f}")
print(f"F1-Score: {f1_final:.4f}")
print(f"\nConfusion Matrix:\n{conf_matrix}")
print(f"\nClassification Report:\n{class_report}")

# ==================== 8. SAVE THE MODEL ====================
print("\n" + "="*50)
print("Step 8: Saving the Model...")
print("="*50)

# Save model and encoder
with open('models/fraud_detection_model.pkl', 'wb') as f:
    pickle.dump(best_model, f)
    print("Model saved as 'models/fraud_detection_model.pkl'")

with open('models/label_encoder.pkl', 'wb') as f:
    pickle.dump(le, f)
    print("Label encoder saved as 'models/label_encoder.pkl'")

# Save feature names
with open('models/feature_names.pkl', 'wb') as f:
    pickle.dump(list(X.columns), f)
    print("Feature names saved as 'models/feature_names.pkl'")

print("\n" + "="*50)
print("Training Complete!")
print("="*50)
