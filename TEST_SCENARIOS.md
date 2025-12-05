# Test Scenarios for Ripe Compliance Demo

## 🎯 Quick Test Cases with New Dropdowns

Use these scenarios to demonstrate the system with the improved country dropdown menus.

---

## 🟢 **Scenario 1: LOW RISK**
### Legitimate Freelancer Payment in Southeast Asia

**Transaction Details:**
- **Amount:** $3,000
- **Currency:** USD
- **Source Country:** 🇸🇬 Singapore
- **Destination Country:** 🇵🇭 Philippines
- **Purpose:** Payroll
- **Counterparty Type:** Freelancer
- **History Signals:** (leave empty)

**Expected Result:**
- ✅ Risk Score: ~13-20
- ✅ Risk Level: **Low**
- ✅ AI Insights: Legitimate cross-border payroll pattern common in SEA gig economy

**Demo Talking Points:**
- "This is a typical Ripe transaction - freelancer receiving payment via stablecoin-to-fiat settlement"
- "Singapore to Philippines corridor is high-volume for remote work payments"
- "Low risk profile allows for streamlined processing"

---

## 🟡 **Scenario 2: MEDIUM RISK**
### SMB Trade Finance in Emerging Market

**Transaction Details:**
- **Amount:** $15,000
- **Currency:** USD
- **Source Country:** 🇻🇳 Vietnam
- **Destination Country:** 🇮🇩 Indonesia
- **Purpose:** Trade Finance
- **Counterparty Type:** SMB
- **History Signals:** (leave empty)

**Expected Result:**
- ⚠️ Risk Score: ~50-65
- ⚠️ Risk Level: **Medium**
- ⚠️ AI Insights: Legitimate business activity but requires additional documentation

**Demo Talking Points:**
- "Medium-risk transaction needs simplified due diligence"
- "Vietnam-Indonesia trade corridor is growing rapidly"
- "AI identifies need for invoice/documentation verification"

---

## 🟡 **Scenario 3: MEDIUM RISK (Higher)**
### Remittance from Medium-Risk Country

**Transaction Details:**
- **Amount:** $18,000
- **Currency:** USD
- **Source Country:** 🇮🇳 India
- **Destination Country:** 🇵🇭 Philippines
- **Purpose:** Remittance
- **Counterparty Type:** SMB
- **History Signals:** (leave empty)

**Expected Result:**
- ⚠️ Risk Score: ~55-70
- ⚠️ Risk Level: **Medium**
- ⚠️ AI Insights: Common remittance corridor, verify purpose and business relationship

**Demo Talking Points:**
- "India-Philippines remittance is common but above $15k triggers enhanced checks"
- "System balances facilitating legitimate flows with compliance needs"
- "AI provides context-specific recommendations"

---

## 🔴 **Scenario 4: HIGH RISK**
### High-Value Investment from High-Risk Origin

**Transaction Details:**
- **Amount:** $30,000
- **Currency:** USD
- **Source Country:** 🇳🇬 Nigeria (High Risk)
- **Destination Country:** 🇸🇬 Singapore
- **Purpose:** Investment
- **Counterparty Type:** Corporate
- **History Signals:** (leave empty)

**Expected Result:**
- 🚨 Risk Score: 75-85
- 🚨 Risk Level: **High**
- 🚨 AI Insights: Multiple red flags, enhanced due diligence required

**Demo Talking Points:**
- "High-risk origin combined with investment purpose triggers immediate escalation"
- "Nigeria is known for sophisticated fraud schemes"
- "AI identifies specific concerns beyond rule-based system"

---

## 🔴 **Scenario 5: VERY HIGH RISK**
### Offshore Jurisdiction with Structuring Signals

**Transaction Details:**
- **Amount:** $28,000
- **Currency:** USD
- **Source Country:** 🇰🇾 Cayman Islands
- **Destination Country:** 🇻🇳 Vietnam
- **Purpose:** Investment
- **Counterparty Type:** NGO
- **History Signals:** "multiple small transactions under $10k in past week"

**Expected Result:**
- 🚨 Risk Score: 95-100
- 🚨 Risk Level: **High**
- 🚨 AI Insights: Potential structuring and layering, immediate compliance review required

**Demo Talking Points:**
- "Offshore jurisdiction + NGO + structuring = maximum scrutiny"
- "Just under $30k threshold combined with history suggests deliberate avoidance"
- "AI identifies this as potential money laundering pattern"
- "Would be flagged for immediate compliance officer review"

---

## 🌏 **Scenario 6: Ripe's Sweet Spot**
### High-Volume E-Wallet Transfer in SEA

**Transaction Details:**
- **Amount:** $5,000
- **Currency:** USD
- **Source Country:** 🇭🇰 Hong Kong
- **Destination Country:** 🇵🇭 Philippines
- **Purpose:** Services
- **Counterparty Type:** Freelancer
- **History Signals:** (leave empty)

**Expected Result:**
- ✅ Risk Score: ~15-25
- ✅ Risk Level: **Low**
- ✅ AI Insights: Typical crypto-to-e-wallet flow, standard checks sufficient

**Demo Talking Points:**
- "This is Ripe's target market - stablecoin to GCash settlement"
- "Hong Kong to Philippines is a major remittance corridor"
- "Low friction, fast settlement, full compliance"
- "Exactly the use case where stablecoins replace slow traditional rails"

---

## 🔄 **Scenario 7: Cross-Regional Corporate**
### US Company Paying Asian Supplier

**Transaction Details:**
- **Amount:** $22,000
- **Currency:** USD
- **Source Country:** 🇺🇸 United States
- **Destination Country:** 🇹🇭 Thailand
- **Purpose:** Trade Finance
- **Counterparty Type:** SMB
- **History Signals:** (leave empty)

**Expected Result:**
- ⚠️ Risk Score: ~45-55
- ⚠️ Risk Level: **Medium**
- ⚠️ AI Insights: Legitimate B2B payment, verify invoices and contracts

**Demo Talking Points:**
- "US-Asia trade flows benefit from stablecoin rails"
- "Faster settlement than traditional SWIFT"
- "Still needs compliance checks for amounts over $20k"

---

## 🚩 **Scenario 8: Sanctions Risk**
### Transaction Involving Sanctioned Country

**Transaction Details:**
- **Amount:** $12,000
- **Currency:** USD
- **Source Country:** 🇮🇷 Iran (High Risk)
- **Destination Country:** 🇦🇪 UAE
- **Purpose:** Services
- **Counterparty Type:** Corporate
- **History Signals:** (leave empty)

**Expected Result:**
- 🚨 Risk Score: 80-90
- 🚨 Risk Level: **High**
- 🚨 AI Insights: Sanctions screening required, potential OFAC violation

**Demo Talking Points:**
- "Iran transactions require immediate sanctions screening"
- "System automatically flags for regulatory review"
- "Demonstrates compliance-first approach"
- "AI provides specific sanctions list references"

---

## 📊 Demo Flow Recommendation

### For a 5-Minute Demo:
1. **Start with Scenario 6** (Ripe's sweet spot) - Show it works
2. **Run Scenario 2** (Medium risk) - Show balanced approach
3. **Run Scenario 5** (Very high risk) - Show system catches bad actors
4. **Go to History Page** - Show all three assessments
5. **Expand the high-risk one** - Show AI insights and JSON

### For a 10-Minute Demo:
1. Run Scenarios 1, 2, 4, 5, 6 (mix of all risk levels)
2. Show History Page with statistics
3. Expand 2-3 assessments showing AI insights
4. Copy JSON to show API integration capability
5. Discuss how this fits Ripe's $5T+ market opportunity

---

## 🌍 Country Coverage in Dropdowns

### Organized by Region:
1. **Southeast Asia (8 countries)** - Ripe's core market
2. **Asia Pacific (10 countries)** - Expansion markets
3. **North America (3 countries)** - Major source markets
4. **Europe (9 countries)** - Financial hubs
5. **Middle East (6 countries)** - Including high-risk jurisdictions
6. **Africa (4 countries)** - Growing markets + high-risk
7. **Latin America (4 countries)** - Emerging crypto adoption
8. **Offshore/High Risk (7 jurisdictions)** - Compliance testing

### Total: 51 countries covering:
- ✅ All major remittance corridors
- ✅ Key crypto adoption markets
- ✅ High-risk jurisdictions for testing
- ✅ Ripe's target APAC/SEA markets

---

## 🎯 Key Demo Messages

1. **"Built for Ripe's Market"**
   - Southeast Asia prominence in dropdown
   - Understands regional compliance nuances
   - Optimized for stablecoin-to-e-wallet flows

2. **"AI-Enhanced, Not AI-Dependent"**
   - Rule-based system always works
   - AI adds contextual intelligence
   - Graceful fallback if AI unavailable

3. **"Compliance at Scale"**
   - Database stores all assessments
   - Audit trail with timestamps
   - API-ready for integration

4. **"Risk-Based Approach"**
   - Low risk = low friction
   - High risk = appropriate scrutiny
   - Balanced for business + compliance

---

**Pro Tip:** Start with low-risk scenarios to show smooth user experience, then demonstrate high-risk scenarios to show robust compliance. End with the history page to show scale and auditability.

