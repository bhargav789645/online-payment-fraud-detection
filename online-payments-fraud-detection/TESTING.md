# Testing Guide

## Pre-Testing Checklist

- [ ] Python 3.8+ installed
- [ ] All dependencies installed: `pip install -r requirements.txt`
- [ ] Training complete: `python training_script.py` ran successfully
- [ ] Model files exist in `models/` directory
- [ ] Flask app starts without errors: `python app/main.py`

## Test Cases

### Test 1: Home Page Load

**Steps:**
1. Start Flask app: `python app/main.py`
2. Open browser: `http://127.0.0.1:5000`

**Expected Result:**
- Page loads successfully
- Shows "Online Payments Fraud Detection" title
- Displays features section
- "Start Prediction" button visible
- Page is responsive

**Pass**: ✅ or ❌

---

### Test 2: Navigate to Prediction Form

**Steps:**
1. On home page, click "Start Prediction"
2. Or navigate to: `http://127.0.0.1:5000/predict`

**Expected Result:**
- Prediction form loads
- All input fields visible:
  - Step
  - Type (dropdown)
  - Amount
  - oldbalanceOrg
  - newbalanceOrig
  - oldbalanceDest
  - newbalanceDest
- "Analyze Transaction" and "Back Home" buttons present

**Pass**: ✅ or ❌

---

### Test 3: Safe Transaction Prediction

**Steps:**
1. Fill in the form with safe transaction data:
   ```
   Step: 1
   Type: TRANSFER
   Amount: 150.50
   Old Balance Origin: 2000.00
   New Balance Origin: 1849.50
   Old Balance Destination: 500.00
   New Balance Destination: 650.50
   ```
2. Click "Analyze Transaction"

**Expected Result:**
- Page displays "✅ SAFE TRANSACTION"
- Green background box
- Shows fraud probability (should be low, ~5-20%)
- Displays all transaction details
- Shows "Check Another Transaction" and "Back Home" buttons

**Pass**: ✅ or ❌

---

### Test 4: Fraudulent Transaction Prediction

**Steps:**
1. Navigate to prediction form
2. Fill with suspicious transaction:
   ```
   Step: 500
   Type: CASH_OUT
   Amount: 99999.00
   Old Balance Origin: 100000.00
   New Balance Origin: 1.00
   Old Balance Destination: 100.00
   New Balance Destination: 99999.00
   ```
3. Click "Analyze Transaction"

**Expected Result:**
- Page displays "🚨 FRAUDULENT TRANSACTION DETECTED"
- Red background box
- Shows high fraud probability (typically >80%)
- Displays all transaction details
- Shows confidence score

**Pass**: ✅ or ❌

---

### Test 5: Form Validation - Missing Fields

**Steps:**
1. Navigate to prediction form
2. Leave some fields empty (e.g., Amount)
3. Click "Analyze Transaction"

**Expected Result:**
- Browser shows HTML5 validation message
- Form prevents submission
- Shows "Please fill in all fields" error

**Pass**: ✅ or ❌

---

### Test 6: Form Validation - Invalid Type

**Steps:**
1. Navigate to prediction form
2. Select valid type from dropdown
3. Verify all 5 transaction types work:
   - CASH_IN
   - CASH_OUT
   - DEBIT
   - PAYMENT
   - TRANSFER

**Expected Result:**
- Dropdown has all 5 types
- Each type can be selected
- No errors when selecting

**Pass**: ✅ or ❌

---

### Test 7: API Endpoint - Safe Transaction

**Steps:**
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

**Expected Result:**
```json
{
  "success": true,
  "prediction": 0,
  "is_fraud": false,
  "fraud_probability": 0.05,
  "message": "Transaction is Safe"
}
```

**Pass**: ✅ or ❌

---

### Test 8: API Endpoint - Fraudulent Transaction

**Steps:**
```bash
curl -X POST http://127.0.0.1:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "step": 500,
    "type": "CASH_OUT",
    "amount": 999999.00,
    "oldbalanceOrg": 1000000.00,
    "newbalanceOrig": 1.00,
    "oldbalanceDest": 0.00,
    "newbalanceDest": 999999.00
  }'
```

**Expected Result:**
```json
{
  "success": true,
  "prediction": 1,
  "is_fraud": true,
  "fraud_probability": 0.95,
  "message": "Fraudulent Transaction Detected!"
}
```

**Pass**: ✅ or ❌

---

### Test 9: Edge Cases

**Test 9a: Zero Amount**
```
Amount: 0
All other fields normal
```
Expected: Should process without error

**Test 9b: Large Amount**
```
Amount: 9999999.99
All other fields normal
```
Expected: Should process without error

**Test 9c: Minimum Step**
```
Step: 1
All other fields normal
```
Expected: Should process normally

**Test 9d: Maximum Step**
```
Step: 744
All other fields normal
```
Expected: Should process normally

**Pass**: ✅ or ❌

---

### Test 10: Responsive Design

**Steps:**
1. Open browser to `http://127.0.0.1:5000`
2. Test on different screen sizes:
   - Desktop (1920x1080)
   - Tablet (768x1024)
   - Mobile (375x667)

**Expected Result:**
- Layout adjusts properly on each size
- Form fields are readable
- Buttons are clickable
- No horizontal scrolling needed
- Text is properly sized

**Pass**: ✅ or ❌

---

### Test 11: Navigation Flow

**Steps:**
1. Start at home page
2. Click "Start Prediction"
3. Submit a transaction
4. Click "Check Another Transaction"
5. Submit another
6. Click "Back Home"

**Expected Result:**
- Navigation works smoothly
- No broken links
- Page transitions are clean
- All buttons functional

**Pass**: ✅ or ❌

---

### Test 12: Error Handling

**Steps:**
Try to trigger errors:
1. Invalid JSON in API
2. Missing fields in API
3. Invalid transaction type in API
4. Non-numeric values for numeric fields

**Expected Result:**
- Appropriate error messages shown
- Application doesn't crash
- User is guided to fix the issue

**Pass**: ✅ or ❌

---

## Performance Testing

### Test 13: Prediction Speed

**Steps:**
1. Submit 10 transactions in quick succession
2. Measure time for each response

**Expected Result:**
- Each prediction completes in <500ms
- Web interface remains responsive
- No timeouts

**Pass**: ✅ or ❌

---

### Test 14: Memory Usage

**Steps:**
1. Run app for 30 minutes
2. Submit predictions continuously
3. Check memory consumption

**Expected Result:**
- Memory usage remains stable
- No memory leaks
- App doesn't crash

**Pass**: ✅ or ❌

---

## Browser Compatibility

Test on different browsers:
- [ ] Chrome/Edge (latest)
- [ ] Firefox (latest)
- [ ] Safari (if on Mac)
- [ ] Mobile browsers (iOS Safari, Chrome Mobile)

Expected: Application works on all modern browsers

---

## Final Verification Checklist

- [ ] All form fields accept valid input
- [ ] Predictions are accurate
- [ ] API returns correct JSON responses
- [ ] UI is responsive and visually appealing
- [ ] Error messages are clear
- [ ] Navigation flows smoothly
- [ ] Performance is acceptable
- [ ] No console errors in browser
- [ ] All buttons work correctly
- [ ] Forms can be submitted multiple times

---

## Reporting Results

### Sample Test Report

```
Date: 2024-02-16
Tester: [Your Name]
Platform: Windows 10, Python 3.10, Chrome Browser

Test Results:
├── Test 1: Home Page Load         ✅ PASS
├── Test 2: Navigation            ✅ PASS
├── Test 3: Safe Transaction      ✅ PASS
├── Test 4: Fraud Detection       ✅ PASS
├── Test 5: Form Validation       ✅ PASS
├── Test 6: Transaction Types     ✅ PASS
├── Test 7: API - Safe            ✅ PASS
├── Test 8: API - Fraud           ✅ PASS
├── Test 9: Edge Cases            ✅ PASS
├── Test 10: Responsive Design    ✅ PASS
├── Test 11: Navigation Flow      ✅ PASS
├── Test 12: Error Handling       ✅ PASS
├── Test 13: Performance          ✅ PASS
└── Test 14: Memory Usage         ✅ PASS

Issues Found: None

Overall Status: READY FOR DEPLOYMENT ✅
```

---

## Troubleshooting During Testing

| Issue | Solution |
|-------|----------|
| Model not loading | Run `python training_script.py` |
| Predictions wrong | Ensure model is trained correctly |
| Slow predictions | Check system resources |
| Form not submitting | Check browser console for errors |
| API returns 500 error | Check Flask console for error details |
| CSS not loading | Ensure `static/styles.css` exists |
| Templates not found | Verify `templates/` folder exists |

---

## Success Criteria

✅ All tests pass
✅ No critical errors
✅ Performance meets requirements
✅ UI is responsive
✅ Predictions are reasonable
✅ API works correctly
✅ Documentation is clear

---

**When all tests pass, the application is ready for deployment!**
