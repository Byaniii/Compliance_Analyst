/**
 * AML/KYC Compliance Review System - Frontend JavaScript
 */

// Elements
const transactionForm = document.getElementById("transactionForm");
const loadingSpinner = document.getElementById("loadingSpinner");
const errorMessage = document.getElementById("errorMessage");
const reviewCard = document.getElementById("reviewCard");
const riskScoreCircle = document.getElementById("riskScoreCircle");
const riskScoreValue = document.getElementById("riskScoreValue");
const riskLevelText = document.getElementById("riskLevelText");
const triggeredRulesList = document.getElementById("triggeredRulesList");
const rationaleText = document.getElementById("rationaleText");
const checklistItems = document.getElementById("checklistItems");

/**
 * Format form data to match backend expectations
 */
function getFormData() {
    const formData = new FormData(transactionForm);
    
    // Handle custom purpose
    let purpose = formData.get("purpose") || "";
    if (purpose === "other") {
        const customPurpose = document.getElementById("customPurpose");
        purpose = customPurpose ? customPurpose.value.trim() : "";
    }
    
    const data = {
        amount: parseFloat(formData.get("amount")) || 0,
        currency: formData.get("currency") || "USD",
        source_country: formData.get("source_country") || "",
        destination_country: formData.get("destination_country") || "",
        purpose: purpose,
        counterparty_type: formData.get("counterparty_type") || "",
        history_signals: formData.get("history_signals") || "",
    };
    return data;
}

/**
 * Show loading state
 */
function showLoading() {
    transactionForm.style.display = "none";
    loadingSpinner.style.display = "block";
    reviewCard.style.display = "none";
    errorMessage.style.display = "none";
}

/**
 * Hide loading state
 */
function hideLoading() {
    loadingSpinner.style.display = "none";
}

/**
 * Show error message
 */
function showError(message) {
    errorMessage.textContent = message;
    errorMessage.style.display = "block";
    transactionForm.style.display = "block";
    reviewCard.style.display = "none";
    loadingSpinner.style.display = "none";
    window.scrollTo(0, 0);
}

/**
 * Display compliance review results
 */
function displayResults(result) {
    // Update risk score
    riskScoreValue.textContent = result.risk_score;
    riskLevelText.textContent = result.risk_level;

    // Update circle color based on risk level
    const riskLevel = result.risk_level.toLowerCase();
    riskScoreCircle.className = "risk-score-circle " + riskLevel;

    // Show assessment saved message with link
    if (result.assessment_id) {
        const savedMessage = document.createElement('div');
        savedMessage.style.cssText = 'background: #d4edda; color: #155724; padding: 15px; border-radius: 8px; margin-bottom: 20px; text-align: center;';
        savedMessage.innerHTML = `
            ✓ Assessment saved (ID: #${result.assessment_id}) | 
            <a href="/history" style="color: #155724; font-weight: bold;">View in History →</a>
        `;
        reviewCard.insertBefore(savedMessage, reviewCard.firstChild);
    }

    // Display document verification and score adjustment if applicable
    if (result.score_adjustment_applied) {
        displayScoreAdjustment(result.score_adjustment_applied, result.document_verification);
    } else {
        document.getElementById('scoreAdjustmentSection').style.display = 'none';
    }

    // Display triggered rules
    triggeredRulesList.innerHTML = "";
    if (result.triggered_rules && result.triggered_rules.length > 0) {
        result.triggered_rules.forEach((rule) => {
            const li = document.createElement("li");
            li.textContent = rule;
            triggeredRulesList.appendChild(li);
        });
    } else {
        const li = document.createElement("li");
        li.textContent = "No high-risk rules triggered";
        triggeredRulesList.appendChild(li);
    }

    // Display rationale
    rationaleText.textContent =
        result.rationale || "Assessment completed.";

    // Display checklist
    checklistItems.innerHTML = "";
    if (result.checklist_items && result.checklist_items.length > 0) {
        result.checklist_items.forEach((item) => {
            const li = document.createElement("li");
            li.textContent = item;
            checklistItems.appendChild(li);
        });
    }

    // Show review card
    transactionForm.style.display = "none";
    reviewCard.style.display = "block";
    loadingSpinner.style.display = "none";
    errorMessage.style.display = "none";
    window.scrollTo(0, 0);
}

/**
 * Reset form and show input again
 */
function resetForm() {
    transactionForm.reset();
    transactionForm.style.display = "block";
    reviewCard.style.display = "none";
    errorMessage.style.display = "none";
    loadingSpinner.style.display = "none";
    window.scrollTo(0, 0);
}

/**
 * Submit form and get compliance assessment with documents
 */
async function submitTransaction(event) {
    event.preventDefault();

    const data = getFormData();
    
    // Check if we have uploaded documents
    const hasDocuments = Object.values(uploadedDocuments).some(doc => doc !== null);

    // Validate required fields
    if (!data.amount || data.amount <= 0) {
        showError("❌ Please enter a valid amount greater than 0");
        return;
    }

    if (!data.source_country || !data.source_country.trim()) {
        showError("❌ Please select the source country");
        return;
    }

    if (!data.destination_country || !data.destination_country.trim()) {
        showError("❌ Please select the destination country");
        return;
    }

    if (!data.purpose || !data.purpose.trim()) {
        showError("❌ Please select a transaction purpose or specify a custom purpose");
        return;
    }

    if (!data.counterparty_type) {
        showError("❌ Please select a counterparty type");
        return;
    }

    showLoading();

    try {
        let response;
        
        if (hasDocuments) {
            // Send transaction data + documents
            const formData = new FormData();
            formData.append('transaction_data', JSON.stringify(data));
            
            // Add all uploaded documents
            Object.entries(uploadedDocuments).forEach(([docType, file]) => {
                if (file) {
                    formData.append(docType, file);
                }
            });
            
            response = await fetch("/api/risk-check-with-documents", {
                method: "POST",
                body: formData,
            });
        } else {
            // Send only transaction data (original endpoint)
            response = await fetch("/api/risk-check", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(data),
            });
        }

        hideLoading();

        if (!response.ok) {
            const errorData = await response.json();
            showError(`❌ Error: ${errorData.error || "Request failed"}`);
            return;
        }

        const result = await response.json();
        displayResults(result);
    } catch (error) {
        hideLoading();
        showError(
            `❌ Network error: ${error.message}. Please check your connection and try again.`
        );
    }
}

/**
 * Document Upload Functionality
 */
const uploadedDocuments = {
    sourceOfFunds: null,
    proofOfIdentity: null,
    proofOfResidency: null,
    businessRegistration: null,
    contractsInvoices: null
};

function initDocumentUpload() {

    // Setup each upload field
    const documentTypes = [
        'sourceOfFunds',
        'proofOfIdentity', 
        'proofOfResidency',
        'businessRegistration',
        'contractsInvoices'
    ];

    documentTypes.forEach(docType => {
        const input = document.getElementById(docType);
        const uploadBox = document.querySelector(`[data-input="${docType}"]`);
        const preview = document.getElementById(`preview-${docType}`);
        
        if (!input || !uploadBox) return;

        // Click to upload
        uploadBox.addEventListener("click", () => {
            input.click();
        });

        // File selected
        input.addEventListener("change", (e) => {
            const file = e.target.files[0];
            if (file) {
                handleDocumentSelection(docType, file);
            }
        });
    });

    // Remove buttons
    document.querySelectorAll('.btn-remove').forEach(btn => {
        btn.addEventListener("click", (e) => {
            const docType = e.target.dataset.doc;
            removeDocument(docType);
        });
    });

}

function handleDocumentSelection(docType, file) {
    // Validate file size (10MB max)
    if (file.size > 10 * 1024 * 1024) {
        showError("❌ File size must be less than 10MB");
        return;
    }

    // Store file
    uploadedDocuments[docType] = file;

    // Update UI
    const uploadBox = document.querySelector(`[data-input="${docType}"]`);
    const preview = document.getElementById(`preview-${docType}`);
    const item = uploadBox.closest('.document-upload-item');

    uploadBox.style.display = "none";
    preview.style.display = "flex";
    preview.querySelector('.file-name').textContent = file.name;
    item.classList.add('has-file');

    // Enable analyze button if at least one document uploaded
    updateAnalyzeButton();
}

function removeDocument(docType) {
    uploadedDocuments[docType] = null;
    
    const input = document.getElementById(docType);
    const uploadBox = document.querySelector(`[data-input="${docType}"]`);
    const preview = document.getElementById(`preview-${docType}`);
    const item = uploadBox.closest('.document-upload-item');

    input.value = "";
    uploadBox.style.display = "block";
    preview.style.display = "none";
    item.classList.remove('has-file');

    updateAnalyzeButton();
}

function updateAnalyzeButton() {
    // Update document count display
    const count = Object.values(uploadedDocuments).filter(doc => doc !== null).length;
    const countDisplay = document.getElementById("documentCount");
    if (countDisplay) {
        countDisplay.textContent = count;
    }
}

// Documents are now submitted with the transaction form, not analyzed separately

function displayScoreAdjustment(adjustment, docVerification) {
    const section = document.getElementById('scoreAdjustmentSection');
    const display = document.getElementById('scoreAdjustmentDisplay');
    
    section.style.display = 'block';
    
    const adjustmentValue = adjustment.adjustment;
    const adjustmentClass = adjustmentValue > 0 ? 'increase' : adjustmentValue < 0 ? 'decrease' : 'neutral';
    const adjustmentColor = adjustmentValue > 0 ? '#ef4444' : adjustmentValue < 0 ? '#10b981' : '#6b7280';
    const arrow = adjustmentValue > 0 ? '↑' : adjustmentValue < 0 ? '↓' : '→';
    
    let html = `
        <div style="background: #f9fafb; padding: 20px; border-radius: 8px; margin-bottom: 15px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                <div>
                    <strong>Base Risk Score:</strong> ${adjustment.original_score}
                </div>
                <div style="font-size: 1.5rem; font-weight: bold; color: ${adjustmentColor};">
                    ${arrow} ${adjustmentValue > 0 ? '+' : ''}${adjustmentValue}
                </div>
                <div>
                    <strong>Final Risk Score:</strong> <span style="font-size: 1.2rem; font-weight: bold;">${adjustment.final_score}</span>
                </div>
            </div>
            <p style="margin: 0; color: #666;">
                <strong>Reason:</strong> ${adjustment.reason}
            </p>
        </div>
    `;
    
    if (docVerification && docVerification.document_reviews) {
        html += `
            <div style="margin-top: 15px;">
                <strong>Documents Reviewed: ${docVerification.verified_count}/${docVerification.documents_analyzed} Verified (${docVerification.verification_rate}%)</strong>
                <div style="margin-top: 10px;">
        `;
        
        docVerification.document_reviews.forEach(review => {
            const analysis = review.analysis;
            const verified = analysis.verified;
            const statusIcon = verified ? '✅' : '⚠️';
            const statusColor = verified ? '#10b981' : '#f59e0b';
            const bgColor = verified ? '#ecfdf5' : '#fffbeb';
            
            // Quality indicators
            const qualityColors = {
                'excellent': '#10b981',
                'good': '#059669',
                'acceptable': '#f59e0b',
                'poor': '#ef4444'
            };
            const qualityColor = qualityColors[analysis.document_quality] || '#6b7280';
            
            html += `
                <div style="background: ${bgColor}; border-left: 4px solid ${statusColor}; padding: 15px; margin-bottom: 10px; border-radius: 6px;">
                    <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 10px;">
                        <div style="font-weight: 600;">
                            ${statusIcon} ${review.document_type}
                        </div>
                        ${analysis.score_adjustment ? `
                            <div style="background: ${analysis.score_adjustment > 0 ? '#fee2e2' : '#d1fae5'}; color: ${analysis.score_adjustment > 0 ? '#991b1b' : '#065f46'}; padding: 4px 12px; border-radius: 12px; font-weight: 600; font-size: 0.9rem;">
                                ${analysis.score_adjustment > 0 ? '+' : ''}${analysis.score_adjustment} pts
                            </div>
                        ` : ''}
                    </div>
                    
                    ${analysis.document_quality ? `
                        <div style="margin-bottom: 10px; padding: 8px 12px; background: white; border-radius: 6px; font-size: 0.9rem;">
                            <strong>Document Quality:</strong> 
                            <span style="color: ${qualityColor}; font-weight: 600; text-transform: uppercase;">${analysis.document_quality}</span>
                            ${analysis.completeness ? `| <strong>Completeness:</strong> ${analysis.completeness}` : ''}
                            ${analysis.authenticity_concerns ? `<br><span style="color: #dc2626; font-weight: 600;">⚠️ Authenticity Concerns Detected</span>` : ''}
                        </div>
                    ` : ''}
                    
                    ${analysis.quality_notes ? `
                        <div style="font-size: 0.9rem; color: #374151; margin-bottom: 8px; padding: 10px; background: white; border-radius: 6px;">
                            <strong>Quality Assessment:</strong> ${analysis.quality_notes}
                        </div>
                    ` : ''}
                    
                    <div style="font-size: 0.9rem; color: #666; margin-bottom: 5px;">
                        <strong>Verification:</strong> ${analysis.notes || 'No additional notes'}
                    </div>
                    
                    ${analysis.red_flags && analysis.red_flags.length > 0 ? `
                        <div style="margin-top: 8px;">
                            <strong style="color: #dc2626;">🚩 Red Flags:</strong>
                            <ul style="margin: 5px 0 0 20px; color: #dc2626; font-size: 0.9rem;">
                                ${analysis.red_flags.map(flag => `<li>${flag}</li>`).join('')}
                            </ul>
                        </div>
                    ` : ''}
                    ${analysis.inconsistencies && analysis.inconsistencies.length > 0 ? `
                        <div style="margin-top: 8px;">
                            <strong style="color: #dc2626;">⚠️ Inconsistencies with Form:</strong>
                            <ul style="margin: 5px 0 0 20px; color: #dc2626; font-size: 0.9rem;">
                                ${analysis.inconsistencies.map(item => `<li>${item}</li>`).join('')}
                            </ul>
                        </div>
                    ` : ''}
                </div>
            `;
        });
        
        html += `
                </div>
            </div>
        `;
    }
    
    display.innerHTML = html;
}

function populateFormFromExtraction(data) {
    if (data.amount) document.getElementById("amount").value = data.amount;
    if (data.currency) document.getElementById("currency").value = data.currency;
    if (data.source_country) document.getElementById("sourceCountry").value = data.source_country;
    if (data.destination_country) document.getElementById("destinationCountry").value = data.destination_country;
    if (data.purpose) document.getElementById("purpose").value = data.purpose;
    if (data.counterparty_type) document.getElementById("counterpartyType").value = data.counterparty_type;
    if (data.history_signals) document.getElementById("historySignals").value = data.history_signals;
}

/**
 * Handle custom purpose input visibility
 */
function initPurposeSelector() {
    const purposeSelect = document.getElementById("purpose");
    const customPurposeGroup = document.getElementById("customPurposeGroup");
    const customPurposeInput = document.getElementById("customPurpose");
    
    if (!purposeSelect || !customPurposeGroup) return;
    
    purposeSelect.addEventListener("change", function() {
        if (this.value === "other") {
            customPurposeGroup.style.display = "block";
            customPurposeInput.required = true;
        } else {
            customPurposeGroup.style.display = "none";
            customPurposeInput.required = false;
            customPurposeInput.value = "";
        }
    });
}

/**
 * Initialize event listeners
 */
function init() {
    transactionForm.addEventListener("submit", submitTransaction);
    initDocumentUpload();
    initPurposeSelector();
}

// Initialize when DOM is ready
if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
} else {
    init();
}
