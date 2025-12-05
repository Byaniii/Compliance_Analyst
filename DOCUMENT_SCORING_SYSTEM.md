# 📊 Document-Integrated Risk Scoring System

## Overview

Documents now **directly affect the final risk score**! The AI analyzes each uploaded document and adjusts the risk score based on whether documents support or contradict the form entries.

## ✅ How It Works

### Step 1: Rule-Based Assessment (Form Fields)
The system first calculates a **Base Risk Score** from form fields:
- Amount
- Source & Destination Countries
- Transaction Purpose
- Customer Type
- History Signals

**Example:**
- Vietnam → Indonesia
- $15,000
- Trade Finance
- SMB
- **Base Score: 63 (Medium Risk)**

### Step 2: Document Analysis
AI reviews each uploaded document and:
1. **Verifies** it supports the transaction
2. **Identifies** red flags or inconsistencies
3. **Calculates** score adjustment (-10 to +40 points)

### Step 3: Final Score Calculation
```
Final Risk Score = Base Score + Document Adjustments
```

**Example:**
- Base Score: 63
- Source of Funds: Well-documented (-5 points)
- Business Registration: Verified (-5 points)
- Invoice: Amounts match, legitimate (-3 points)
- **Document Adjustment: -13 points**
- **Final Score: 50 (Medium Risk, but lower)**

---

## 📈 Score Adjustment Rules

### 🟢 Negative Adjustments (Lower Risk) -5 to -10 points

**When documents STRONGLY support transaction:**
- ✅ All details match perfectly (amount, parties, dates)
- ✅ Established business with clean history
- ✅ Legitimate income source clearly shown
- ✅ Professional, complete documentation
- ✅ No red flags or concerns

**Examples:**
- **-10 points:** Perfect documentation, everything verified, high confidence
- **-7 points:** Good verification, minor missing details
- **-5 points:** Documents support transaction adequately

---

### 🟡 Neutral Adjustments (No Change) 0 to +5 points

**When documents are acceptable but raise minor concerns:**
- ⚠️ Some details can't be verified
- ⚠️ Documentation incomplete but not suspicious
- ⚠️ Minor inconsistencies with reasonable explanation
- ⚠️ Recent documents (but not suspicious timing)

**Examples:**
- **0 points:** Documents adequate, no impact
- **+3 points:** Minor concerns, needs follow-up
- **+5 points:** Partial verification, some gaps

---

### 🔴 Positive Adjustments (Higher Risk) +10 to +40 points

**When documents raise concerns or contradict form:**

#### +10 to +15 points: Moderate Concerns
- ⚠️ Amounts don't perfectly match (within 10% variance)
- ⚠️ Dates are inconsistent
- ⚠️ Documentation seems rushed or incomplete
- ⚠️ Can't fully verify all parties
- ⚠️ Business is relatively new (6-18 months)

#### +20 to +25 points: Significant Red Flags
- 🚨 Amounts significantly different (>10% variance)
- 🚨 Countries don't match stated transaction
- 🚨 Purpose contradicts documentation
- 🚨 Multiple small transactions suggesting structuring
- 🚨 Offshore jurisdiction involved
- 🚨 Anonymous ownership structures
- 🚨 Vague or generic documentation

#### +30 to +40 points: Critical Issues
- 🚨 Major contradictions between documents and form
- 🚨 Documents appear tampered or fake
- 🚨 Clear fraud indicators
- 🚨 Shell company characteristics
- 🚨 Money laundering patterns
- 🚨 Sanctions violations
- 🚨 Multiple severe red flags combined

---

## 🎯 Real Examples

### Example 1: ✅ Documents LOWER Risk

**Form Entry:**
- Amount: $18,000
- Vietnam → Indonesia
- Trade Finance
- SMB
- **Base Score: 63 (Medium)**

**Documents Uploaded:**
- ✅ Business Registration: 5 years old, legitimate trade company
- ✅ Source of Funds: Clean business bank account with consistent revenue
- ✅ Invoice: Professional PO for $18,000 electronics
- ✅ Owner ID: Vietnamese national, matches business

**AI Analysis:**
- Source of Funds: "Verified, consistent business revenue" (-5 points)
- Business Registration: "Established, legitimate" (-5 points)
- Invoice: "Matches amount and purpose perfectly" (-3 points)

**Final Result:**
- Document Adjustment: -13 points
- **Final Score: 50 (Medium, but lower confidence)**
- **Verdict: Approved with standard checks**

---

### Example 2: ⚠️ Documents INCREASE Risk

**Form Entry:**
- Amount: $15,000
- Singapore → Philippines
- Services
- Freelancer
- **Base Score: 25 (Low)**

**Documents Uploaded:**
- ⚠️ ID: Passport shows Nigeria (not Singapore as claimed!) 
- ⚠️ Bank Statement: Multiple $9,900 deposits (structuring pattern!)
- ⚠️ Invoice: Amount shows $12,000 (doesn't match $15,000 claim!)
- ⚠️ No proof of residency

**AI Analysis:**
- ID: "Country mismatch - claimed Singapore but passport Nigeria" (+15 points)
- Bank Statement: "Structuring pattern detected - multiple just under $10k" (+20 points)
- Invoice: "Amount discrepancy - shows $12k not $15k" (+10 points)

**Final Result:**
- Document Adjustment: +45 points
- **Final Score: 70 (HIGH RISK!)**
- **Risk Level upgraded from LOW to HIGH**
- **Verdict: FLAGGED for compliance review - inconsistencies detected**

---

### Example 3: 🚨 Documents Reveal Fraud

**Form Entry:**
- Amount: $30,000
- United States → Singapore
- Investment
- Corporate
- **Base Score: 55 (Medium)**

**Documents Uploaded:**
- 🚨 Business Registration: Cayman Islands (offshore, not US!)
- 🚨 Source of Funds: Vague sources, recent accumulation
- 🚨 Directors: Nominee directors, no real UBO
- 🚨 Investment docs: No specifics, generic template

**AI Analysis:**
- Business Reg: "Offshore jurisdiction not disclosed in form, shell company indicators" (+25 points)
- Source of Funds: "Cannot verify legitimate source, suspicious patterns" (+20 points)
- Investment docs: "Vague, no real business purpose" (+15 points)

**Final Result:**
- Document Adjustment: +60 points (capped at +40)
- **Final Score: 95 (VERY HIGH RISK)**
- **Verdict: REJECT - potential money laundering**

---

## 📊 Visual Display in UI

### Score Adjustment Section Shows:

```
┌──────────────────────────────────────────┐
│ 📊 Document Verification Impact          │
├──────────────────────────────────────────┤
│ Base Risk Score: 63                      │
│          ↓ -13                           │
│ Final Risk Score: 50                     │
│                                          │
│ Reason: Documents verified and support   │
│ transaction. Minor concerns addressed.   │
├──────────────────────────────────────────┤
│ Documents Reviewed: 3/3 Verified (100%)  │
│                                          │
│ ✅ Source of Funds Statement      -5pts  │
│ • Verified, consistent business revenue   │
│                                          │
│ ✅ Business Registration           -5pts  │
│ • Established, legitimate trade company  │
│                                          │
│ ✅ Contracts/Invoices             -3pts  │
│ • Amount matches perfectly               │
└──────────────────────────────────────────┘
```

### With Red Flags:

```
┌──────────────────────────────────────────┐
│ Base Risk Score: 25                      │
│          ↑ +45                           │
│ Final Risk Score: 70 (UPGRADED TO HIGH!) │
│                                          │
│ Reason: Critical inconsistencies found   │
├──────────────────────────────────────────┤
│ Documents Reviewed: 0/3 Verified (0%)    │
│                                          │
│ ⚠️ Proof of Identity              +15pts  │
│ • Country mismatch detected              │
│ Red Flags:                               │
│   • Passport shows Nigeria not Singapore │
│   • Claimed Singapore in form            │
│                                          │
│ ⚠️ Source of Funds                +20pts  │
│ • Structuring pattern detected           │
│ Red Flags:                               │
│   • Multiple transactions $9,900         │
│   • All just under $10k threshold        │
│                                          │
│ ⚠️ Contracts/Invoices             +10pts  │
│ Inconsistencies:                         │
│   • Invoice shows $12,000                │
│   • Form claims $15,000                  │
└──────────────────────────────────────────┘
```

---

## 🎯 Scoring Philosophy

### Documents Can:

**✅ Lower Risk (-10 max per document):**
- Strong verification
- Complete documentation
- Everything checks out
- High confidence

**⚠️ Increase Risk (+15 typical, +40 max):**
- Inconsistencies found
- Red flags detected
- Missing information
- Suspicious patterns

### Total Adjustments:
- **Maximum decrease:** -30 points (if 3+ docs all excellent)
- **Maximum increase:** +40 points per assessment (safety cap)
- **Typical range:** -15 to +20 points

---

## 🔍 What AI Checks Per Document

### 💰 Source of Funds Statement
**Verification:**
- ✅ Amount in bank statement matches transaction amount
- ✅ Source country matches stated origin
- ✅ Income pattern is legitimate and consistent
- ✅ No suspicious patterns

**Red Flags:**
- 🚨 Multiple transactions just under $10k (structuring)
- 🚨 Sudden large deposits with no explanation
- 🚨 Source country doesn't match claim
- 🚨 Round numbers only ($10,000, $20,000)
- 🚨 Cash deposits for large amounts

---

### 🪪 Proof of Identity
**Verification:**
- ✅ Name matches other documents
- ✅ Country matches stated nationality
- ✅ Document is valid and current
- ✅ No sanctions list concerns

**Red Flags:**
- 🚨 Country different from claimed origin
- 🚨 Multiple nationalities without explanation
- 🚨 Very recently issued ID
- 🚨 Document appears tampered

---

### 🏠 Proof of Residency
**Verification:**
- ✅ Address matches stated country
- ✅ Recent (< 3 months)
- ✅ Name consistent with ID
- ✅ Appropriate for claimed activity

**Red Flags:**
- 🚨 Address in different country than claimed
- 🚨 PO Box or mail forwarding service
- 🚨 Virtual office address
- 🚨 Doesn't match business type

---

### 🏢 Business Registration
**Verification:**
- ✅ Registered in stated country
- ✅ Business age appropriate (2+ years for medium amounts)
- ✅ Legitimate business type
- ✅ Clear ownership structure

**Red Flags:**
- 🚨 Offshore jurisdiction not disclosed
- 🚨 Very recently formed (< 6 months) handling large amounts
- 🚨 Shell company indicators
- 🚨 Bearer shares or anonymous ownership
- 🚨 Vague business purpose

---

### 📋 Contracts/Invoices/Payroll
**Verification:**
- ✅ Amount matches transaction exactly
- ✅ Parties match stated counterparties
- ✅ Purpose matches stated reason
- ✅ Professional and complete

**Red Flags:**
- 🚨 Amount significantly different
- 🚨 Parties don't match
- 🚨 Purpose contradicts claim
- 🚨 Generic template with no specifics
- 🚨 Unsigned or undated

---

## 🚀 For Your Mock Files Test

### Your Mock Files in `/mock_users/`:
1. Source_of_Funds.pdf
2. Proof_of_Identity.pdf
3. Proof_of_Residency.pdf
4. Business_Registration.pdf
5. Payroll_List.pdf

### Test Scenario Recommendations:

#### Test 1: Perfect Match (Should LOWER risk)
**Form:**
- Amount: Whatever is in Payroll_List.pdf
- Countries: Match what's in documents
- Purpose: Matches payroll/invoice

**Expected:**
- Base score: calculated from rules
- Document adjustment: -10 to -15 points
- Final score: Lower, approved

#### Test 2: Mismatch (Should INCREASE risk)
**Form:**
- Amount: $20,000 (but payroll shows $15,000)
- Countries: Different from documents
- Purpose: Investment (but documents show services)

**Expected:**
- Base score: from rules
- Document adjustment: +20 to +35 points
- Final score: HIGHER, flagged for review
- Specific inconsistencies listed

---

## 💡 Benefits of This Approach

### 1. **Catches Fraud**
- Form says $10,000, invoice shows $5,000 → +10 points
- Fake consistency means nothing - AI reads actual docs

### 2. **Rewards Good Compliance**
- Complete, professional docs → Lower score
- Faster approval for legitimate transactions

### 3. **Transparent**
- Shows exact score impact per document
- Lists specific reasons
- Auditable decision trail

### 4. **Flexible**
- AI adapts to context
- Considers document quality
- Weighs severity of issues

### 5. **Realistic**
- Mirrors real compliance workflow
- Documents matter (as they should!)
- Can't game the system

---

## 🎯 For Ripe Demo

### Demo Script:

**Show Form Entry:**
> "Here's a transaction - $15k from Vietnam to Indonesia for trade finance. Based on rules alone, this scores 63 - medium risk."

**Upload Documents:**
> "Now let's upload the supporting documents..."

*Upload 3-5 documents*

**Submit & Show Results:**
> "Watch what happens when the AI reviews the documents..."

*Show loading, then results*

**Scenario A - Good Documents:**
> "Look - the AI verified all documents support the transaction. Risk score adjusted DOWN by 13 points. From 63 to 50. Still medium, but shows strong documentation. Approved."

**Scenario B - Bad Documents:**
> "But watch this - if documents don't match..." 

*Show example with mismatched amounts*

> "The AI caught it! Invoice shows $12k but form claims $15k. Risk score adjusted UP by 10 points. Flagged for review. This is how we catch fraud at scale."

---

## 📋 Response Structure

```json
{
  "risk_score": 50,
  "risk_level": "Medium",
  "score_adjustment_applied": {
    "original_score": 63,
    "adjustment": -13,
    "final_score": 50,
    "reason": "Source of Funds: verified (-5) | Business Registration: legitimate (-5) | Invoice: matches (-3)"
  },
  "document_verification": {
    "documents_analyzed": 3,
    "verified_count": 3,
    "verification_rate": 100,
    "document_reviews": [
      {
        "document_type": "Source of Funds Statement",
        "analysis": {
          "verified": true,
          "confidence_level": "high",
          "notes": "Clean business bank account...",
          "red_flags": [],
          "inconsistencies": [],
          "score_adjustment": -5,
          "adjustment_reason": "Well-documented income"
        }
      }
    ],
    "score_adjustment": -13,
    "adjustment_reason": "All documents verified..."
  },
  "triggered_rules": [...],
  "rationale": "... Documents verified successfully, risk reduced by 13 points.",
  "checklist_items": [...]
}
```

---

## ⚙️ Tuning the System

### If Too Sensitive (Too many false positives):
- Reduce adjustment amounts
- Increase tolerance for minor mismatches
- Focus only on critical issues

### If Not Sensitive Enough (Missing fraud):
- Increase adjustment for red flags
- Lower tolerance for inconsistencies
- Weight critical documents more (Source of Funds, Business Reg)

### Current Settings (Balanced):
- Good docs: -5 to -10 per document
- Minor issues: 0 to +5
- Major issues: +10 to +25
- Critical fraud: +30 to +40

---

## 🚀 Try It Now!

**With Your Mock Files:**

1. **Go to:** http://localhost:8000

2. **Fill form** with transaction details

3. **Upload your 5 PDFs** from `/mock_users/`

4. **Submit**

5. **Watch the result:**
   - See base score
   - See document analysis
   - See score adjustment (↑ or ↓)
   - See final score
   - See each document's impact

**The AI will tell you if your documents support or contradict your form entries!**

---

## ✅ Summary

**What Changed:**
- ❌ Old: Documents were informational only
- ✅ New: Documents directly adjust risk score

**Score Calculation:**
```
Base Score (from form fields)
    +
Document Adjustments (-10 to +40 per doc)
    =
Final Risk Score (0-100)
```

**Benefits:**
- ✅ Holistic assessment
- ✅ Catches inconsistencies automatically
- ✅ Rewards good documentation
- ✅ Penalizes poor/fake documents
- ✅ More accurate risk rating

**Your system now has fully integrated document-based risk scoring! 🎉**

Test it with your mock files to see how documents affect the final risk assessment!
