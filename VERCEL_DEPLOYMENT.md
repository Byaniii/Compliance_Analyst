# 🚀 Vercel Deployment Guide

## ⚠️ Important Limitations on Vercel

**What Works:**
- ✅ Risk assessment (form-based)
- ✅ AI analysis
- ✅ Document upload and analysis
- ✅ Configurable rules
- ✅ Download test documents

**What Doesn't Work:**
- ❌ **Assessment History** (SQLite doesn't persist on serverless)
- ❌ **History page** (no data to show)
- ⚠️ **Long document processing** (may timeout after 60 seconds)

---

## 📋 Deployment Steps

### 1. Go to Vercel Dashboard
Visit: https://vercel.com

### 2. Import GitHub Repository
- Click "Add New Project"
- Select "Import Git Repository"
- Choose: `Byaniii/Compliance_Analyst`
- Click "Import"

### 3. Configure Environment Variables
**Add these variables:**
- **Key:** `OPENAI_API_KEY`
- **Value:** Your OpenAI API key
- Click "Add"

**Add second variable:**
- **Key:** `OPENAI_MODEL`  
- **Value:** `gpt-4o-mini`
- Click "Add"

### 4. Deploy
- Click "Deploy"
- Wait 2-3 minutes
- Get your live URL!

---

## ⚙️ What Was Changed for Vercel

### 1. Database Disabled
- SQLite doesn't work on serverless
- History features disabled
- Each request is stateless

### 2. Serverless Entry Point
- Created `api/index.py` as entry point
- Wrapped Flask app for Vercel

### 3. Dynamic Port
- App uses PORT from environment
- Required for Vercel

---

## 🎯 What Judges Can Test

Even without history, judges can test:

✅ **Main Functionality:**
1. Submit transactions with form
2. Upload documents
3. Get AI-powered risk assessment
4. See document verification
5. Download mock test files

✅ **Configuration:**
1. Visit `/configure`
2. Modify rules
3. Test assessments with new rules

❌ **Can't Test:**
- Viewing past assessments
- Statistics dashboard
- Assessment history

---

## 💡 Alternative: Include Screenshot/Video

Since history won't work on Vercel, consider:
1. **Take screenshots** of history page locally
2. **Record video** of full demo
3. **Add to README** or create `DEMO.md`

---

## 🚀 After Deployment

Your Vercel URL will be:
`https://compliance-analyst-[random].vercel.app`

**Share this URL with judges!**

They can:
- Test risk assessments
- Upload documents
- See AI analysis
- Download test files
- Try all 3 scenarios

---

## ⚠️ Known Issues on Vercel

1. **Document processing timeout**
   - If analyzing 5 large PDFs takes >60s, may fail
   - Solution: Test with fewer documents or smaller files

2. **No persistence**
   - Each assessment is independent
   - No audit trail
   - Consider adding "Results were not saved (serverless demo)" message

3. **Cold starts**
   - First request after idle may be slow (10-20s)
   - Subsequent requests faster

---

## 🎯 For Production

If this were production, you'd want:
- **Railway/Render** - Persistent database
- **Heroku** - Full app support
- **AWS/GCP** - Enterprise scale

But for demo/judging, Vercel works fine for the core assessment features!

---

**Deploy now and get your live URL in 3 minutes!** 🚀

