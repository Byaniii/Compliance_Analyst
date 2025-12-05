# 🎯 Mock Documents for Testing - Judge's Guide

## Welcome!

This ZIP contains **12 mock compliance documents** across 3 risk scenarios to test the Bounty AML/KYC system.

---

## 📦 What's Included

```
low_risk/          4 PDFs - Legitimate freelancer
medium_risk/       4 PDFs - Established SMB  
high_risk/         4 PDFs - Suspicious offshore entity
```

---

## 🧪 3 Test Scenarios (5 minutes each)

### 🟢 TEST 1: LOW RISK (Score: 0-10)

**Scenario:** Filipino freelancer receiving payment from Singapore client

**1. Fill Form:**
- Amount: **$3,000**
- From: **Singapore**
- To: **Philippines**
- Purpose: **Services**
- Type: **Freelancer**
- History: (empty)

**2. Upload from `low_risk/` folder:**
- Source of Funds → `low_sof.pdf`
- Proof of Identity → `low_id.pdf`
- Proof of Residency → `low_residency.pdf`
- Contracts/Invoices → `low_invoice.pdf`
- (Skip Business Registration - optional for freelancers)

**3. Expected Result:**
- ✅ Base Score: ~13
- ✅ Documents verify everything: -10 to -15 points
- ✅ **Final: 0-5 (LOW RISK)**
- ✅ **Decision: Instant Approval**

---

### 🟡 TEST 2: MEDIUM RISK (Score: 50-60)

**Scenario:** Vietnamese SMB importing from Indonesian supplier

**1. Fill Form:**
- Amount: **$18,000**
- From: **Vietnam**
- To: **Indonesia**
- Purpose: **Trade Finance**
- Type: **SMB**
- History: (empty)

**2. Upload from `medium_risk/` folder:**
- Source of Funds → `medium_sof.pdf`
- Proof of Identity → `medium_id.pdf`
- Business Registration → `medium_business.pdf`
- Contracts/Invoices → `medium_invoice.pdf`
- (Skip Residency - optional)

**3. Expected Result:**
- ⚠️ Base Score: ~63
- ⚠️ Documents support transaction: -8 to -12 points
- ⚠️ **Final: 51-55 (MEDIUM RISK)**
- ⚠️ **Decision: Standard checks, likely approved**

---

### 🔴 TEST 3: HIGH RISK (Score: 95-100)

**Scenario:** Offshore company with suspicious patterns

**1. Fill Form:**
- Amount: **$35,000**
- From: **Cayman Islands**
- To: **Vietnam**
- Purpose: **Investment**
- Type: **NGO**
- History: **"multiple small transactions under $10k in past 2 weeks"**

**2. Upload from `high_risk/` folder:**
- Source of Funds → `high_sof.pdf` (shows structuring!)
- Proof of Identity → `high_id.pdf` (Nigerian director)
- Business Registration → `high_business.pdf` (offshore, anonymous)
- Contracts/Invoices → `high_investment.pdf` (vague terms)

**3. Expected Result:**
- 🚨 Base Score: ~98
- 🚨 Documents show red flags: +20 to +30 points
- 🚨 **Final: 100 (HIGH RISK)**
- 🚨 **Decision: REJECT or Extensive Review**

---

## 🎯 What to Look For

### Low Risk Test:
✅ Clean documents, everything matches
✅ Professional freelancer workflow
✅ AI verifies and lowers risk score
✅ Fast approval path

### Medium Risk Test:
⚠️ Legitimate business but needs verification
⚠️ Documents support the transaction
⚠️ Balanced risk assessment
⚠️ Standard compliance checks

### High Risk Test:
🚨 Multiple red flags in documents
🚨 Structuring patterns ($9,900 x 5)
🚨 Offshore + Anonymous ownership
🚨 AI increases risk score significantly
🚨 System catches suspicious activity

---

## 📊 Key System Features to Demonstrate

1. **Rule-Based + AI Hybrid**
   - Base score from rules
   - AI enhances with document analysis

2. **Document Verification**
   - AI reads PDFs visually
   - Checks quality and authenticity
   - Verifies against form data

3. **Score Adjustment**
   - Good docs lower risk
   - Bad docs increase risk
   - Transparent reasoning

4. **Fraud Detection**
   - Catches amount mismatches
   - Detects structuring
   - Identifies offshore risks

5. **Configurable Rules**
   - Visit /configure to see
   - Adjust thresholds real-time
   - No code deployment needed

---

## 💡 Demo Tips

**Start with Low Risk** - Show smooth UX for legitimate transactions

**Then Medium Risk** - Show balanced approach for business

**End with High Risk** - Show system catches bad actors

**Show History Page** - View all 3 assessments, compare scores

**Show Configure** - Demonstrate flexibility

---

## 🚀 Quick Start

1. Go to compliance system URL
2. Click "📥 Download Test Documents" (that's how you got this!)
3. Extract ZIP
4. Follow 3 test scenarios above
5. See the system in action!

---

**Questions? Each scenario should take 2-3 minutes to test.**
**Total demo time: 10-15 minutes to show all capabilities.**

Good luck! 🎯

