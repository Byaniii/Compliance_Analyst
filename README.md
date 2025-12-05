# 🛡️ Bounty AML/KYC Compliance System

A complete AI-powered compliance review system for money transfers, featuring real-time risk assessment, document verification, and configurable rules. Built for Ripe's stablecoin-to-fiat settlement use case across Southeast Asia and APAC markets.

## ✨ Features

### 🎯 Core Capabilities
- **Dual Risk Assessment** - Rule-based engine + OpenAI-enhanced analysis
- **Document Verification** - AI analyzes 5 compliance documents (ID, bank statements, invoices, etc.)
- **Configurable Rules** - Web UI to customize risk criteria without code changes
- **Complete Audit Trail** - SQLite database stores all assessments
- **Beautiful UI** - Professional, mobile-responsive interface

### 🧠 AI-Powered Analysis
- **OpenAI Vision API** - Reads and critiques document quality
- **Smart Verification** - Detects inconsistencies between documents and form data
- **Score Adjustment** - Documents directly impact final risk score (-30 to +40 points)
- **Fraud Detection** - Identifies structuring, offshore risks, and suspicious patterns

### ⚙️ Configurable Compliance Rules
- **No-code configuration** via web interface
- **Three risk tiers** - Customize Low/Medium/High criteria
- **Live updates** - Changes take effect immediately
- **Duplicate prevention** - Smart conflict resolution

### 📊 Comprehensive Assessment
Each transaction receives:
- Risk Score (0-100)
- Risk Level (Low/Medium/High)
- Triggered Rules
- AI-Enhanced Rationale
- Document Verification Results
- Compliance Checklist

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
brew install poppler  # Required for PDF processing (macOS)
```

### 2. Set Up OpenAI API Key
```bash
python setup_env.py
```
Or manually create `.env`:
```
OPENAI_API_KEY=your-key-here
OPENAI_MODEL=gpt-4o-mini
```

### 3. Run the Application
```bash
python app.py
```

Visit: http://localhost:8000

---

## 🧪 Test with Mock Documents

**Download test documents** directly from the app:
- Click "📥 Download Test Documents" button
- Get 12 PDFs across 3 risk scenarios
- Follow included instructions

**Or use the included mock files:**
- `mock_users/low_risk/` - Legitimate freelancer (Score: 0-10)
- `mock_users/medium_risk/` - Established SMB (Score: 50-60)
- `mock_users/high_risk/` - Suspicious offshore entity (Score: 95-100)

---

## 📋 Risk Assessment Criteria

### Base Score (From Form Fields)

**Countries:**
- Low (+5): Singapore, US, UK, Philippines
- Medium (+18): Vietnam, Indonesia, India
- High (+35): Cayman Islands, Nigeria, Iran, North Korea, Syria

**Transaction Purpose:**
- Low (+3): Payroll, services
- Medium (+15): Trade finance, remittance
- High (+28): Investment, gambling, crypto trading

**Customer Type:**
- Freelancer: +5 | SMB: +15 | Corporate/NGO: +40

**Amount Thresholds:**
- > $10k from high-risk: +40
- > $15k: +15
- > $25k: +40

### Document Impact

**Good Documents:** -5 to -10 points each
- Professional, authentic, complete
- Matches form data perfectly
- No red flags

**Bad Documents:** +10 to +40 points each
- Poor quality, suspicious, incomplete
- Mismatches with form data
- Fraud indicators

**Final Score = Base + Document Adjustment**

---

## 🎯 Key Features for Ripe

### Southeast Asia Optimized
- 51+ countries with SEA prioritized
- Regional compliance understanding
- Stablecoin-to-e-wallet flows supported

### High-Volume Ready
- Fast assessments (5-30 seconds)
- Database scales to millions
- API-ready architecture

### Compliance-First
- Proper KYC/AML documentation
- Full audit trail
- Explainable AI decisions
- Regulatory-ready

---

## 📚 Documentation

- **Quick Start:** `QUICKSTART.md`
- **OpenAI Setup:** `OPENAI_SETUP.md`
- **Document Scoring:** `DOCUMENT_SCORING_SYSTEM.md`
- **Configurable Rules:** `CONFIGURABLE_RULES.md`
- **Test Scenarios:** `mock_users/TEST_INSTRUCTIONS.md`

---

## 🏗️ Architecture

```
Frontend (HTML/CSS/JS)
    ↓
Flask API
    ↓
├─ RulesManager (configurable rules)
├─ ComplianceEngine (rule-based assessment)
├─ OpenAI Client (AI enhancement + document analysis)
├─ PDF Converter (document handling)
└─ SQLite Database (audit trail)
```

---

## 🌐 API Endpoints

- `POST /api/risk-check` - Assess transaction (form only)
- `POST /api/risk-check-with-documents` - Assess with documents
- `GET /api/assessments` - Get all assessments
- `GET /api/statistics` - Get summary statistics
- `GET /api/rules` - Get current rules
- `POST /api/rules` - Update rules
- `GET /api/download-mock-documents` - Download test files

---

## 💰 Cost

Using OpenAI gpt-4o-mini:
- Basic assessment: ~$0.001-0.003
- With 5 documents: ~$0.01-0.02
- Very affordable for enhanced compliance

---

## 🎯 Use Cases

### Freelancer Payment (Low Risk)
- Filipino freelancer receiving $3k from Singapore client
- Documents verify identity and income
- **Result:** Instant approval

### SMB Trade (Medium Risk)
- Vietnamese company importing $18k from Indonesia
- Business registration and invoices verified
- **Result:** Standard checks, approved

### Suspicious Transaction (High Risk)
- Offshore company, $35k, structuring patterns
- Documents show red flags
- **Result:** Flagged for review/rejection

---

## 🔧 Tech Stack

- **Backend:** Python, Flask, SQLite
- **AI:** OpenAI GPT-4o-mini (Vision API)
- **Frontend:** Vanilla JavaScript, HTML5, CSS3
- **Document Processing:** pdf2image, Pillow, poppler
- **Configuration:** JSON-based rules

---

## 📝 License

MIT License - See LICENSE file

---

## 🚀 Built For

**Ripe's Vision:** Powering stablecoin-to-fiat settlement across Southeast Asia, connecting crypto wallets to e-wallets (GCash, etc.), serving freelancers, SMBs, and remittance recipients in a high-volume, cross-border environment.

**This system demonstrates:** How AI can make compliance fast, thorough, and scalable for a $5T+ e-wallet payments market.

---

## 📧 Contact

For questions or demo requests, please open an issue.

---

**⭐ Star this repo if you find it useful!**

