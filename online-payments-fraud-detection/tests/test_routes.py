import unittest
from app.routes.fraud_detection_routes import app

class TestRoutes(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to the Online Payments Fraud Detection System', response.data)

    def test_predict(self):
        response = self.app.post('/predict')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Fraud Prediction', response.data)

    def test_submit(self):
        response = self.app.post('/submit')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Prediction Submitted', response.data)

if __name__ == '__main__':
    unittest.main()