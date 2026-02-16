# config.py
"""
Configuration file for Fraud Detection System
"""

import os

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fraud_detection_secret_key_2024'
    DEBUG = False
    TESTING = False
    MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models', 'fraud_detection_model.pkl')
    ENCODER_PATH = os.path.join(os.path.dirname(__file__), 'models', 'label_encoder.pkl')
    FEATURES_PATH = os.path.join(os.path.dirname(__file__), 'models', 'feature_names.pkl')
    DATA_PATH = os.path.join(os.path.dirname(__file__), 'data', 'raw_data.csv')


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
