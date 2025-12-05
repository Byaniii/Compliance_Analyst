# Frontend Application - Setup & Running Guide

## Overview

The AML/KYC Compliance Review System now includes a complete web application with:
- **Backend**: Flask REST API (`/api/risk-check` endpoint)
- **Frontend**: Single-page application with transaction form and compliance review display
- **Integration**: Full end-to-end transaction assessment workflow

## Project Structure

```
/Users/yanyan/Documents/Code/Bounty/
├── app.py                          # Flask backend server
├── compliance_engine.py            # Compliance assessment logic
├── requirements.txt                # Python dependencies
├── run_app.sh                      # Startup script
├── setup.py                        # Package configuration
├── static/
│   ├── index.html                 # Main UI page
│   ├── style.css                  # Styling
│   ├── script.js                  # Frontend logic
└── venv/                          # Python virtual environment
```

## Prerequisites

- Python 3.8+
- pip (Python package installer)
- Modern web browser (Chrome, Firefox, Safari, Edge)

## Installation

### 1. Create Virtual Environment (if not already created)

```bash
cd /Users/yanyan/Documents/Code/Bounty
python3 -m venv venv
```

### 2. Install Dependencies

```bash
venv/bin/pip install -r requirements.txt
```

This installs:
- `flask` - Web framework
- `flask-cors` - Cross-origin resource sharing
- `pytest` - Testing framework

## Running the Application

### Quick Start

```bash
cd /Users/yanyan/Documents/Code/Bounty
bash run_app.sh
```

This will:
1. Activate the virtual environment
2. Install dependencies if needed
3. Start the Flask server on port 8000

### Manual Start

```bash
cd /Users/yanyan/Documents/Code/Bounty
venv/bin/python app.py
```

### Access the Application

Once running, open your browser to:
- **Local**: http://localhost:8000
- **Network**: http://<your-ip>:8000 (e.g., http://192.168.1.66:8000)

## How to Use

### 1. Fill Out Transaction Details

The form requires:
- **Amount** (USD): Transaction value (e.g., 15000)
- **Currency**: Select from dropdown (USD, EUR, GBP, CHF, CNY)
- **Source Country**: Enter country name (e.g., "Nigeria")
- **Destination Country**: Enter country name (e.g., "United States")
- **Purpose**: Select from dropdown:
  - Payroll
  - Remittance
  - Trade Finance
  - Services
  - Investment
  - Gambling
  - Crypto Trading
- **Counterparty Type**: Select from dropdown:
  - Freelancer (low-risk)
  - SMB (medium-risk)
  - Corporate (medium-risk)
  - NGO (high-risk)
- **Structuring Signals** (Optional): Describe any concerning patterns

### 2. Submit for Assessment

Click "Assess Compliance Risk" button

### 3. View Results

The application displays:
- **Risk Score**: 0-100 (color-coded)
  - 0-30: Green (Low)
  - 31-70: Orange (Medium)
  - 71-100: Red (High)
- **Risk Level**: Low, Medium, or High
- **Triggered Rules**: List of compliance rules that were activated
- **Assessment Rationale**: Explanation of the risk assessment
- **Compliance Checklist**: Specific actions required based on risk level

### 4. Assess Another Transaction

Click "← Assess Another Transaction" to reset the form

## API Endpoint Reference

### POST /api/risk-check

Performs compliance risk assessment on a transaction.

**Request:**
```json
{
  "amount": 15000,
  "currency": "USD",
  "source_country": "Nigeria",
  "destination_country": "United States",
  "purpose": "investment",
  "counterparty_type": "freelancer",
  "history_signals": ""
}
```

**Response:**
```json
{
  "risk_score": 100,
  "risk_level": "High",
  "triggered_rules": [
    "Origin country 'Nigeria' classified as high-risk",
    "Transaction purpose 'investment' classified as high-risk",
    "Amount $15,000.00 exceeds $10,000 from high-risk country"
  ],
  "rationale": "Origin country Nigeria is on the high-risk list. Transaction purpose 'investment' is classified as high-risk...",
  "checklist_items": [
    "Verify customer identity (KYC)",
    "Confirm transaction purpose",
    "Check sanctions lists (OFAC, UN, EU)",
    "Escalate to compliance officer for manual review",
    ...
  ]
}
```

### GET /api/health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy"
}
```

## Testing with curl

```bash
# Test health endpoint
curl http://localhost:8000/api/health

# Test risk assessment
curl -X POST http://localhost:8000/api/risk-check \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 50000,
    "currency": "USD",
    "source_country": "Syria",
    "destination_country": "United States",
    "purpose": "crypto trading",
    "counterparty_type": "ngo",
    "history_signals": "Multiple small transactions detected"
  }'
```

## Example Test Cases

### Low-Risk Transaction
```json
{
  "amount": 5000,
  "source_country": "United States",
  "destination_country": "United Kingdom",
  "purpose": "payroll",
  "counterparty_type": "freelancer"
}
```
Expected: Risk Score ~13 (Low)

### Medium-Risk Transaction
```json
{
  "amount": 18000,
  "source_country": "Vietnam",
  "destination_country": "United States",
  "purpose": "trade finance",
  "counterparty_type": "smb"
}
```
Expected: Risk Score ~63 (Medium)

### High-Risk Transaction
```json
{
  "amount": 50000,
  "source_country": "Nigeria",
  "destination_country": "United States",
  "purpose": "crypto trading",
  "counterparty_type": "ngo",
  "history_signals": "Structuring signals"
}
```
Expected: Risk Score 100 (High)

## Troubleshooting

### Port Already in Use

If you get "Address already in use" error:

```bash
# Find and kill process using port 8000
lsof -i :8000 | grep -v COMMAND | awk '{print $2}' | xargs kill -9

# Or use a different port by editing app.py
# Change: app.run(debug=True, host="0.0.0.0", port=8000)
# To: app.run(debug=True, host="0.0.0.0", port=8001)
```

### Module Not Found Error

If you get "ModuleNotFoundError: No module named 'compliance_engine'":

```bash
# Copy the compliance_engine to site-packages
cp compliance_engine.py venv/lib/python3.13/site-packages/
```

### Virtual Environment Issues

If the virtual environment is corrupted:

```bash
# Remove old venv
rm -rf venv

# Create new one
python3 -m venv venv
venv/bin/pip install -r requirements.txt
```

## Frontend Features

### Responsive Design
- Works on desktop, tablet, and mobile devices
- Clean, minimal UI
- Color-coded risk indicators

### Form Validation
- Required field validation
- Amount validation (must be > 0)
- Country name validation
- Real-time feedback

### Loading States
- Visual spinner during assessment
- Prevents double submission
- Clear error messages

### Results Display
- Risk score in visual circle
- Color coding (green/orange/red)
- Detailed rule triggers
- Actionable compliance checklist
- Rationale explanation

## Development

### File Structure

**app.py** - Flask application
- Routes: `/`, `/api/risk-check`, `/api/health`
- CORS enabled for cross-origin requests
- Stateless design for scalability

**index.html** - Main interface
- Form for transaction input
- Results display card
- Loading spinner
- Error messaging

**style.css** - Responsive styling
- Mobile-first design
- CSS Grid layout
- Gradient backgrounds
- Smooth animations

**script.js** - Frontend logic
- Form submission handling
- API integration with fetch()
- DOM manipulation
- Form validation
- Result rendering

## Production Considerations

⚠️ **Important Notes:**

1. **Not for Production**: This is a demo/educational system
2. **Real Compliance**: Integrate with actual OFAC, sanctions lists, and regulatory databases
3. **Authentication**: Add user authentication and authorization
4. **Logging**: Implement comprehensive audit logging
5. **HTTPS**: Use HTTPS in production
6. **Rate Limiting**: Add rate limiting to prevent abuse
7. **Error Handling**: Implement comprehensive error handling and recovery
8. **Database**: Add database for storing assessments
9. **Compliance Officer Review**: All high-risk transactions should be manually reviewed

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the compliance_engine.py for rule definitions
3. Check browser console for JavaScript errors
4. Review Flask logs for backend errors

## License

This is a demonstration project for educational purposes.
