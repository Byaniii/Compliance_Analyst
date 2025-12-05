"""
Flask backend for AML/KYC Compliance Review System
Provides REST API endpoint for risk assessment
"""

import sys
import os
from pathlib import Path

# Add current directory to path so we can import local modules
current_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(current_dir))

from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
from compliance_engine import ComplianceEngine, Transaction, CustomerType
from config import Config
from database import AssessmentDB
from rules_manager import RulesManager
import base64
import json
import io
import zipfile
import tempfile
from pathlib import Path
from PIL import Image
try:
    from pdf2image import convert_from_bytes
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False

app = Flask(__name__, static_folder='static', static_url_path='/static')
CORS(app)

# Initialize database
db = AssessmentDB()

# Initialize rules manager
rules_manager = RulesManager()

# Initialize OpenAI client if API key is available
openai_client = None
if Config.is_openai_enabled():
    try:
        from openai import OpenAI
        openai_client = OpenAI(api_key=Config.OPENAI_API_KEY)
        print("✓ OpenAI integration enabled")
    except Exception as e:
        print(f"⚠ OpenAI initialization failed: {e}")
        print("  Continuing with rule-based assessment only")
else:
    print("⚠ OPENAI_API_KEY not set - using rule-based assessment only")
    print("  To enable AI-enhanced analysis, add OPENAI_API_KEY to .env file")

# Initialize compliance engine with rules manager
engine = ComplianceEngine(openai_client=openai_client, rules_manager=rules_manager)


def parse_customer_type(customer_str: str) -> CustomerType:
    """Convert customer type string to enum"""
    mapping = {
        "freelancer": CustomerType.LOW,
        "smb": CustomerType.MEDIUM,
        "corporate": CustomerType.MEDIUM,
        "ngo": CustomerType.HIGH,
    }
    return mapping.get(customer_str.lower(), CustomerType.MEDIUM)


@app.route("/", methods=["GET"])
def index():
    """Serve the main HTML page"""
    return send_from_directory("static", "index.html")


@app.route("/api/risk-check", methods=["POST"])
def risk_check():
    """
    Perform compliance risk assessment on a transaction
    
    Expected JSON input:
    {
        "amount": number,
        "currency": string,
        "source_country": string,
        "destination_country": string,
        "purpose": string,
        "counterparty_type": string,
        "history_signals": string (optional)
    }
    
    Returns JSON:
    {
        "risk_score": number,
        "risk_level": string,
        "triggered_rules": [string],
        "rationale": string,
        "checklist_items": [string]
    }
    """
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = [
            "amount",
            "source_country",
            "destination_country",
            "purpose",
            "counterparty_type",
        ]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        # Parse and validate data
        try:
            amount = float(data.get("amount", 0))
        except (ValueError, TypeError):
            return jsonify({"error": "Invalid amount"}), 400

        if amount < 0:
            return jsonify({"error": "Amount must be positive"}), 400

        source_country = data.get("source_country", "").strip()
        destination_country = data.get("destination_country", "").strip()
        purpose = data.get("purpose", "").strip()
        counterparty_type = data.get("counterparty_type", "").strip()
        history_signals = data.get("history_signals", "").strip()

        if not source_country:
            return jsonify({"error": "Source country is required"}), 400
        if not destination_country:
            return jsonify({"error": "Destination country is required"}), 400
        if not purpose:
            return jsonify({"error": "Purpose is required"}), 400
        if not counterparty_type:
            return jsonify({"error": "Counterparty type is required"}), 400

        # Convert counterparty type to customer type
        customer_type = parse_customer_type(counterparty_type)

        # Check for structuring signals
        has_structuring = len(history_signals) > 0

        # Create transaction object
        transaction = Transaction(
            amount_usd=amount,
            origin_country=source_country,
            destination_country=destination_country,
            purpose=purpose,
            customer_type=customer_type,
            has_structuring_signals=has_structuring,
        )

        # Perform compliance review
        result = engine.review(transaction)

        # Save assessment to database
        assessment_id = db.save_assessment(data, result)
        result['assessment_id'] = assessment_id

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500


@app.route("/api/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200


@app.route("/api/assessments", methods=["GET"])
def get_assessments():
    """
    Get all stored assessments
    
    Query params:
    - limit: Number of records to return (default: 100)
    - offset: Number of records to skip (default: 0)
    """
    try:
        limit = int(request.args.get('limit', 100))
        offset = int(request.args.get('offset', 0))
        
        assessments = db.get_all_assessments(limit=limit, offset=offset)
        return jsonify({
            "assessments": assessments,
            "count": len(assessments)
        }), 200
    except Exception as e:
        return jsonify({"error": f"Failed to retrieve assessments: {str(e)}"}), 500


@app.route("/api/assessments/<int:assessment_id>", methods=["GET"])
def get_assessment(assessment_id):
    """Get a specific assessment by ID"""
    try:
        assessment = db.get_assessment_by_id(assessment_id)
        if not assessment:
            return jsonify({"error": "Assessment not found"}), 404
        return jsonify(assessment), 200
    except Exception as e:
        return jsonify({"error": f"Failed to retrieve assessment: {str(e)}"}), 500


@app.route("/api/statistics", methods=["GET"])
def get_statistics():
    """Get summary statistics of all assessments"""
    try:
        stats = db.get_statistics()
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({"error": f"Failed to retrieve statistics: {str(e)}"}), 500


@app.route("/history", methods=["GET"])
def history():
    """Serve the assessment history page"""
    return send_from_directory("static", "history.html")


@app.route("/configure", methods=["GET"])
def configure():
    """Serve the rules configuration page"""
    return send_from_directory("static", "configure.html")


@app.route("/api/download-mock-documents", methods=["GET"])
def download_mock_documents():
    """
    Download all mock test documents as a ZIP file
    Includes Low, Medium, and High risk scenarios with instructions
    """
    try:
        # Create a temporary ZIP file
        temp_zip = tempfile.NamedTemporaryFile(delete=False, suffix='.zip')
        
        with zipfile.ZipFile(temp_zip.name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            mock_users_dir = Path(__file__).parent / "mock_users"
            
            # Add all PDFs from each risk level
            for risk_folder in ['low_risk', 'medium_risk', 'high_risk']:
                folder_path = mock_users_dir / risk_folder
                if folder_path.exists():
                    for pdf_file in folder_path.glob('*.pdf'):
                        arcname = f"{risk_folder}/{pdf_file.name}"
                        zipf.write(pdf_file, arcname)
            
            # Add instructions
            instructions_file = mock_users_dir / "TEST_INSTRUCTIONS.md"
            if instructions_file.exists():
                zipf.write(instructions_file, "TEST_INSTRUCTIONS.md")
            
            # Add README for judges
            readme_file = mock_users_dir / "README_FOR_JUDGES.md"
            if readme_file.exists():
                zipf.write(readme_file, "README.md")
            
            # Add quick reference
            quick_ref_content = """# 🧪 Mock Documents Test Guide

## 📦 What's Included

- **low_risk/** - 4 PDFs for Low Risk scenario
- **medium_risk/** - 4 PDFs for Medium Risk scenario  
- **high_risk/** - 4 PDFs for High Risk scenario

---

## 🟢 LOW RISK TEST

**Form Inputs:**
- Amount: $3,000
- From: Singapore → To: Philippines
- Purpose: Services
- Type: Freelancer

**Upload:** All 4 PDFs from `low_risk/` folder
**Expected:** Score 0-10 (LOW) ✅

---

## 🟡 MEDIUM RISK TEST

**Form Inputs:**
- Amount: $18,000
- From: Vietnam → To: Indonesia
- Purpose: Trade Finance
- Type: SMB

**Upload:** All 4 PDFs from `medium_risk/` folder
**Expected:** Score 50-60 (MEDIUM) ⚠️

---

## 🔴 HIGH RISK TEST

**Form Inputs:**
- Amount: $35,000
- From: Cayman Islands → To: Vietnam
- Purpose: Investment
- Type: NGO
- History: "multiple small transactions under $10k"

**Upload:** All 4 PDFs from `high_risk/` folder
**Expected:** Score 95-100 (HIGH) 🚨

---

**Start testing at:** http://localhost:8000
"""
            
            zipf.writestr("README.md", quick_ref_content)
        
        # Send the ZIP file
        return send_file(
            temp_zip.name,
            mimetype='application/zip',
            as_attachment=True,
            download_name='mock_compliance_documents.zip'
        )
        
    except Exception as e:
        return jsonify({"error": f"Failed to create download: {str(e)}"}), 500


@app.route("/api/rules", methods=["GET"])
def get_rules():
    """Get current compliance rules configuration"""
    try:
        rules = rules_manager.get_rules()
        return jsonify(rules), 200
    except Exception as e:
        return jsonify({"error": f"Failed to get rules: {str(e)}"}), 500


@app.route("/api/rules", methods=["POST"])
def update_rules():
    """Update compliance rules configuration"""
    try:
        new_rules = request.get_json()
        
        if not new_rules:
            return jsonify({"error": "No rules data provided"}), 400
        
        # Save new rules
        success = rules_manager.save_rules(new_rules)
        
        if success:
            # Reload rules in the compliance engine
            engine.reload_rules()
            return jsonify({
                "message": "Rules updated successfully",
                "rules": rules_manager.get_rules()
            }), 200
        else:
            return jsonify({"error": "Failed to save rules"}), 500
            
    except Exception as e:
        return jsonify({"error": f"Failed to update rules: {str(e)}"}), 500


@app.route("/api/rules/reset", methods=["POST"])
def reset_rules():
    """Reset rules to default configuration"""
    try:
        success = rules_manager.reset_to_defaults()
        
        if success:
            # Reload rules in the compliance engine
            engine.reload_rules()
            return jsonify({
                "message": "Rules reset to defaults",
                "rules": rules_manager.get_rules()
            }), 200
        else:
            return jsonify({"error": "Failed to reset rules"}), 500
            
    except Exception as e:
        return jsonify({"error": f"Failed to reset rules: {str(e)}"}), 500


@app.route("/api/risk-check-with-documents", methods=["POST"])
def risk_check_with_documents():
    """
    Perform compliance risk assessment with supporting documents
    Documents are used as additional context for AI analysis
    """
    try:
        # Get transaction data
        transaction_data_str = request.form.get('transaction_data')
        if not transaction_data_str:
            return jsonify({"error": "No transaction data provided"}), 400
        
        transaction_data = json.loads(transaction_data_str)
        
        # Validate required fields (same as regular endpoint)
        required_fields = [
            "amount",
            "source_country",
            "destination_country",
            "purpose",
            "counterparty_type",
        ]
        for field in required_fields:
            if field not in transaction_data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Parse and validate data
        try:
            amount = float(transaction_data.get("amount", 0))
        except (ValueError, TypeError):
            return jsonify({"error": "Invalid amount"}), 400

        if amount < 0:
            return jsonify({"error": "Amount must be positive"}), 400

        source_country = transaction_data.get("source_country", "").strip()
        destination_country = transaction_data.get("destination_country", "").strip()
        purpose = transaction_data.get("purpose", "").strip()
        counterparty_type = transaction_data.get("counterparty_type", "").strip()
        history_signals = transaction_data.get("history_signals", "").strip()

        # Validation checks
        if not source_country:
            return jsonify({"error": "Source country is required"}), 400
        if not destination_country:
            return jsonify({"error": "Destination country is required"}), 400
        if not purpose:
            return jsonify({"error": "Purpose is required"}), 400
        if not counterparty_type:
            return jsonify({"error": "Counterparty type is required"}), 400

        # Convert counterparty type to customer type
        customer_type = parse_customer_type(counterparty_type)

        # Check for structuring signals
        has_structuring = len(history_signals) > 0

        # Create transaction object
        transaction = Transaction(
            amount_usd=amount,
            origin_country=source_country,
            destination_country=destination_country,
            purpose=purpose,
            customer_type=customer_type,
            has_structuring_signals=has_structuring,
        )

        # Perform standard compliance review
        result = engine.review(transaction)
        
        # If documents are uploaded and OpenAI is available, enhance with document analysis
        if openai_client and request.files:
            document_types = {
                'sourceOfFunds': 'Source of Funds Statement',
                'proofOfIdentity': 'Proof of Identity (KYC)',
                'proofOfResidency': 'Proof of Residency',
                'businessRegistration': 'Business Registration/Articles',
                'contractsInvoices': 'Contracts/Invoices/Payroll'
            }
            
            uploaded_docs = {}
            for doc_key, doc_label in document_types.items():
                if doc_key in request.files:
                    file = request.files[doc_key]
                    if file and file.filename != '':
                        uploaded_docs[doc_key] = {
                            'file': file,
                            'label': doc_label
                        }
            
            if uploaded_docs:
                # Analyze documents as supporting evidence and get score adjustment
                doc_context = analyze_documents_as_evidence(uploaded_docs, transaction, result)
                
                if doc_context:
                    result['document_verification'] = doc_context
                    result['documents_reviewed'] = len(uploaded_docs)
                    
                    # APPLY DOCUMENT SCORE ADJUSTMENT
                    if 'score_adjustment' in doc_context:
                        original_score = result['risk_score']
                        adjustment = doc_context['score_adjustment']
                        
                        # Apply adjustment
                        result['risk_score'] = max(0, min(100, original_score + adjustment))
                        
                        # Recalculate risk level based on new score
                        result['risk_level'] = engine._score_to_level(result['risk_score'])
                        
                        # Add explanation
                        result['score_adjustment_applied'] = {
                            'original_score': original_score,
                            'adjustment': adjustment,
                            'final_score': result['risk_score'],
                            'reason': doc_context.get('adjustment_reason', 'Based on document verification')
                        }
                        
                        # Update rationale
                        if adjustment > 0:
                            result['rationale'] += f" DOCUMENT ALERT: Risk increased by {adjustment} points due to document concerns."
                        elif adjustment < 0:
                            result['rationale'] += f" Documents verified successfully, risk reduced by {abs(adjustment)} points."

        # Save assessment to database
        assessment_id = db.save_assessment(transaction_data, result)
        result['assessment_id'] = assessment_id

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500


def analyze_documents_as_evidence(uploaded_docs, transaction, risk_result):
    """
    Analyze uploaded documents as supporting evidence for the transaction
    Returns verification context AND score adjustment based on document findings
    """
    try:
        document_summaries = []
        score_adjustment = 0
        adjustment_reasons = []
        
        for doc_key, doc_info in uploaded_docs.items():
            file = doc_info['file']
            doc_label = doc_info['label']
            
            # Reset file pointer
            file.seek(0)
            
            # Check file type and convert PDFs
            content_type = file.content_type
            filename = file.filename.lower()
            
            # Skip Word documents
            if content_type in ['application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'] or filename.endswith(('.doc', '.docx')):
                continue
            
            # Read file data
            file_data = file.read()
            
            # Handle PDFs - convert to image
            if content_type == 'application/pdf' or filename.endswith('.pdf'):
                if not PDF_SUPPORT:
                    continue
                
                try:
                    images = convert_from_bytes(file_data, first_page=1, last_page=1)
                    if images:
                        img_byte_arr = io.BytesIO()
                        images[0].save(img_byte_arr, format='PNG')
                        img_byte_arr = img_byte_arr.getvalue()
                        base64_image = base64.b64encode(img_byte_arr).decode('utf-8')
                        image_format = 'png'
                    else:
                        continue
                except Exception:
                    continue
            else:
                base64_image = base64.b64encode(file_data).decode('utf-8')
                image_format = content_type.split('/')[-1]
                if image_format == 'jpeg':
                    image_format = 'jpg'
            
            # Ask AI to verify document and critique its quality/authenticity
            prompt = f"""You are reviewing {doc_label} for AML/KYC compliance.

CLAIMED TRANSACTION DETAILS (from form):
- Amount: ${transaction.amount_usd:,.2f}
- From: {transaction.origin_country} → To: {transaction.destination_country}
- Purpose: {transaction.purpose}
- Customer Type: {transaction.customer_type.value}

CURRENT RISK ASSESSMENT:
- Risk Score: {risk_result['risk_score']}/100
- Risk Level: {risk_result['risk_level']}

Perform TWO types of analysis:

A. DOCUMENT QUALITY CRITIQUE (regardless of form data):
   - Is this a legitimate, authentic-looking document?
   - Is it complete with all necessary information?
   - Is it professionally formatted?
   - Are there signs of tampering, forgery, or manipulation?
   - Is it recent and valid (dates, signatures, etc.)?
   - Does it meet typical standards for this document type?
   - Quality rating: poor/acceptable/good/excellent

B. TRANSACTION VERIFICATION (comparing to form):
   - Do amounts match between document and form?
   - Do countries/parties match?
   - Is the stated purpose verified by this document?
   - Any contradictions or inconsistencies?

C. RED FLAGS & CONCERNS:
   - Suspicious patterns (structuring, round numbers, timing)
   - Missing critical information
   - Questionable legitimacy or authenticity
   - Fraud indicators
   - Compliance concerns

D. SCORE IMPACT:
   - Excellent document + perfect match + no issues: -10 points
   - Good document + matches form: -5 to -7 points
   - Acceptable document, minor issues: 0 to +5 points
   - Poor quality document or mismatches: +10 to +15 points
   - Suspicious/fake document or major contradictions: +20 to +30 points
   - Critical fraud indicators: +35 to +40 points

Return JSON with:
- document_quality: "poor"/"acceptable"/"good"/"excellent"
- authenticity_concerns: true/false
- completeness: "incomplete"/"partial"/"complete"
- quality_notes: critique of document itself
- verified: true/false (matches form data)
- confidence_level: "low"/"medium"/"high"
- notes: detailed explanation of verification
- red_flags: array of specific issues found
- inconsistencies: array of contradictions with form data
- score_adjustment: number (-10 to +40)
- adjustment_reason: explanation including both quality critique and verification result"""

            try:
                response = openai_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an expert AML/KYC compliance analyst. Your document review directly impacts risk scores. Be thorough but fair."
                        },
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/{image_format};base64,{base64_image}"
                                    }
                                }
                            ]
                        }
                    ],
                    max_tokens=700,
                    temperature=0.2,
                    response_format={"type": "json_object"}
                )
                
                doc_analysis = json.loads(response.choices[0].message.content)
                
                # Extract score adjustment
                doc_adjustment = doc_analysis.get('score_adjustment', 0)
                doc_reason = doc_analysis.get('adjustment_reason', '')
                
                # Accumulate adjustments
                score_adjustment += doc_adjustment
                if doc_adjustment != 0:
                    adjustment_reasons.append(f"{doc_label}: {doc_reason} ({doc_adjustment:+d} points)")
                
                document_summaries.append({
                    "document_type": doc_label,
                    "analysis": doc_analysis
                })
                
            except Exception as e:
                print(f"Error analyzing {doc_label}: {e}")
                continue
        
        if document_summaries:
            # Calculate overall verification status
            verified_count = sum(1 for doc in document_summaries if doc['analysis'].get('verified', False))
            total_count = len(document_summaries)
            verification_rate = verified_count / total_count if total_count > 0 else 0
            
            # Determine overall status
            if verification_rate >= 0.8:
                overall_status = "Documents strongly support the transaction"
            elif verification_rate >= 0.5:
                overall_status = "Documents partially support the transaction with some concerns"
            else:
                overall_status = "Documents raise significant concerns about the transaction"
            
            return {
                "documents_analyzed": len(document_summaries),
                "document_reviews": document_summaries,
                "verified_count": verified_count,
                "verification_rate": round(verification_rate * 100, 1),
                "overall_verification": overall_status,
                "score_adjustment": score_adjustment,
                "adjustment_reason": " | ".join(adjustment_reasons) if adjustment_reasons else "No adjustments needed"
            }
        
        return None
        
    except Exception as e:
        print(f"Error in document evidence analysis: {e}")
        return None


@app.route("/api/analyze-documents", methods=["POST"])
def analyze_documents():
    """
    Analyze uploaded KYC/AML documents to extract transaction details
    Handles multiple document types including images, PDFs, and Word documents
    """
    try:
        # Check if OpenAI is available
        if not openai_client:
            return jsonify({
                "error": "Document analysis requires OpenAI API. Please configure OPENAI_API_KEY."
            }), 503
        
        # Collect all uploaded documents
        document_types = {
            'sourceOfFunds': 'Source of Funds Statement',
            'proofOfIdentity': 'Proof of Identity (KYC)',
            'proofOfResidency': 'Proof of Residency',
            'businessRegistration': 'Business Registration/Articles',
            'contractsInvoices': 'Contracts/Invoices/Payroll'
        }
        
        uploaded_docs = {}
        for doc_key, doc_label in document_types.items():
            if doc_key in request.files:
                file = request.files[doc_key]
                if file and file.filename != '':
                    uploaded_docs[doc_key] = {
                        'file': file,
                        'label': doc_label
                    }
        
        if not uploaded_docs:
            return jsonify({"error": "No documents uploaded"}), 400
        
        # Analyze each document with OpenAI
        document_analysis = {}
        extracted_data_combined = {
            "amount": None,
            "currency": "USD",
            "source_country": None,
            "destination_country": None,
            "purpose": None,
            "counterparty_type": None,
            "history_signals": ""
        }
        
        for doc_key, doc_info in uploaded_docs.items():
            file = doc_info['file']
            doc_label = doc_info['label']
            
            # Reset file pointer
            file.seek(0)
            
            # Check file type
            content_type = file.content_type
            filename = file.filename.lower()
            
            # Handle Word documents differently
            if content_type in ['application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'] or filename.endswith(('.doc', '.docx')):
                # For Word documents, inform user to convert or use text extraction
                document_analysis[doc_key] = {
                    "note": "Word document detected. For best results, please convert to PDF or image format.",
                    "filename": file.filename,
                    "status": "skipped"
                }
                continue
            
            # Read file data
            file_data = file.read()
            
            # Handle PDFs - convert to image
            if content_type == 'application/pdf' or filename.endswith('.pdf'):
                if not PDF_SUPPORT:
                    document_analysis[doc_key] = {
                        "error": "PDF support not available. Please install pdf2image.",
                        "filename": file.filename,
                        "status": "error"
                    }
                    continue
                
                try:
                    # Convert PDF first page to image
                    images = convert_from_bytes(file_data, first_page=1, last_page=1)
                    if images:
                        # Convert PIL Image to bytes
                        img_byte_arr = io.BytesIO()
                        images[0].save(img_byte_arr, format='PNG')
                        img_byte_arr = img_byte_arr.getvalue()
                        
                        # Encode as base64
                        base64_image = base64.b64encode(img_byte_arr).decode('utf-8')
                        image_format = 'png'
                    else:
                        document_analysis[doc_key] = {
                            "error": "Could not convert PDF to image",
                            "filename": file.filename,
                            "status": "error"
                        }
                        continue
                except Exception as e:
                    document_analysis[doc_key] = {
                        "error": f"PDF conversion failed: {str(e)}",
                        "filename": file.filename,
                        "status": "error"
                    }
                    continue
            else:
                # Handle images directly
                base64_image = base64.b64encode(file_data).decode('utf-8')
                image_format = content_type.split('/')[-1]
                if image_format == 'jpeg':
                    image_format = 'jpg'
            
            # Create document-specific prompt
            system_prompt = f"""You are an expert KYC/AML compliance analyst analyzing: {doc_label}.

Extract relevant information for transaction compliance:
- Transaction amount and currency
- Countries involved (source and destination)
- Transaction purpose or nature of business
- Entity type (freelancer, SMB, corporate, NGO)
- Any red flags or suspicious patterns
- Identity verification details (if ID document)
- Business legitimacy indicators (if business doc)
- Source of funds verification (if financial statement)

Return a JSON object with all relevant fields you can extract."""
            
            # Call OpenAI Vision API
            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": f"Analyze this {doc_label} document and extract transaction/compliance details. Return as JSON with fields: amount, currency, source_country, destination_country, purpose, counterparty_type, identity_verified, business_legitimate, red_flags, notes. Use null for fields you cannot determine."
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/{image_format};base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=800,
                temperature=0.2
            )
            
            # Parse response
            extracted_text = response.choices[0].message.content
            
            try:
                # Find JSON in response
                if "```json" in extracted_text:
                    extracted_text = extracted_text.split("```json")[1].split("```")[0].strip()
                elif "```" in extracted_text:
                    extracted_text = extracted_text.split("```")[1].split("```")[0].strip()
                
                doc_data = json.loads(extracted_text)
                document_analysis[doc_key] = doc_data
                
                # Merge transaction data (prioritize non-null values)
                if doc_data.get("amount"):
                    extracted_data_combined["amount"] = doc_data["amount"]
                if doc_data.get("currency"):
                    extracted_data_combined["currency"] = doc_data["currency"]
                if doc_data.get("source_country"):
                    extracted_data_combined["source_country"] = doc_data["source_country"]
                if doc_data.get("destination_country"):
                    extracted_data_combined["destination_country"] = doc_data["destination_country"]
                if doc_data.get("purpose"):
                    extracted_data_combined["purpose"] = doc_data["purpose"]
                if doc_data.get("counterparty_type"):
                    extracted_data_combined["counterparty_type"] = doc_data["counterparty_type"]
                if doc_data.get("red_flags"):
                    if extracted_data_combined["history_signals"]:
                        extracted_data_combined["history_signals"] += "; " + doc_data["red_flags"]
                    else:
                        extracted_data_combined["history_signals"] = doc_data["red_flags"]
                
            except json.JSONDecodeError:
                document_analysis[doc_key] = {
                    "error": "Could not parse document data",
                    "raw_response": extracted_text[:200]
                }
        
        # Return extracted data
        return jsonify({
            "extracted_data": extracted_data_combined,
            "document_analysis": document_analysis,
            "documents_analyzed": len(uploaded_docs),
            "message": f"Successfully analyzed {len(uploaded_docs)} document(s)"
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed to analyze documents: {str(e)}"}), 500


if __name__ == "__main__":
    # Run with debug=True for development, use PORT from environment for deployment
    import os
    port = int(os.environ.get('PORT', 8000))
    app.run(debug=False, host="0.0.0.0", port=port)
