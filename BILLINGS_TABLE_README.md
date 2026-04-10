# BILLINGS TABLE DOCUMENTATION

## Table Overview
**Table Name:** `ds_p.default.billings`  
**Source:** billings.xlsx  
**Total Records:** 115,661  
**Unique Customers:** 46,819  
**Columns:** 62

## Purpose
This table contains comprehensive billing and customer information for membership renewals. It serves as the primary dataset for understanding customer demographics, payment history, renewal patterns, and various scoring metrics that are critical for building a post-renewal churn prediction model.

## Data Timeline
* **Registration Dates:** 2000-01-01 to 2026-03-24
* **Renewal Dates:** 2023-01-01 to 2050-10-13
* **Payment Dates:** 2021-06-21 to 2026-01-11

---

## Column Documentation

### 1. Customer Identification
#### Co_Ref (string)
* **Description:** Customer Reference ID - Unique identifier for each customer/contractor
* **Type:** Categorical (Identifier)
* **Purpose:** Primary key for joining with other tables (emails, cc_calls, renewal_calls)
* **Churn Relevance:** ⭐⭐⭐⭐⭐ Essential for tracking customer churn across datasets

---

### 2. Connection Metrics
#### Connection_Net (double)
* **Description:** Net connection amount
* **Type:** Numeric (Currency)
* **Purpose:** Tracks network-related charges
* **Churn Relevance:** ⭐⭐ May indicate service usage patterns

#### Connection_Qty (double)
* **Description:** Quantity of connections
* **Type:** Numeric (Count)
* **Purpose:** Number of connections associated with the membership
* **Churn Relevance:** ⭐⭐ Higher connections may indicate stronger engagement

#### Starting_Connection_Net (double)
* **Description:** Initial connection net amount
* **Type:** Numeric (Currency)
* **Purpose:** Starting value for connections
* **Churn Relevance:** ⭐⭐ Baseline for measuring growth

#### Starting_Connection_Qty (double)
* **Description:** Initial quantity of connections
* **Type:** Numeric (Count)
* **Purpose:** Starting number of connections
* **Churn Relevance:** ⭐⭐ Track expansion or contraction

#### Connection_Group (string)
* **Description:** Categorizes customers by number of connections
* **Type:** Categorical
* **Categories:** 
  * "1" (36,142 customers) - Single connection
  * "Independent" (23,679) - Independent contractors
  * "4 to 9" (19,552) - Mid-size operations
  * "2" (18,382) - Two connections
  * "3" (9,924) - Three connections
  * "10+" (7,831) - Large operations
* **Purpose:** Segment customers by business size
* **Churn Relevance:** ⭐⭐⭐⭐ Larger operations may have different churn patterns

#### #_of_Connection (double)
* **Description:** Total number of connections
* **Type:** Numeric (Count)
* **Purpose:** Quantifies customer scale
* **Churn Relevance:** ⭐⭐⭐ Scale correlates with retention

#### Last_Connections (double)
* **Description:** Previous year's connection count
* **Type:** Numeric (Count)
* **Purpose:** Historical comparison
* **Churn Relevance:** ⭐⭐⭐ Declining connections signal churn risk

---

### 3. Pricing & Discount Metrics
#### Discount_Amount (double)
* **Description:** Discount applied to the customer's subscription
* **Type:** Numeric (Currency)
* **Purpose:** Tracks promotional discounts and special offers
* **Churn Relevance:** ⭐⭐⭐⭐ Customers with discounts may be price-sensitive

#### Last_Years_Price (double)
* **Description:** Previous year's subscription price
* **Type:** Numeric (Currency)
* **Purpose:** Baseline for price comparison and price increase calculation
* **Churn Relevance:** ⭐⭐⭐⭐⭐ Price increases are a major churn driver

#### Gross (double)
* **Description:** Gross billing amount
* **Type:** Numeric (Currency)
* **Purpose:** Total revenue before adjustments
* **Churn Relevance:** ⭐⭐⭐ Higher-value customers may have different retention

#### Total_Net_Paid (double)
* **Description:** Total net amount paid by customer
* **Type:** Numeric (Currency)
* **Purpose:** Actual revenue received
* **Churn Relevance:** ⭐⭐⭐⭐ Payment behavior predicts future commitment

#### Amount (long)
* **Description:** Base amount
* **Type:** Numeric (Currency)
* **Purpose:** Core billing amount
* **Churn Relevance:** ⭐⭐⭐ Price sensitivity indicator

#### Total_Amount (double)
* **Description:** Total billing amount
* **Type:** Numeric (Currency)
* **Purpose:** Complete transaction value
* **Churn Relevance:** ⭐⭐⭐ Overall financial commitment

---

### 4. Membership Package Components
#### Starting_Net (long)
* **Description:** Initial net amount
* **Type:** Numeric (Currency)
* **Churn Relevance:** ⭐⭐ Baseline pricing

#### Starting_Vat (double)
* **Description:** Initial VAT amount
* **Type:** Numeric (Currency)
* **Churn Relevance:** ⭐ Tax component

#### Starting_Gross (double)
* **Description:** Initial gross amount
* **Type:** Numeric (Currency)
* **Churn Relevance:** ⭐⭐ Starting price point

#### Starting_Membership_Net (long)
* **Description:** Initial membership fee (net)
* **Type:** Numeric (Currency)
* **Churn Relevance:** ⭐⭐⭐ Core membership cost

#### Starting_Package_Net (long)
* **Description:** Initial package fee (net)
* **Type:** Numeric (Currency)
* **Churn Relevance:** ⭐⭐ Additional package cost

#### Starting_PQQ_Net (long)
* **Description:** Initial PQQ (Pre-Qualification Questionnaire) fee
* **Type:** Numeric (Currency)
* **Churn Relevance:** ⭐⭐ Accreditation-related cost

#### Membership_Net (double)
* **Description:** Current membership fee (net)
* **Type:** Numeric (Currency)
* **Churn Relevance:** ⭐⭐⭐⭐ Core recurring revenue

#### Package_Net (double)
* **Description:** Current package fee (net)
* **Type:** Numeric (Currency)
* **Churn Relevance:** ⭐⭐⭐ Add-on service revenue

#### PQQNet (long)
* **Description:** Current PQQ fee
* **Type:** Numeric (Currency)
* **Churn Relevance:** ⭐⭐ Compliance cost

#### Other_Net (long)
* **Description:** Other miscellaneous fees
* **Type:** Numeric (Currency)
* **Churn Relevance:** ⭐⭐ Additional charges

---

### 5. Scoring Metrics (Churn Prediction Features)
#### Last_Payment_Score (long)
* **Description:** Score based on payment history
* **Type:** Numeric (Score 0-10)
* **Purpose:** Quantifies payment reliability
* **Churn Relevance:** ⭐⭐⭐⭐⭐ Strong predictor - consistent payers less likely to churn

#### Last_Discount_Score (long)
* **Description:** Score based on discount history
* **Type:** Numeric (Score 0-10)
* **Purpose:** Measures discount dependency
* **Churn Relevance:** ⭐⭐⭐⭐ High scores may indicate price sensitivity

#### Sustainability_Score (double)
* **Description:** Sustainability/longevity score
* **Type:** Numeric (Score)
* **Purpose:** Predicts long-term customer viability
* **Churn Relevance:** ⭐⭐⭐⭐⭐ Core churn prediction metric

#### Total_Renewal_Score_New (double)
* **Description:** Comprehensive renewal likelihood score
* **Type:** Numeric (Score)
* **Purpose:** Aggregate score combining multiple factors
* **Churn Relevance:** ⭐⭐⭐⭐⭐ Primary churn prediction score

#### Auto_Renewal_Score (long)
* **Description:** Score for auto-renewal likelihood
* **Type:** Numeric (Score 0-10)
* **Purpose:** Measures automated renewal probability
* **Churn Relevance:** ⭐⭐⭐⭐⭐ Auto-renewal customers have lower churn

#### Status_Scores (long)
* **Description:** Account status-based score
* **Type:** Numeric (Score 0-10)
* **Purpose:** Reflects account health status
* **Churn Relevance:** ⭐⭐⭐⭐⭐ Poor status = high churn risk

#### Anchoring_Score (double)
* **Description:** Score for client anchoring/requirements
* **Type:** Numeric (Score)
* **Purpose:** Measures if customer is "anchored" by client requirements
* **Churn Relevance:** ⭐⭐⭐⭐⭐ Anchored customers less likely to churn

#### Tenure_Scores (double)
* **Description:** Score based on customer tenure
* **Type:** Numeric (Score)
* **Purpose:** Rewards long-term customers
* **Churn Relevance:** ⭐⭐⭐⭐⭐ Longer tenure = lower churn

#### Renewal_Score_At_Release (double)
* **Description:** Renewal score at time of release
* **Type:** Numeric (Score)
* **Purpose:** Snapshot score
* **Churn Relevance:** ⭐⭐⭐⭐ Historical benchmark

---

### 6. Auto-Renewal & Payment Automation
#### Proforma_Auto_Renewal (double)
* **Description:** Proforma auto-renewal indicator
* **Type:** Binary (0/1)
* **Purpose:** Flags auto-renewal setup in proforma
* **Churn Relevance:** ⭐⭐⭐⭐⭐ Auto-renewal drastically reduces churn

#### Current_Auto_Renewal_Flag (string)
* **Description:** Current auto-renewal status
* **Type:** Categorical (Binary)
* **Categories:** 
  * "y" (109,647) - Auto-renewal enabled
  * "n" (6,014) - No auto-renewal
* **Purpose:** Identifies automatic renewal customers
* **Churn Relevance:** ⭐⭐⭐⭐⭐ Critical churn predictor

#### Proforma_World_Pay_Token (double)
* **Description:** Proforma payment token indicator
* **Type:** Binary (0/1)
* **Purpose:** Flags saved payment method in proforma
* **Churn Relevance:** ⭐⭐⭐⭐ Saved payment = easier renewal

#### Current_World_Pay_Token (string)
* **Description:** Current saved payment token status
* **Type:** Categorical (Binary)
* **Categories:** 
  * "n" (60,727) - No saved payment
  * "y" (54,934) - Payment method saved
* **Purpose:** Tracks payment convenience
* **Churn Relevance:** ⭐⭐⭐⭐ Reduces friction in renewal

---

### 7. Account Status & Stage
#### Proforma_Account_Stage (string)
* **Description:** Current account stage in the membership lifecycle
* **Type:** Categorical
* **Categories:** 
  * "Published" (73,364) - Active, accredited accounts
  * "Membership Only" (16,586) - Basic membership without accreditation
  * "Renewal Process" (13,068) - In renewal workflow
  * "Vetting" (2,501) - Undergoing vetting process
  * "Suspended" (891) - Account suspended
  * "Retired" (1) - Closed account
  * "vetting" (1) - Lowercase variant
* **Purpose:** Categorizes customer lifecycle stage
* **Churn Relevance:** ⭐⭐⭐⭐⭐ "Suspended" and "Renewal Process" are high churn risk

#### Proforma_Audit_Status (string)
* **Description:** Accreditation and audit status
* **Type:** Categorical
* **Top Categories:** 
  * "Accredited" (72,317) - Fully accredited
  * "Failed- Renewal Questionnaire not received" (6,284) - **HIGH CHURN RISK**
  * "Renewal Questionnaire Received" (6,064) - In progress
  * "Failed- Renewal Additional Information Not Received" (3,610) - **HIGH CHURN RISK**
  * "Failed- Initial additional info not received" (3,477) - **HIGH CHURN RISK**
  * "Failed- Initial Questionnaire not received" (3,199) - **HIGH CHURN RISK**
  * "Renewal Questionnaire Sent" (3,186)
  * Plus 13 more statuses
* **Purpose:** Tracks accreditation completion
* **Churn Relevance:** ⭐⭐⭐⭐⭐ "Failed" statuses strongly predict churn

#### Proforma_Membership_Status (string)
* **Description:** Overall membership status
* **Type:** Categorical
* **Purpose:** High-level status categorization
* **Churn Relevance:** ⭐⭐⭐⭐ Status health indicator

---

### 8. Pricing Bands & Segments
#### Band (string)
* **Description:** Pricing/membership tier band
* **Type:** Categorical
* **Categories:** 
  * "Band B" (31,043) - Most common
  * "Band C1" (23,620)
  * "Band D" (17,904)
  * "Band C2" (14,949)
  * "Band E" (9,111)
  * "Band F1" (5,517)
  * "Band A" (3,597)
  * "Band F2" (2,967)
  * "Band G" (2,273)
  * "Band F" (2,193)
  * "Group" (941)
  * "Band H" (777)
  * "Band J" (369)
  * "Band I" (365)
* **Purpose:** Price segmentation
* **Churn Relevance:** ⭐⭐⭐⭐ Different bands may have different churn patterns

#### Last_Band (string)
* **Description:** Previous pricing band
* **Type:** Categorical
* **Purpose:** Track band changes (upgrades/downgrades)
* **Churn Relevance:** ⭐⭐⭐ Band changes may signal satisfaction shifts

---

### 9. Date Fields
#### Registration_Date (timestamp)
* **Description:** Date when customer first registered
* **Type:** Date
* **Range:** 2000-01-01 to 2026-03-24
* **Purpose:** Calculate customer tenure
* **Churn Relevance:** ⭐⭐⭐⭐ Tenure is inversely related to churn

#### Proforma_Date (timestamp)
* **Description:** Proforma invoice date
* **Type:** Date
* **Purpose:** Invoice generation timing
* **Churn Relevance:** ⭐⭐ Process timing

#### Date_Paid (timestamp)
* **Description:** Date when payment was received
* **Type:** Date
* **Range:** 2021-06-21 to 2026-01-11
* **Purpose:** Payment timing analysis
* **Churn Relevance:** ⭐⭐⭐⭐ Late payments indicate churn risk

#### Prospect_Renewal_Date (timestamp)
* **Description:** **CRITICAL FOR POST-RENEWAL CHURN** - Expected renewal date
* **Type:** Date
* **Range:** 2023-01-01 to 2050-10-13
* **Purpose:** Defines the renewal deadline; features from renewal_calls after this date are "post-renewal"
* **Churn Relevance:** ⭐⭐⭐⭐⭐ **Essential for defining post-renewal churn period**

#### Closed_Date (timestamp)
* **Description:** Date when account/transaction was closed
* **Type:** Date
* **Purpose:** Track completion timing
* **Churn Relevance:** ⭐⭐⭐ Closed accounts

#### Renewal_Month (timestamp)
* **Description:** Month of renewal
* **Type:** Date (Month)
* **Purpose:** Seasonal pattern analysis
* **Churn Relevance:** ⭐⭐⭐ Seasonality affects renewal

#### Last_Renewal (timestamp)
* **Description:** Date of last renewal
* **Type:** Date
* **Purpose:** Renewal recency
* **Churn Relevance:** ⭐⭐⭐⭐ Recency matters for retention

#### Review_Date_At_Time_Of_Release (timestamp)
* **Description:** Review date snapshot
* **Type:** Date
* **Purpose:** Audit timing
* **Churn Relevance:** ⭐⭐ Process milestone

#### DateTime_Out (timestamp)
* **Description:** Output/extraction timestamp
* **Type:** Date
* **Purpose:** Data snapshot time
* **Churn Relevance:** ⭐ Metadata

---

### 10. Tenure Metrics
#### Payment_Timeframe (double)
* **Description:** Time period for payment
* **Type:** Numeric (Days/Period)
* **Purpose:** Payment cycle length
* **Churn Relevance:** ⭐⭐⭐ Delayed payments = churn risk

#### Tenure_Years (double)
* **Description:** Number of years as a customer
* **Type:** Numeric (Years)
* **Purpose:** Measures customer loyalty/longevity
* **Churn Relevance:** ⭐⭐⭐⭐⭐ Longer tenure = lower churn

#### Tenure_Group (string)
* **Description:** Categorical tenure segment
* **Type:** Categorical
* **Purpose:** Group customers by tenure brackets
* **Churn Relevance:** ⭐⭐⭐⭐ Segmented tenure analysis

---

### 11. Anchoring Metrics
#### Current_Anchorings (long)
* **Description:** Number of current client anchorings
* **Type:** Numeric (Count)
* **Purpose:** Counts how many clients require this accreditation
* **Churn Relevance:** ⭐⭐⭐⭐⭐ More anchorings = mandatory renewal = low churn

#### Proforma_Approved_Lists (double)
* **Description:** Number of approved lists
* **Type:** Numeric (Count)
* **Purpose:** Tracks client approvals
* **Churn Relevance:** ⭐⭐⭐⭐ More approvals = more value

#### Anchor_Group (string)
* **Description:** Anchoring category/group
* **Type:** Categorical
* **Purpose:** Segment by anchoring type
* **Churn Relevance:** ⭐⭐⭐⭐ Anchored customers are locked in

---

### 12. Outcome Metrics
#### Prospect_Outcome (string)
* **Description:** Final outcome of the renewal prospect
* **Type:** Categorical
* **Likely Categories:** "Won", "Lost", "Pending"
* **Purpose:** **TARGET VARIABLE FOR CHURN MODEL**
* **Churn Relevance:** ⭐⭐⭐⭐⭐ **This is the churn label**

#### Last_Years_Date_Paid (double)
* **Description:** Last year's payment date (numeric format)
* **Type:** Numeric (Timestamp)
* **Purpose:** Historical payment reference
* **Churn Relevance:** ⭐⭐⭐ Payment consistency

#### Last_Total_Net_Paid (double)
* **Description:** Last year's total net paid
* **Type:** Numeric (Currency)
* **Purpose:** Historical spending comparison
* **Churn Relevance:** ⭐⭐⭐ Spending trend analysis

---

### 13. Metadata Fields
#### Billings_Contractor (long)
* **Description:** Contractor flag or count
* **Type:** Numeric (Binary/Count)
* **Purpose:** Identifies contractor-type accounts
* **Churn Relevance:** ⭐⭐ Account type segmentation

#### Renewal_Year (long)
* **Description:** Year of renewal
* **Type:** Numeric (Year)
* **Purpose:** Temporal segmentation
* **Churn Relevance:** ⭐⭐⭐ Yearly trends

---

## Data Insights

### Customer Distribution
* **46,819 unique customers** across 115,661 billing records
* Some customers have multiple billing records (renewals, adjustments)
* Customer tenure spans from 2000 to 2026 (26 years of data)

### Pricing Structure
* **14 distinct pricing bands** from Band A to Band J, plus Group
* Band B is most common (31,043 records) indicating mid-market focus
* Pricing varies significantly by band and connection size

### Auto-Renewal Adoption
* **94.8% of customers (109,647)** have auto-renewal enabled
* Only 5.2% require manual renewal - **these are higher churn risk**
* **47.5% have saved payment tokens** - reduces renewal friction

### Account Health
* **63.4% are "Published"** (fully accredited and active)
* **62.5% are "Accredited"** - healthy accounts
* **Failed statuses (questionnaire/info not received)** account for ~16,600 records - **HIGH CHURN RISK**

### Connection Patterns
* **31.2% are single connection** customers
* **20.4% are independent** contractors
* **Large operations (10+)** represent 6.8% - likely more stable

---

## Churn Prediction Relevance

### Critical Features for Churn Model
1. **Prospect_Renewal_Date** - Defines the post-renewal period
2. **Prospect_Outcome** - Target variable (Won/Lost)
3. **Total_Renewal_Score_New** - Composite churn score
4. **Current_Auto_Renewal_Flag** - Strong predictor
5. **Proforma_Audit_Status** - "Failed" = high risk
6. **Proforma_Account_Stage** - "Suspended" = high risk
7. **Payment_Timeframe** - Late payments signal risk
8. **Anchoring_Score & Current_Anchorings** - Mandatory renewals reduce churn
9. **Tenure_Scores** - Loyalty indicator
10. **Band** - Price sensitivity varies by segment

### Post-Renewal Feature Engineering
According to the project requirements, **post-renewal features should be extracted from the renewal_calls dataset where call_date is AFTER prospect_renewal_date**.

This table provides:
* **Customer baseline characteristics**
* **Historical payment behavior**
* **Pre-renewal scores and statuses**
* **The renewal date threshold** for defining "post-renewal"

---

## Usage Recommendations

### For EDA (Exploratory Data Analysis)
```python
# Load billings data
billings = spark.table("ds_p.default.billings")

# Key churn indicators
billings.groupBy("Current_Auto_Renewal_Flag", "Prospect_Outcome").count().show()
billings.groupBy("Proforma_Audit_Status").agg({"Prospect_Outcome": "count"}).show()
billings.groupBy("Band").agg({"Total_Renewal_Score_New": "avg"}).show()
```

### For Joining with Renewal Calls
```python
# Join to extract post-renewal call features
renewal_calls = spark.table("ds_p.default.renewal_calls")

# Get post-renewal calls only
post_renewal = billings.join(
    renewal_calls, 
    on="Co_Ref"
).filter(
    renewal_calls.Call_Date > billings.Prospect_Renewal_Date
)
```

---

## Data Quality Notes
* Some dates extend to 2050 (future renewals) - likely placeholders
* Certain categorical fields have data quality issues (lowercase variants, unexpected values)
* Null values exist across many numeric fields - requires imputation strategy
* Some scores may be on different scales - normalization needed

---

**Last Updated:** 2026-04-10  
**Contact:** Data Science Team  
**Project:** Post-Renewal Churn Prediction Model
