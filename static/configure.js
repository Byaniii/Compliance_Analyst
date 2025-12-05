/**
 * Risk Rules Configuration UI JavaScript
 */

let currentRules = {};

// Master list of all available countries
const ALL_COUNTRIES = [
    // Southeast Asia
    "Singapore", "Philippines", "Vietnam", "Indonesia", "Thailand", "Malaysia", "Myanmar", "Cambodia",
    // Asia Pacific
    "Hong Kong", "China", "Japan", "South Korea", "Taiwan", "India", "Pakistan", "Bangladesh", "Australia", "New Zealand",
    // North America
    "United States", "Canada", "Mexico",
    // Europe
    "United Kingdom", "Germany", "France", "Switzerland", "Netherlands", "Italy", "Spain", "Poland", "Russia",
    // Middle East
    "United Arab Emirates", "Saudi Arabia", "Qatar", "Israel", "Turkey", "Iran",
    // Africa
    "South Africa", "Nigeria", "Kenya", "Egypt",
    // Latin America
    "Brazil", "Argentina", "Colombia", "Chile",
    // Offshore/High Risk
    "Cayman Islands", "British Virgin Islands", "Panama", "Bahamas", "Seychelles", "North Korea", "Syria"
];

// Load rules on page load
window.addEventListener('DOMContentLoaded', loadRules);

async function loadRules() {
    showLoading();
    try {
        const response = await fetch('/api/rules');
        if (!response.ok) {
            throw new Error('Failed to load rules');
        }
        
        currentRules = await response.json();
        populateUI(currentRules);
        hideLoading();
    } catch (error) {
        showError('Failed to load configuration: ' + error.message);
        hideLoading();
    }
}

function populateUI(rules) {
    // Populate country dropdowns
    populateCountryDropdowns();
    
    // Populate countries
    renderList('low-countries', rules.low_risk_countries, 'low', 'country');
    renderList('medium-countries', rules.medium_risk_countries, 'medium', 'country');
    renderList('high-countries', rules.high_risk_countries, 'high', 'country');
    
    // Populate purposes
    renderList('low-purposes', rules.low_risk_purposes, 'low', 'purpose');
    renderList('medium-purposes', rules.medium_risk_purposes, 'medium', 'purpose');
    renderList('high-purposes', rules.high_risk_purposes, 'high', 'purpose');
    
    // Populate scores
    document.getElementById('low-country-score').value = rules.country_risk_scores.low;
    document.getElementById('medium-country-score').value = rules.country_risk_scores.medium;
    document.getElementById('high-country-score').value = rules.country_risk_scores.high;
    
    document.getElementById('low-purpose-score').value = rules.purpose_risk_scores.low;
    document.getElementById('medium-purpose-score').value = rules.purpose_risk_scores.medium;
    document.getElementById('high-purpose-score').value = rules.purpose_risk_scores.high;
    
    document.getElementById('low-customer-score').value = rules.customer_type_scores.low;
    document.getElementById('medium-customer-score').value = rules.customer_type_scores.medium;
    document.getElementById('high-customer-score').value = rules.customer_type_scores.high;
    
    // Populate thresholds
    document.getElementById('high-risk-origin-threshold').value = rules.amount_thresholds.high_risk_origin_threshold;
    document.getElementById('general-high-threshold').value = rules.amount_thresholds.general_high_threshold;
    document.getElementById('moderate-threshold').value = rules.amount_thresholds.moderate_threshold;
    
    document.getElementById('low-max-score').value = rules.risk_score_thresholds.low_max;
    document.getElementById('medium-max-score').value = rules.risk_score_thresholds.medium_max;
    
    document.getElementById('config-content').style.display = 'block';
}

function populateCountryDropdowns() {
    const levels = ['low', 'medium', 'high'];
    
    levels.forEach(level => {
        const select = document.getElementById(`add-${level}-country`);
        if (!select) return;
        
        // Clear existing options except first
        select.innerHTML = '<option value="">-- Select country to add --</option>';
        
        // Add all countries sorted alphabetically
        const sortedCountries = [...ALL_COUNTRIES].sort();
        sortedCountries.forEach(country => {
            const option = document.createElement('option');
            option.value = country;
            option.textContent = country;
            select.appendChild(option);
        });
        
        // Add "Other" option for custom entry
        const otherOption = document.createElement('option');
        otherOption.value = '__custom__';
        otherOption.textContent = '✏️ Other (Type custom country)';
        select.appendChild(otherOption);
    });
}

function renderList(containerId, items, level, type) {
    const container = document.getElementById(containerId);
    container.innerHTML = '';
    
    items.forEach(item => {
        const tag = document.createElement('div');
        tag.className = 'tag';
        tag.innerHTML = `
            <span>${item}</span>
            <span class="tag-remove" onclick="removeItem('${level}', '${type}', '${item}')">×</span>
        `;
        container.appendChild(tag);
    });
}

function addItem(level, type) {
    const input = document.getElementById(`add-${level}-${type}`);
    let value = input.value.trim();
    
    if (!value) {
        alert('Please select or enter a value');
        return;
    }
    
    // Handle custom country entry
    if (value === '__custom__' && type === 'country') {
        const customCountry = prompt('Enter custom country name:');
        if (!customCountry || !customCountry.trim()) {
            return;
        }
        value = customCountry.trim();
    }
    
    const typeKey = type === 'country' ? 'countries' : 'purposes';
    const currentKey = `${level}_risk_${typeKey}`;
    
    // Check if already exists in this level
    if (currentRules[currentKey].includes(value)) {
        alert(`"${value}" is already in the ${level} risk list`);
        return;
    }
    
    // Check if exists in other risk levels
    const otherLevels = ['low', 'medium', 'high'].filter(l => l !== level);
    let existsInLevel = null;
    
    for (const otherLevel of otherLevels) {
        const otherKey = `${otherLevel}_risk_${typeKey}`;
        if (currentRules[otherKey].includes(value)) {
            existsInLevel = otherLevel;
            break;
        }
    }
    
    if (existsInLevel) {
        const shouldMove = confirm(
            `"${value}" is currently in the ${existsInLevel} risk list.\n\n` +
            `Do you want to MOVE it to ${level} risk?\n\n` +
            `Click OK to move, Cancel to keep it where it is.`
        );
        
        if (shouldMove) {
            // Remove from old level
            const oldKey = `${existsInLevel}_risk_${typeKey}`;
            currentRules[oldKey] = currentRules[oldKey].filter(item => item !== value);
            renderList(`${existsInLevel}-${typeKey}`, currentRules[oldKey], existsInLevel, type);
            
            // Add to new level
            currentRules[currentKey].push(value);
            renderList(`${level}-${typeKey}`, currentRules[currentKey], level, type);
            input.value = '';
            
            // Show success feedback
            showItemSuccess(event.target, `Moved from ${existsInLevel} to ${level}`);
        }
    } else {
        // Add to current level
        currentRules[currentKey].push(value);
        renderList(`${level}-${typeKey}`, currentRules[currentKey], level, type);
        input.value = '';
        
        // Show success feedback
        showItemSuccess(event.target, 'Added');
    }
}

function showItemSuccess(btn, message) {
    const originalText = btn.textContent;
    btn.textContent = `✓ ${message}`;
    btn.style.background = '#10b981';
    setTimeout(() => {
        btn.textContent = originalText;
        btn.style.background = '';
    }, 2000);
}

function removeItem(level, type, item) {
    const key = `${level}_risk_${type === 'country' ? 'countries' : 'purposes'}`;
    
    currentRules[key] = currentRules[key].filter(i => i !== item);
    renderList(`${level}-${type === 'country' ? 'countries' : 'purposes'}`, currentRules[key], level, type);
}

async function saveRules() {
    // Validate no duplicates across risk levels
    const validation = validateNoDuplicates();
    if (!validation.valid) {
        alert(`❌ Cannot save: ${validation.error}\n\nPlease fix the conflicts before saving.`);
        return;
    }
    
    showLoading();
    
    try {
        // Collect all values from UI
        const rules = {
            high_risk_countries: currentRules.high_risk_countries,
            medium_risk_countries: currentRules.medium_risk_countries,
            low_risk_countries: currentRules.low_risk_countries,
            high_risk_purposes: currentRules.high_risk_purposes,
            medium_risk_purposes: currentRules.medium_risk_purposes,
            low_risk_purposes: currentRules.low_risk_purposes,
            country_risk_scores: {
                high: parseInt(document.getElementById('high-country-score').value),
                medium: parseInt(document.getElementById('medium-country-score').value),
                low: parseInt(document.getElementById('low-country-score').value)
            },
            purpose_risk_scores: {
                high: parseInt(document.getElementById('high-purpose-score').value),
                medium: parseInt(document.getElementById('medium-purpose-score').value),
                low: parseInt(document.getElementById('low-purpose-score').value)
            },
            customer_type_scores: {
                high: parseInt(document.getElementById('high-customer-score').value),
                medium: parseInt(document.getElementById('medium-customer-score').value),
                low: parseInt(document.getElementById('low-customer-score').value)
            },
            amount_thresholds: {
                high_risk_origin_threshold: parseInt(document.getElementById('high-risk-origin-threshold').value),
                general_high_threshold: parseInt(document.getElementById('general-high-threshold').value),
                moderate_threshold: parseInt(document.getElementById('moderate-threshold').value)
            },
            risk_score_thresholds: {
                low_max: parseInt(document.getElementById('low-max-score').value),
                medium_max: parseInt(document.getElementById('medium-max-score').value)
            }
        };
        
        const response = await fetch('/api/rules', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(rules)
        });
        
        if (!response.ok) {
            throw new Error('Failed to save rules');
        }
        
        const result = await response.json();
        currentRules = result.rules;
        
        hideLoading();
        showSuccess('✓ Configuration saved successfully! Rules are now active.');
    } catch (error) {
        hideLoading();
        showError('Failed to save configuration: ' + error.message);
    }
}

async function resetToDefaults() {
    if (!confirm('Are you sure you want to reset all rules to default values? This cannot be undone.')) {
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch('/api/rules/reset', {
            method: 'POST'
        });
        
        if (!response.ok) {
            throw new Error('Failed to reset rules');
        }
        
        const result = await response.json();
        currentRules = result.rules;
        populateUI(currentRules);
        
        hideLoading();
        showSuccess('✓ Rules reset to default configuration');
    } catch (error) {
        hideLoading();
        showError('Failed to reset configuration: ' + error.message);
    }
}

function showLoading() {
    document.getElementById('loading').style.display = 'block';
    document.getElementById('config-content').style.display = 'none';
    document.getElementById('message').innerHTML = '';
}

function hideLoading() {
    document.getElementById('loading').style.display = 'none';
}

function showSuccess(message) {
    const messageDiv = document.getElementById('message');
    messageDiv.innerHTML = `<div class="success-message">${message}</div>`;
    setTimeout(() => {
        messageDiv.innerHTML = '';
    }, 5000);
}

function showError(message) {
    const messageDiv = document.getElementById('message');
    messageDiv.innerHTML = `<div class="error-message">❌ ${message}</div>`;
}

function validateNoDuplicates() {
    const errors = [];
    
    // Check countries
    const allCountries = [
        ...currentRules.low_risk_countries,
        ...currentRules.medium_risk_countries,
        ...currentRules.high_risk_countries
    ];
    
    const countryDuplicates = allCountries.filter((item, index) => allCountries.indexOf(item) !== index);
    if (countryDuplicates.length > 0) {
        const unique = [...new Set(countryDuplicates)];
        errors.push(`Countries in multiple risk levels: ${unique.join(', ')}`);
    }
    
    // Check purposes
    const allPurposes = [
        ...currentRules.low_risk_purposes,
        ...currentRules.medium_risk_purposes,
        ...currentRules.high_risk_purposes
    ];
    
    const purposeDuplicates = allPurposes.filter((item, index) => allPurposes.indexOf(item) !== index);
    if (purposeDuplicates.length > 0) {
        const unique = [...new Set(purposeDuplicates)];
        errors.push(`Purposes in multiple risk levels: ${unique.join(', ')}`);
    }
    
    if (errors.length > 0) {
        return {
            valid: false,
            error: errors.join('\n')
        };
    }
    
    return { valid: true };
}

