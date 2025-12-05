# 🧪 Testing Instructions - 3 Complete Scenarios

## ✅ PDFs Generated!

All 12 PDF files created in `/mock_users/` folders:

```
mock_users/
├── low_risk/          (4 PDFs)
├── medium_risk/       (4 PDFs)
└── high_risk/         (4 PDFs)
```

---

## 🟢 TEST 1: LOW RISK

### Form Input:
- **Amount:** $3,000
- **Source Country:** Singapore
- **Destination Country:** Philippines
- **Purpose:** Services
- **Counterparty Type:** Freelancer
- **History Signals:** (empty)

### Upload These PDFs:
1. **Source of Funds** → `low_risk/low_sof.pdf`
2. **Proof of Identity** → `low_risk/low_id.pdf`
3. **Proof of Residency** → `low_risk/low_residency.pdf`
4. **Contracts/Invoices** → `low_risk/low_invoice.pdf`
5. **Business Registration** → Skip (freelancer)

### Expected Result:
- Base Score: ~13
- Doc Adjustment: -10 to -15
- **Final: 0-5 (LOW RISK)** ✅

---

## 🟡 TEST 2: MEDIUM RISK

### Form Input:
- **Amount:** $18,000
- **Source Country:** Vietnam
- **Destination Country:** Indonesia
- **Purpose:** Trade Finance
- **Counterparty Type:** SMB
- **History Signals:** (empty)

### Upload These PDFs:
1. **Source of Funds** → `medium_risk/medium_sof.pdf`
2. **Proof of Identity** → `medium_risk/medium_id.pdf`
3. **Business Registration** → `medium_risk/medium_business.pdf`
4. **Contracts/Invoices** → `medium_risk/medium_invoice.pdf`
5. **Proof of Residency** → Skip (optional)

### Expected Result:
- Base Score: ~63
- Doc Adjustment: -8 to -12
- **Final: 51-55 (MEDIUM RISK)** ⚠️

---

## 🔴 TEST 3: HIGH RISK

### Form Input:
- **Amount:** $35,000
- **Source Country:** Cayman Islands
- **Destination Country:** Vietnam
- **Purpose:** Investment
- **Counterparty Type:** NGO
- **History Signals:** "multiple small transactions under $10k in past 2 weeks"

### Upload These PDFs:
1. **Source of Funds** → `high_risk/high_sof.pdf`
2. **Proof of Identity** → `high_risk/high_id.pdf`
3. **Business Registration** → `high_risk/high_business.pdf`
4. **Contracts/Invoices** → `high_risk/high_investment.pdf`
5. **Proof of Residency** → Skip

### Expected Result:
- Base Score: ~98
- Doc Adjustment: +20 to +30 (red flags detected!)
- **Final: 100 (HIGH RISK)** 🚨

---

## 🚀 Quick Test (5 Minutes Each)

1. Go to http://localhost:8000
2. Fill form with data above
3. Upload 4 PDFs from corresponding folder
4. Click submit
5. Watch the results!

**All 12 PDFs are ready to use!** 🎉

