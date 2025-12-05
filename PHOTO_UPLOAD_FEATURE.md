# 📸 Photo Upload Feature

## Overview

Users can now assess transactions by simply uploading a photo! The system uses **OpenAI Vision API** to extract transaction details from screenshots, receipts, invoices, or any transaction document.

## ✨ What You Can Upload

### Supported Images:
- 📱 **E-wallet screenshots** (GCash, PayMaya, Grab, etc.)
- 💳 **Bank transaction screenshots**
- 🧾 **Invoices and receipts**
- 📄 **Wire transfer confirmations**
- 💼 **Payment app screenshots** (Wise, PayPal, Venmo, etc.)
- 📊 **Transaction statements**
- 📸 **Any document showing transaction details**

### File Requirements:
- ✅ **Formats:** JPG, PNG, HEIC
- ✅ **Max size:** 10MB
- ✅ **Quality:** Clear and readable text

## 🎯 How It Works

### User Flow:

1. **Upload Photo**
   - Click the upload box or drag & drop
   - Photo preview appears

2. **AI Analysis**
   - Click "Analyze Photo"
   - OpenAI Vision API extracts details
   - Takes 2-5 seconds

3. **Auto-Populate**
   - Form fields automatically filled
   - Review and adjust if needed
   - Submit for assessment

### What Gets Extracted:

The AI identifies and extracts:
- 💰 **Amount** - Transaction value
- 💱 **Currency** - USD, EUR, PHP, SGD, etc.
- 🌏 **Source Country** - Where money comes from
- 🌍 **Destination Country** - Where money goes to
- 📝 **Purpose** - Reason for transaction
- 👤 **Counterparty Type** - Freelancer, SMB, Corporate, NGO
- 🚩 **History Signals** - Any suspicious patterns mentioned

## 🚀 Try It Now!

### Test with Screenshots:

**Example 1: E-Wallet Screenshot**
- Take a screenshot of GCash/PayMaya transaction
- Upload it
- Watch the fields auto-populate!

**Example 2: Invoice**
- Upload a business invoice
- AI extracts amount, parties, purpose
- Review and submit

**Example 3: Bank Transfer**
- Screenshot of wire transfer
- AI reads all transaction details
- Instant risk assessment

## 🎨 UI Features

### Upload Area:
```
┌─────────────────────────────────────┐
│            📷                       │
│   Click to upload or drag & drop   │
│  Supports: JPG, PNG, HEIC (Max 10MB)│
└─────────────────────────────────────┘
```

### With Photo:
```
┌─────────────────────────────────────┐
│   [Photo Preview]                   │
│                                     │
│  [Remove Photo] [Analyze Photo]    │
└─────────────────────────────────────┘
```

### During Analysis:
```
┌─────────────────────────────────────┐
│         ⟳ Loading...               │
│  Analyzing image and extracting     │
│  transaction details...             │
└─────────────────────────────────────┘
```

## 🧠 AI Intelligence

### Vision API Capabilities:

1. **Text Recognition**
   - Reads text in any orientation
   - Handles multiple languages
   - Works with handwriting (limited)

2. **Context Understanding**
   - Identifies transaction elements
   - Understands payment app layouts
   - Recognizes invoice formats

3. **Smart Extraction**
   - Separates amount from currency
   - Identifies country names
   - Classifies transaction purpose
   - Detects suspicious patterns

4. **Conservative Approach**
   - Only extracts what it's confident about
   - Marks uncertain fields as null
   - User reviews before submission

## 💡 Use Cases for Ripe

### 1. Freelancer Payments
**Scenario:** Freelancer receives payment via GCash
- Takes screenshot of transaction
- Uploads to compliance system
- Auto-assessed and approved in seconds
- ✅ Fast onboarding, minimal friction

### 2. SMB Invoice Processing
**Scenario:** Small business needs to send trade payment
- Uploads invoice PDF screenshot
- System extracts supplier details
- Compliance check performed
- ✅ Streamlined B2B payments

### 3. Remittance from Abroad
**Scenario:** OFW sending money home
- Screenshot from remittance app
- Uploads for compliance check
- Details extracted, risk assessed
- ✅ Faster processing for legitimate transfers

### 4. Compliance Review
**Scenario:** Suspicious transaction flagged
- User uploads supporting documents
- AI extracts details for review
- Compliance officer sees full picture
- ✅ Better decision-making

## 🔧 Technical Details

### Backend Endpoint:
```
POST /api/analyze-photo
Content-Type: multipart/form-data
```

**Request:**
```
Form Data:
- photo: [image file]
```

**Response:**
```json
{
  "extracted_data": {
    "amount": 15000,
    "currency": "USD",
    "source_country": "Singapore",
    "destination_country": "Philippines",
    "purpose": "services",
    "counterparty_type": "freelancer",
    "history_signals": ""
  },
  "message": "Transaction details extracted successfully"
}
```

### OpenAI Vision API:
- **Model:** gpt-4o-mini (cost-effective, fast)
- **Temperature:** 0.2 (consistent, factual)
- **Max Tokens:** 500
- **Response Format:** Structured JSON

### Process Flow:
```
1. User uploads image
   ↓
2. Frontend sends to /api/analyze-photo
   ↓
3. Backend encodes image as base64
   ↓
4. Sends to OpenAI Vision API
   ↓
5. AI analyzes and extracts data
   ↓
6. Backend parses JSON response
   ↓
7. Returns extracted data
   ↓
8. Frontend populates form fields
   ↓
9. User reviews and submits
   ↓
10. Normal risk assessment flow
```

## 💰 Cost Considerations

### Per Image Analysis:
- **OpenAI Vision API:** ~$0.002-0.005 per image
- **Very affordable** for enhanced UX
- **Optional feature** - manual entry still available

### Value Proposition:
- ⬆️ **Faster onboarding** - Seconds vs minutes
- ⬇️ **Fewer errors** - AI reads accurately
- ⬆️ **Better UX** - Mobile-first workflow
- ⬇️ **Lower abandonment** - Easy upload vs tedious typing

## 🎯 Perfect for Demo

### Demo Script:

**"Watch this - instead of typing all the details..."**

1. Pull up e-wallet screenshot on phone
2. Upload to compliance system
3. Click "Analyze Photo"
4. **"See? The AI just read everything!"**
5. Show auto-populated form
6. Submit for instant assessment
7. **"That's how Ripe makes compliance effortless."**

### Key Messages:

1. **"Mobile-First Compliance"**
   - Users live on mobile devices
   - Screenshots are natural workflow
   - No desktop required

2. **"AI-Powered Extraction"**
   - Vision AI reads any document
   - Works across payment platforms
   - Multilingual support

3. **"Speed + Accuracy"**
   - 5 seconds vs 2 minutes manual entry
   - Fewer typos and errors
   - Better user experience

4. **"Still Compliance-First"**
   - Same rigorous assessment
   - User reviews before submit
   - Full audit trail

## 🔒 Security & Privacy

### Image Handling:
- ✅ **Not stored** - Analyzed and discarded
- ✅ **Secure transmission** - HTTPS only
- ✅ **No logging** - Images not saved to database
- ✅ **OpenAI compliance** - Enterprise-grade security

### Data Privacy:
- Only extracted transaction details stored
- Original images never persisted
- Compliant with GDPR/data protection laws

## 📝 Tips for Best Results

### For Users:

1. **Clear Photos**
   - Good lighting
   - No glare or shadows
   - Entire transaction visible

2. **Screenshot Tips**
   - Capture full screen
   - Include all relevant details
   - Crop out personal info (optional)

3. **Supported Languages**
   - English (best)
   - Chinese, Japanese, Korean
   - Most major languages work

### If Extraction Fails:

- ✅ **Fallback to manual entry** - Always available
- ✅ **Partial extraction** - Fill in missing fields
- ✅ **Try again** - Different angle/quality might work

## 🚀 Future Enhancements

Possible improvements:
- [ ] Batch upload (multiple photos)
- [ ] PDF document support
- [ ] Real-time camera capture
- [ ] OCR confidence scores
- [ ] Multi-page document scanning
- [ ] Template learning (common formats)
- [ ] Offline OCR (privacy-focused)

## 📊 Metrics to Track

### Adoption:
- % of assessments via photo vs manual
- Upload success rate
- Extraction accuracy

### Performance:
- Average analysis time
- User satisfaction scores
- Error/retry rates

### Business Impact:
- Reduced onboarding time
- Lower abandonment rate
- Higher transaction volume

## ✅ Current State

**Status:** ✅ **Fully Implemented and Working**

What's live:
- ✅ Photo upload UI with drag & drop
- ✅ Image preview
- ✅ OpenAI Vision API integration
- ✅ Transaction detail extraction
- ✅ Auto-form population
- ✅ Error handling and fallbacks
- ✅ Mobile-responsive design

**Ready for demo and production use!**

## 🎉 Summary

You can now assess transactions in **two ways**:

1. **📸 Quick Photo Upload**
   - Snap a screenshot
   - Upload it
   - Let AI extract details
   - Submit for assessment
   - ⏱️ Takes ~10 seconds

2. **📝 Manual Entry**
   - Fill in form fields
   - Use dropdown menus
   - Submit for assessment
   - ⏱️ Takes ~2 minutes

**Both methods:**
- ✅ Same rigorous compliance checks
- ✅ AI-enhanced risk analysis
- ✅ Stored in database
- ✅ Full audit trail
- ✅ JSON API access

---

**This feature makes your compliance system truly cutting-edge! 🚀**

Perfect for Ripe's mobile-first, high-volume use case where users transact via e-wallets and need fast, frictionless compliance.

