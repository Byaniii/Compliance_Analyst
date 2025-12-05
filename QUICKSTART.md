# Quick Start Guide - OpenAI Integration

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Set Up Your OpenAI API Key

### Option A: Interactive Setup (Recommended)
```bash
python setup_env.py
```

This will:
- Guide you through creating your `.env` file
- Prompt for your OpenAI API key
- Let you choose which model to use
- Set proper file permissions

### Option B: Manual Setup
1. Create a `.env` file in the project root
2. Add your API key:
```
OPENAI_API_KEY=sk-your-actual-key-here
OPENAI_MODEL=gpt-4o-mini
FLASK_ENV=development
FLASK_DEBUG=True
```

## Step 3: Run the Application

```bash
python app.py
```

You should see:
```
✓ OpenAI integration enabled
 * Running on http://0.0.0.0:8000
```

## Step 4: Test It

Open your browser to `http://localhost:8000` and submit a transaction.

The response will now include `ai_insights` with:
- Enhanced risk analysis
- Additional red flags to investigate
- Specific compliance recommendations
- AI confidence level

## Example API Response

```json
{
  "risk_score": 65,
  "risk_level": "Medium",
  "triggered_rules": [
    "Origin country 'Nigeria' classified as high-risk",
    "Amount $15,000 is above moderate threshold"
  ],
  "rationale": "Origin country Nigeria is on the high-risk list...",
  "checklist_items": [
    "Verify customer identity (KYC)",
    "Check sanctions lists (OFAC, UN, EU)",
    "Perform simplified due diligence (SDD)"
  ],
  "ai_insights": {
    "enhanced_rationale": "Nigeria presents elevated risk due to active fraud schemes...",
    "additional_red_flags": [
      "Purpose 'investment' combined with high-risk origin warrants scrutiny",
      "Amount falls in common structuring range"
    ],
    "recommendations": [
      "Verify source of funds documentation",
      "Check for related party transactions",
      "Review customer's historical transaction patterns"
    ],
    "risk_adjustment": {
      "suggested_score": 70,
      "justification": "Combination of factors suggests elevated risk"
    },
    "confidence_level": "high"
  }
}
```

## What's Different?

### Before (Rule-Based Only)
- ✓ Fast and deterministic
- ✓ Based on predefined rules
- ✗ Limited contextual understanding
- ✗ Can't adapt to new patterns

### After (Rule-Based + AI)
- ✓ Everything from before
- ✓ **Contextual analysis** of geopolitical factors
- ✓ **Pattern recognition** beyond simple rules
- ✓ **Natural language insights** for compliance teams
- ✓ **Adaptive recommendations** based on current trends
- ✓ **Confidence scoring** for assessments

## Cost Estimate

Using gpt-4o-mini:
- ~$0.001-0.002 per transaction analysis
- 1,000 transactions = ~$1-2
- Very cost-effective for enhanced insights

## Need Help?

See `OPENAI_SETUP.md` for detailed documentation including:
- Security best practices
- Troubleshooting common issues
- Configuration options
- How to disable OpenAI if needed

