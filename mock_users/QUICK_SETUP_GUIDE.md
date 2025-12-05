# ⚡ Quick Setup - Create Test Documents (15 Minutes)

## 🎯 What You Need

Create 3 sets of documents (Low, Medium, High risk) to test your system.

---

## 📋 Step-by-Step

### 1. Open Google Docs (docs.google.com)

### 2. For Each Document Below:
- Copy the text
- Paste into new Google Doc
- File → Download → PDF
- Save with the specified filename

---

## 🟢 LOW RISK SET

### Create these 4 PDFs in `/mock_users/low_risk/`:

#### File: `low_sof.pdf`
```
DBS BANK SINGAPORE
PERSONAL ACCOUNT STATEMENT

Account: Maria Santos | No: 123-456-789-0
Period: Sep-Nov 2024

Sep 15  Client Payment TechStart      $2,800
Oct 10  Client Payment WebCo          $3,200  
Nov 05  Client Payment DesignHub      $3,000
Nov 28  Client Payment CodeFactory    $2,900

Balance: $18,450
Regular freelance income - Web design services
```

#### File: `low_id.pdf`
```
PHILIPPINES PASSPORT

Passport: P9876543
Name: SANTOS, MARIA ELENA
DOB: 15 May 1995
Nationality: Filipino
Issued: 10 Jan 2022
Expires: 10 Jan 2032
```

#### File: `low_residency.pdf`
```
MERALCO Electric Bill

Maria Santos
456 Makati Ave, Makati 1200
Manila, Philippines

Bill Date: Dec 1, 2024
Period: Nov 1-30, 2024
Consumption: 300 kWh
Total: ₱3,450
```

#### File: `low_invoice.pdf`
```
INVOICE MS-2024-11-028
Date: Nov 28, 2024

FROM: Maria Santos, Freelance Designer
      Manila, Philippines

TO: TechStart Pte Ltd
    Singapore

Services: E-commerce Website Design
120 hours @ $25/hr

TOTAL: $3,000 USD
Payment: USDT via Ripe
```

**FORM INPUTS FOR LOW RISK:**
- Amount: **$3,000**
- From: **Singapore**
- To: **Philippines**
- Purpose: **Services**
- Type: **Freelancer**

---

## 🟡 MEDIUM RISK SET

### Create these 4 PDFs in `/mock_users/medium_risk/`:

#### File: `medium_sof.pdf`
```
VIETCOMBANK BUSINESS ACCOUNT

Company: Saigon Trading Co Ltd
Period: Aug-Nov 2024

Aug 15  Export Payment              $25,000
Sep 10  Supplier Payment Jakarta   -$18,500
Oct 15  Supplier Payment           -$18,000
Nov 05  Customer Payment            $28,000

Balance: $112,300
Import-Export Electronics Business
```

#### File: `medium_business.pdf`
```
VIETNAM BUSINESS REGISTRATION

Company: Saigon Trading Co., Ltd
Registration: 0123456789
Date: March 15, 2021 (3 years old)
Type: LLC

Business: Import-Export Electronics
Address: District 1, HCMC, Vietnam
Director: Nguyen Van Minh
Status: ACTIVE
```

#### File: `medium_id.pdf`
```
VIETNAM CITIZEN ID

ID: 079085001234
Name: NGUYEN VAN MINH
DOB: 20/03/1985
Address: District 1, Ho Chi Minh City
Issued: 05/01/2020
Expires: 05/01/2040
```

#### File: `medium_invoice.pdf`
```
PROFORMA INVOICE ST-2024-11-042
Date: Nov 25, 2024

FROM: Jakarta Electronics Supply
      Jakarta, Indonesia

TO: Saigon Trading Co Ltd
    Ho Chi Minh City, Vietnam

ITEMS:
LED Display Modules  500 units  $28  $14,000
Circuit Boards       200 units  $20  $4,000

TOTAL: $18,000 USD
Terms: FOB Jakarta
Purpose: Import Electronic Components
```

**FORM INPUTS FOR MEDIUM RISK:**
- Amount: **$18,000**
- From: **Vietnam**
- To: **Indonesia**
- Purpose: **Trade Finance**
- Type: **SMB**

---

## 🔴 HIGH RISK SET

### Create these 4 PDFs in `/mock_users/high_risk/`:

#### File: `high_sof.pdf`
```
FINANCIAL STATEMENT
Global Ventures Ltd - Cayman Islands

Nov 01  Wire Transfer Unknown      $9,900
Nov 03  Wire Transfer Unknown      $9,800
Nov 05  Cash Equivalent            $9,700
Nov 08  Wire Transfer Unknown      $9,900
Nov 12  Transfer Various           $9,850

(STRUCTURING PATTERN - All under $10k!)

Total: $58,900
Purpose: Investment Activities
```

#### File: `high_business.pdf`
```
CAYMAN ISLANDS INCORPORATION

Company: Global Ventures Ltd
Number: 123456
Incorporated: May 15, 2024 (ONLY 6 MONTHS!)

Registered: PO Box 1234, Grand Cayman
Directors: Nominee Director Services Ltd
Shareholders: Bearer Shares (ANONYMOUS!)
Activity: Investment Holdings (VAGUE!)
```

#### File: `high_id.pdf`
```
NIGERIA PASSPORT

Passport: A1234567
Name: OKONKWO, JOHN EMMANUEL
Nationality: Nigerian
DOB: 10/08/1980
Issued: 15 Sep 2024 (VERY RECENT!)
Expires: 15 Sep 2034

Director of Global Ventures Ltd
```

#### File: `high_investment.pdf`
```
INVESTMENT AGREEMENT
Date: Nov 28, 2024

INVESTOR: Global Ventures Ltd (Cayman Islands)
DIRECTOR: John Okonkwo

TARGET: Vietnam Property Holdings

Amount: $35,000
Purpose: Real estate investment (VAGUE!)
Terms: To be determined (NO SPECIFICS!)
Returns: Subject to performance
Exit: At discretion

Preliminary agreement - terms pending
```

**FORM INPUTS FOR HIGH RISK:**
- Amount: **$35,000**
- From: **Cayman Islands**
- To: **Vietnam**
- Purpose: **Investment**
- Type: **NGO**
- History: **"multiple small transactions under $10k in past 2 weeks"**

---

## ⚡ 15-Minute Process

1. **Copy each text block above**
2. **Paste into Google Docs** (12 separate docs)
3. **Format minimally** (bold the titles)
4. **Download each as PDF**
5. **Rename** to match filenames above
6. **Done!**

---

## 🎯 Expected Results

**LOW:** Base 13 + Docs -12 = **Score: 1 (Low)** ✅
**MEDIUM:** Base 63 + Docs -10 = **Score: 53 (Medium)** ⚠️
**HIGH:** Base 98 + Docs +30 = **Score: 100 (High)** 🚨

**Your scenarios will now work perfectly!** 🚀

