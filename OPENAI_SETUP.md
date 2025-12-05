# OpenAI Integration Setup Guide

## Overview
This system now uses OpenAI's GPT-4o-mini to provide enhanced risk analysis for AML/KYC compliance assessments. The AI provides contextual insights, identifies additional red flags, and offers recommendations beyond the rule-based system.

## Setup Steps

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

This will install:
- `openai` - OpenAI Python SDK
- `python-dotenv` - Environment variable management

### 2. Create `.env` File

Create a file named `.env` in the project root directory:

```bash
# Copy the example template
cp .env.example .env
```

Or create it manually with this content:

```
# OpenAI API Configuration
OPENAI_API_KEY=sk-your-actual-api-key-here
OPENAI_MODEL=gpt-4o-mini

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
```

### 3. Add Your OpenAI API Key

1. Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys)
2. Replace `sk-your-actual-api-key-here` with your actual key in `.env`
3. **IMPORTANT**: Never commit `.env` to version control (it's in `.gitignore`)

### 4. Test the Integration

Start the server:
```bash
python app.py
```

You should see:
```
✓ OpenAI integration enabled
 * Running on http://0.0.0.0:8000
```

If you see a warning instead:
```
⚠ OPENAI_API_KEY not set - using rule-based assessment only
```
Then check that your `.env` file exists and contains the correct API key.

## How It Works

### Rule-Based Assessment (Always Active)
The system first runs rule-based compliance checks:
- Country risk assessment
- Transaction purpose analysis
- Amount threshold checks
- Customer type evaluation
- Structuring pattern detection

### AI-Enhanced Analysis (When Enabled)
If OpenAI is configured, the system also provides:

1. **Enhanced Rationale**: Deeper contextual analysis considering:
   - Geopolitical factors
   - Current regulatory trends
   - Industry-specific patterns

2. **Additional Red Flags**: Identifies concerns that rules might miss:
   - Unusual transaction patterns
   - Context-specific risks
   - Emerging compliance issues

3. **Actionable Recommendations**: Specific steps for compliance teams:
   - Investigation priorities
   - Documentation requirements
   - Escalation guidance

4. **Risk Adjustment Suggestions**: AI may suggest score adjustments with justification

### API Response Format

With OpenAI enabled, responses include an `ai_insights` field:

```json
{
  "risk_score": 65,
  "risk_level": "Medium",
  "triggered_rules": ["..."],
  "rationale": "...",
  "checklist_items": ["..."],
  "ai_insights": {
    "enhanced_rationale": "Detailed AI analysis...",
    "additional_red_flags": [
      "Specific concern 1",
      "Specific concern 2"
    ],
    "recommendations": [
      "Action item 1",
      "Action item 2"
    ],
    "risk_adjustment": {
      "suggested_score": 70,
      "justification": "Reason for adjustment"
    },
    "confidence_level": "high"
  }
}
```

## Cost Considerations

- **Model**: gpt-4o-mini (cost-effective)
- **Tokens per request**: ~600-1000 tokens
- **Approximate cost**: $0.001-0.002 per transaction analysis
- **Fallback**: If OpenAI fails, system continues with rule-based assessment

## Troubleshooting

### Issue: "OpenAI initialization failed"
**Solution**: Check that:
- OpenAI package is installed: `pip install openai`
- API key is valid and not expired
- You have sufficient API credits

### Issue: API responses are slow
**Solution**: 
- Model is optimized (gpt-4o-mini)
- Consider caching for identical transactions
- Check your internet connection

### Issue: Rate limits exceeded
**Solution**:
- Implement request throttling
- Upgrade your OpenAI plan
- Add retry logic with exponential backoff

## Security Best Practices

✅ **DO**:
- Store API key in `.env` file
- Add `.env` to `.gitignore`
- Rotate API keys regularly
- Monitor API usage on OpenAI dashboard
- Use environment-specific keys (dev/prod)

❌ **DON'T**:
- Commit API keys to version control
- Share keys in chat/email
- Hardcode keys in source code
- Use production keys in development

## Disabling OpenAI Integration

To disable AI analysis and use only rule-based assessment:

1. Remove or comment out `OPENAI_API_KEY` in `.env`:
   ```
   # OPENAI_API_KEY=sk-...
   ```

2. Restart the application

The system will automatically fall back to rule-based assessment only.

