# ✅ New Document Workflow - Supporting Evidence Approach

## What Changed

The system now uses documents as **supporting evidence** for risk assessment, not as the primary data source. This is more aligned with real compliance workflows!

## 🔄 New Flow

### Old Way (Removed):
```
Upload Docs → Extract Data → Fill Form → Submit → Assess
```

### New Way (Better!):
```
Fill Form → Upload Supporting Docs → Submit → Assess with Document Context
```

## 📋 How It Works Now

### Step 1: User Fills Form
- Enter transaction details manually
- Use dropdown menus for countries
- Specify amount, purpose, counterparty type

### Step 2: Upload Supporting Documents (Optional)
- Attach compliance documents
- See count update: "Documents uploaded: 3"
- Documents are held client-side

### Step 3: Submit for Assessment
- Click "Submit for Compliance Review"
- If documents attached → calls `/api/risk-check-with-documents`
- If no documents → calls `/api/risk-check` (normal flow)

### Step 4: AI Analysis
**The AI now does TWO things:**

1. **Rule-Based Assessment** (always)
   - Applies compliance rules
   - Calculates risk score
   - Generates checklist

2. **Document Verification** (if documents uploaded)
   - Reviews each document
   - Checks if it supports the transaction
   - Identifies red flags or inconsistencies
   - Adds confidence level

## 🎯 What AI Checks in Documents

For each uploaded document, AI analyzes:

### ✅ Verification
- Does this document support the stated transaction?
- Are amounts consistent?
- Do countries match?
- Is the purpose verified?

### 🚩 Red Flags
- Inconsistencies with form data
- Missing information
- Suspicious patterns
- Tampered documents

### 📊 Confidence
- **High**: Document strongly supports transaction
- **Medium**: Document provides some support
- **Low**: Document raises questions

## 📦 Response Structure

### Without Documents:
```json
{
  "risk_score": 65,
  "risk_level": "Medium",
  "triggered_rules": [...],
  "rationale": "...",
  "checklist_items": [...],
  "ai_insights": {...}
}
```

### With Documents:
```json
{
  "risk_score": 65,
  "risk_level": "Medium",
  "triggered_rules": [...],
  "rationale": "...",
  "checklist_items": [...],
  "ai_insights": {...},
  "document_verification": {
    "documents_analyzed": 3,
    "document_reviews": [
      {
        "document_type": "Source of Funds Statement",
        "analysis": {
          "verified": true,
          "confidence_level": "high",
          "notes": "Bank statement shows consistent income...",
          "red_flags": []
        }
      },
      {
        "document_type": "Proof of Identity",
        "analysis": {
          "verified": true,
          "confidence_level": "high",
          "notes": "Valid passport, matches stated country",
          "red_flags": []
        }
      },
      {
        "document_type": "Contracts/Invoices",
        "analysis": {
          "verified": true,
          "confidence_level": "medium",
          "notes": "Invoice amount matches transaction",
          "red_flags": ["Invoice date is quite recent"]
        }
      }
    ],
    "overall_verification": "Documents provide supporting evidence..."
  },
  "documents_reviewed": 3
}
```

## 💡 Benefits of This Approach

### 1. Realistic Compliance Workflow
- ✅ Mirrors real KYC/AML processes
- ✅ Documents support, not replace, data entry
- ✅ Compliance officer reviews both

### 2. Better Accuracy
- ✅ User provides accurate transaction details
- ✅ Documents verify the details
- ✅ AI catches inconsistencies

### 3. Flexible
- ✅ Works with or without documents
- ✅ Optional document upload
- ✅ Can add documents later

### 4. More Insightful
- ✅ AI explains what each document shows
- ✅ Identifies specific red flags
- ✅ Provides confidence levels

## 🎯 Use Cases

### Case 1: Freelancer Payment (Low Risk)
**Form:**
- Amount: $3,000
- Singapore → Philippines
- Purpose: Services
- Type: Freelancer

**Documents:**
1. Passport (verifies Philippines resident)
2. Payroll invoice (verifies $3,000 payment)
3. Bank statement (shows legitimate income)

**Result:**
- Risk: Low
- Document verification: All verified ✓
- Confidence: High
- **Approved in seconds**

---

### Case 2: Suspicious Transaction (High Risk)
**Form:**
- Amount: $30,000
- Nigeria → Cayman Islands
- Purpose: Investment
- Type: NGO

**Documents:**
1. Business registration (recent, vague)
2. Source of funds (multiple small transactions)
3. Contract (no specific details)

**Result:**
- Risk: High
- Document verification: ⚠️ Red flags detected
  - "Registration is very recent"
  - "Multiple transactions just under $10k"
  - "Contract lacks specifics"
- Confidence: Low
- **Flagged for review**

---

### Case 3: No Documents Uploaded
**Form:**
- Amount: $15,000
- Vietnam → Indonesia
- Purpose: Trade Finance
- Type: SMB

**Documents:** None

**Result:**
- Risk: Medium
- Rule-based assessment only
- Checklist includes: "Please provide invoices"
- **Requires documentation before approval**

## 🚀 For Ripe Demo

### Demo Script:

**Setup:**
> "Ripe processes thousands of stablecoin settlements daily. Each needs compliance verification."

**Show Form:**
> "Compliance officer enters the transaction details here."

*Fill out form: $18,000, Vietnam → Indonesia, Trade Finance*

**Upload Documents:**
> "They attach supporting documents - business registration, invoices, bank statements."

*Upload 3-4 PDFs - watch count update*

**Submit:**
> "One click submits everything."

*Loading screen - 10-15 seconds*

**Show Results:**
> "Look at this - the AI analyzed the transaction AND verified all the documents. Here's what it found..."

*Scroll through document verification section*

> "For the business registration - verified, high confidence. For the invoice - amount matches, all good. For bank statement - shows legitimate business activity."

**Key Message:**
> "What would take a compliance team 30 minutes, Ripe does in 15 seconds. Same thoroughness, instant results. That's how we scale compliance for a $5T market."

## 📊 Technical Flow

```
Client Side:
1. User fills form
2. User uploads documents (stored in uploadedDocuments object)
3. User clicks submit
4. JavaScript checks: hasDocuments?
   - YES → POST to /api/risk-check-with-documents (FormData with transaction + files)
   - NO → POST to /api/risk-check (JSON with transaction only)

Server Side:
1. Receives request
2. Validates transaction data
3. Runs rule-based assessment
4. IF documents present:
   a. Convert PDFs to images
   b. For each document:
      - Send to OpenAI with context about transaction
      - AI verifies document supports transaction
      - Collect verification results
   c. Add document_verification to response
5. Save to database
6. Return enhanced result

Client Side:
7. Display results with document verification (if present)
```

## ✅ Summary

**What's Better:**
- ✅ Documents are supporting evidence, not primary data
- ✅ More realistic compliance workflow
- ✅ AI verifies documents against transaction
- ✅ Identifies inconsistencies and red flags
- ✅ Works with or without documents
- ✅ More insightful analysis

**User Experience:**
1. Fill form (easy, familiar)
2. Upload docs (optional, drag & drop)
3. Submit (one button)
4. Get comprehensive analysis (transaction + documents)

**Perfect for Ripe's compliance-first approach while maintaining speed and scale!** 🚀

