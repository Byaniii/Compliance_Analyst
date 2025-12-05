# ⚙️ Configurable Rules System

## Overview

The compliance system now has **fully configurable rules** with a beautiful UI! You can customize all risk criteria, thresholds, and scoring without touching code.

## 🎯 What You Can Configure

### 1. **Risk Categories** (Low/Medium/High)

For each risk level, you can configure:

#### Countries
- Add/remove countries to each risk tier
- Examples:
  - Low: Singapore, US, UK, Philippines
  - Medium: Vietnam, Indonesia, India
  - High: Cayman Islands, Nigeria, Iran, North Korea

#### Transaction Purposes
- Add/remove transaction types to each tier
- Examples:
  - Low: payroll, services
  - Medium: trade finance, remittance
  - High: investment, gambling, crypto trading

#### Score Points
- **Country Score**: Points added when country matches
  - Low: 5 points
  - Medium: 18 points
  - High: 35 points

- **Purpose Score**: Points added when purpose matches
  - Low: 3 points
  - Medium: 15 points
  - High: 28 points

- **Customer Score**: Points for customer type
  - Low (Freelancer): 5 points
  - Medium (SMB): 15 points
  - High (NGO/PEP): 40 points

### 2. **Amount Thresholds**

Configure when transaction amounts trigger alerts:

- **High-Risk Origin Threshold**: $10,000 (default)
  - Amount that triggers alert if from high-risk country

- **General High Threshold**: $25,000 (default)
  - Amount that triggers high-risk regardless of origin

- **Moderate Threshold**: $15,000 (default)
  - Amount that triggers moderate-risk flag

### 3. **Risk Score Thresholds**

Define what total score = Low/Medium/High:

- **Low Max Score**: 30 (default)
  - Scores 0-30 = Low Risk

- **Medium Max Score**: 70 (default)
  - Scores 31-70 = Medium Risk
  - Scores 71-100 = High Risk

## 🚀 How to Use

### Access Configuration Page

**URL:** http://localhost:8000/configure

Or click "⚙️ Configure Rules" from main page

### Step 1: Modify Risk Categories

**Add Country to High Risk:**
1. Go to "HIGH RISK" section
2. Type country name in "Add country..." field
3. Click "Add"
4. Country appears as a tag

**Remove Country:**
- Click the "×" on any country tag

**Same process for purposes!**

### Step 2: Adjust Score Points

**Example: Make low-risk countries worth fewer points**
1. In "LOW RISK" section
2. Find "Risk Score Points"
3. Change "Country Score" from 5 to 3
4. System will use new value

### Step 3: Update Thresholds

**Example: Lower high-risk threshold**
1. Go to "Amount & Score Thresholds"
2. Change "General High" from $25,000 to $20,000
3. Now $20k+ transactions = high risk

### Step 4: Save Configuration

1. Click **"💾 Save Configuration"** button
2. Success message appears
3. Rules immediately active for new assessments

### Reset to Defaults

- Click **"🔄 Reset to Defaults"**
- Confirms before resetting
- All rules return to original values

## 📊 Example Configuration Scenarios

### Scenario 1: Stricter Compliance

**Goal:** More conservative risk assessment

**Changes:**
- Lower thresholds:
  - High-risk origin: $10,000 → $5,000
  - General high: $25,000 → $15,000
- Increase scores:
  - High-risk country: 35 → 45
  - High-risk purpose: 28 → 35
- Lower risk level thresholds:
  - Low max: 30 → 20
  - Medium max: 70 → 50

**Result:** More transactions flagged as high-risk

---

### Scenario 2: Southeast Asia Focus

**Goal:** Optimize for Ripe's APAC markets

**Changes:**
- Move to low-risk:
  - Add: Thailand, Malaysia, Hong Kong
- Add to medium-risk:
  - Add: Myanmar, Cambodia, Bangladesh
- Add purposes:
  - Low: "freelance", "contractor payment"
  - Medium: "e-commerce", "marketplace"

**Result:** Better tuned for regional transactions

---

### Scenario 3: Crypto-Friendly

**Goal:** Support legitimate crypto businesses

**Changes:**
- Move "crypto trading" from high to medium risk
- Add to medium purposes:
  - "DeFi protocol", "NFT marketplace", "staking"
- Adjust scores:
  - Purpose medium: 15 → 12

**Result:** Legitimate crypto use cases get fairer assessment

---

### Scenario 4: Conservative Banking

**Goal:** Traditional bank compliance standards

**Changes:**
- Add more high-risk countries
- Lower all thresholds by 30%
- Increase all high-risk scores
- Move "investment" scoring higher

**Result:** Ultra-conservative assessment

## 🔧 Technical Details

### Storage

Rules stored in `rules_config.json`:
```json
{
  "high_risk_countries": [...],
  "medium_risk_countries": [...],
  "low_risk_countries": [...],
  "high_risk_purposes": [...],
  "amount_thresholds": {...},
  "risk_score_thresholds": {...}
}
```

### API Endpoints

**Get Rules:**
```bash
GET /api/rules
```

**Update Rules:**
```bash
POST /api/rules
Content-Type: application/json

{
  "high_risk_countries": [...],
  ...
}
```

**Reset to Defaults:**
```bash
POST /api/rules/reset
```

### Architecture

```
ConfigureUI (configure.html)
    ↓
API Endpoints (/api/rules)
    ↓
RulesManager (rules_manager.py)
    ↓
rules_config.json (persistent storage)
    ↓
ComplianceEngine (reads on init and reload)
    ↓
Risk Assessment (uses configured rules)
```

### Auto-Reload

When rules are saved:
1. Written to `rules_config.json`
2. `RulesManager` updates in-memory copy
3. `ComplianceEngine.reload_rules()` called
4. Next assessment uses new rules immediately

## 💡 Use Cases for Ripe

### Regulatory Changes

**Scenario:** New country added to FATF grey list

**Action:**
1. Go to configure page
2. Add country to "HIGH RISK"
3. Save
4. All new transactions from that country = high risk

**Time:** 30 seconds vs. code deployment

---

### Market Expansion

**Scenario:** Ripe launches in new Southeast Asian country

**Action:**
1. Add country to appropriate risk tier
2. Add local transaction purposes
3. Adjust thresholds for local currency
4. Save

**Result:** Instant support for new market

---

### A/B Testing

**Scenario:** Test different risk criteria

**Action:**
1. Export current rules (copy JSON)
2. Modify and test
3. Compare results
4. Keep best configuration

**Benefit:** Data-driven compliance tuning

---

### Audit Requirements

**Scenario:** Regulator requires documentation of rules

**Action:**
1. Access `/api/rules` endpoint
2. Export current configuration
3. Provide to auditors
4. Show configuration UI

**Benefit:** Full transparency and audit trail

## 🎯 Best Practices

### Testing Configuration Changes

1. **Test on development first**
   - Don't modify production rules directly
   - Test impact with sample transactions

2. **Document changes**
   - Keep notes on why rules were changed
   - Export rules before major changes

3. **Gradual adjustments**
   - Make small changes
   - Monitor impact
   - Iterate based on results

### Security Considerations

1. **Access control**
   - Restrict who can access `/configure`
   - Add authentication (future enhancement)

2. **Backup rules**
   - Keep copy of `rules_config.json`
   - Version control recommended

3. **Change logging**
   - Log who changed what when (future enhancement)
   - Audit trail for compliance

## 📊 Impact Simulation

Want to see impact before saving?

**Manual test:**
1. Make changes in UI
2. Open new tab to main page
3. Submit test transaction
4. DON'T save if results aren't good
5. Refresh config page to discard

**Future enhancement:**
- "Preview Impact" button
- Shows how existing assessments would change
- Simulation mode

## 🚀 Demo Script

**For Ripe Presentation:**

> "One unique feature of our compliance system - fully configurable rules without touching code."

*Open configuration page*

> "Here you can see all our risk criteria organized by level. Let's say we want to add a new country to our low-risk list..."

*Add "Hong Kong" to low-risk countries*

> "Just type it in, click add, and save. Now all Hong Kong transactions will be assessed as lower risk."

*Show amount thresholds*

> "We can adjust thresholds too. If we want to be more conservative with high-risk countries..."

*Change $10,000 to $7,500*

> "One click to save, and the engine immediately uses the new rules. No code deployment, no downtime."

*Go back to main page and run assessment*

> "And here's a transaction being assessed with our custom rules - instant."

**Key Message:** 
"This flexibility means Ripe can adapt to regulatory changes, new markets, and evolving risk landscapes in real-time. Not weeks for a code release - literally 30 seconds."

## ✅ Summary

**What You Can Configure:**
- ✅ Countries (Low/Medium/High risk)
- ✅ Transaction purposes (Low/Medium/High risk)
- ✅ Score points for each category
- ✅ Amount thresholds ($)
- ✅ Risk score thresholds (0-100)

**Benefits:**
- 🚀 Change rules in 30 seconds
- 🎯 No code deployment needed
- 📊 Immediate effect
- 🔒 Full audit trail (JSON storage)
- 💼 Business users can manage
- 🌍 Adapt to new markets instantly

**Perfect for Ripe's dynamic, global compliance needs!** ⚙️

