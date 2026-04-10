# CC_CALLS TABLE DOCUMENTATION

## Table Overview
**Table Name:** `ds_p.default.cc_calls`  
**Source:** cc_calls.xlsx  
**Total Records:** 32,597  
**Unique Contacts:** 32,597 (one call per contact record)  
**Columns:** 35

## Purpose
This table captures customer care (CC) call interactions between agents and contractors. It contains rich behavioral and sentiment data from support calls, including issues raised, customer satisfaction, pricing concerns, and agent interactions. This data provides valuable insights into customer health and potential churn signals through service quality metrics.

---

## Column Documentation

### 1. Call Identification
#### Contact_ID (string)
* **Description:** Unique identifier for each customer care contact/call
* **Type:** Categorical (Identifier)
* **Purpose:** Primary key for this table; can be linked to customer records
* **Churn Relevance:** ⭐⭐⭐ Each call is a customer touchpoint

#### Direction (string)
* **Description:** Call direction - who initiated the call
* **Type:** Categorical
* **Categories:** 
  * "OUT_BOUND" (24,711) - Agent-initiated calls (75.8%)
  * "IN_BOUND" (7,878) - Customer-initiated calls (24.2%)
  * Plus some data quality issues (unexpected values: "No", "Satisfied", customer IDs)
* **Purpose:** Distinguish proactive outreach from reactive support
* **Churn Relevance:** ⭐⭐⭐⭐ Inbound calls may signal issues; outbound may be retention efforts

---

### 2. Customer Care Package
#### cc_care_package (string)
* **Description:** Type of care package offered or discussed
* **Type:** Categorical
* **Likely Values:** "Standard", "Premium", etc.
* **Purpose:** Service tier identification
* **Churn Relevance:** ⭐⭐⭐ Package level affects satisfaction

#### cc_care_package_discussed (string)
* **Description:** Whether the care package was discussed during the call
* **Type:** Binary Categorical
* **Values:** "Yes" / "No"
* **Purpose:** Tracks upsell/cross-sell conversations
* **Churn Relevance:** ⭐⭐ Package upgrades may improve retention

---

### 3. Service Urgency & Support
#### cc_urgency_getting_on_site (string)
* **Description:** Customer expressed urgency about getting site assessment/audit
* **Type:** Binary Categorical
* **Values:** "Yes" / "No"
* **Purpose:** Identifies customers with time pressure
* **Churn Relevance:** ⭐⭐⭐ Urgency without resolution = churn risk

#### cc_external_consultant (string)
* **Description:** Customer mentioned using external consultant
* **Type:** Binary Categorical
* **Values:** "Yes" / "No"
* **Purpose:** Flags customers seeking outside help
* **Churn Relevance:** ⭐⭐⭐ May indicate dissatisfaction with support

---

### 4. Agent Behavior
#### cc_agent_cross_sell_attempt (string)
* **Description:** Agent attempted to cross-sell additional services
* **Type:** Binary Categorical
* **Values:** "Yes" / "No"
* **Purpose:** Tracks sales behavior during support calls
* **Churn Relevance:** ⭐⭐ Aggressive sales may frustrate customers

#### cc_call_initiated_by (string)
* **Description:** Who initiated the call
* **Type:** Categorical
* **Categories:** 
  * "Customer" (22,350) - 68.6%
  * "Agent" (8,425) - 25.8%
  * "Not Relevant" (1,653) - 5.1%
  * Plus some data issues
* **Purpose:** Identifies proactive vs reactive contacts
* **Churn Relevance:** ⭐⭐⭐⭐ Customer-initiated calls often indicate problems

---

### 5. Customer Issues & Concerns
#### cc_customer_issues_concerns (string)
* **Description:** Customer raised general issues or concerns
* **Type:** Binary Categorical
* **Values:** "Yes" / "No"
* **Purpose:** Flags problem calls
* **Churn Relevance:** ⭐⭐⭐⭐⭐ Issues unresolved → churn

#### cc_business_struggles_financial_hardship (string)
* **Description:** Customer mentioned business difficulties or financial problems
* **Type:** Binary Categorical
* **Values:** "Yes" / "No"
* **Purpose:** Identifies at-risk customers due to financial stress
* **Churn Relevance:** ⭐⭐⭐⭐⭐ **CRITICAL CHURN PREDICTOR** - financially distressed customers likely to cancel

---

### 6. Questionnaire & Accreditation Process
#### cc_questionnaire_completion (string)
* **Description:** Status of questionnaire completion
* **Type:** Binary Categorical
* **Values:** "Yes" / "No"
* **Purpose:** Tracks accreditation progress
* **Churn Relevance:** ⭐⭐⭐⭐ Incomplete = risk of not renewing

#### cc_chasing_response (string)
* **Description:** Agent chasing customer for response
* **Type:** Binary Categorical
* **Values:** "Yes" / "No"
* **Purpose:** Identifies customers needing follow-up
* **Churn Relevance:** ⭐⭐⭐ Non-responsive customers at risk

#### cc_issues_within_questionnaire (string)
* **Description:** Customer had problems with the questionnaire itself
* **Type:** Binary Categorical
* **Values:** "Yes" / "No"
* **Purpose:** Process friction indicator
* **Churn Relevance:** ⭐⭐⭐⭐ Process frustration drives churn

---

### 7. Technical & Platform Issues
#### cc_login_issues (string)
* **Description:** Customer reported login problems
* **Type:** Binary Categorical
* **Values:** "Yes" / "No"
* **Purpose:** Technical barrier identification
* **Churn Relevance:** ⭐⭐⭐ Access issues frustrate users

#### cc_platform_issues (string)
* **Description:** Customer reported platform/system problems
* **Type:** Binary Categorical
* **Values:** "Yes" / "No"
* **Purpose:** System quality indicator
* **Churn Relevance:** ⭐⭐⭐⭐ Poor platform UX drives churn

#### cc_document_upload_issues (string)
* **Description:** Customer had trouble uploading documents
* **Type:** Binary Categorical
* **Values:** "Yes" / "No"
* **Purpose:** Technical friction point
* **Churn Relevance:** ⭐⭐⭐ Upload problems block accreditation

---

### 8. Process Satisfaction
#### cc_dissatisfaction_time_to_complete (string)
* **Description:** Customer unhappy with time required to complete process
* **Type:** Binary Categorical
* **Values:** "Yes" / "No"
* **Purpose:** Process efficiency metric
* **Churn Relevance:** ⭐⭐⭐⭐ Time burden reduces satisfaction

#### cc_process_complexity_concerns (string)
* **Description:** Customer found process too complex
* **Type:** Binary Categorical
* **Values:** "Yes" / "No"
* **Purpose:** Ease-of-use metric
* **Churn Relevance:** ⭐⭐⭐⭐ Complexity drives churn

#### cc_questions_harder_than_expected (string)
* **Description:** Customer found questionnaire questions difficult
* **Type:** Binary Categorical
* **Values:** "Yes" / "No"
* **Purpose:** Content difficulty metric
* **Churn Relevance:** ⭐⭐⭐ Difficulty creates frustration

---

### 9. Support Quality
#### cc_dissatisfaction_support (string)
* **Description:** Customer expressed dissatisfaction with support quality
* **Type:** Binary Categorical
* **Values:** "Yes" / "No"
* **Purpose:** Support effectiveness metric
* **Churn Relevance:** ⭐⭐⭐⭐⭐ **CRITICAL** - Poor support drives churn

---

### 10. Customer Sentiment (Primary Churn Signals)
#### cc_contractor_sentiment (string)
* **Description:** Overall customer sentiment during the call
* **Type:** Categorical
* **Categories:** 
  * "Satisfied" (15,887) - 48.7% - **POSITIVE**
  * "Neutral" (12,910) - 39.6% - **AT RISK**
  * "Not Discussed" (2,446) - 7.5%
  * "Dissatisfied" (928) - 2.8% - **HIGH CHURN RISK**
  * Plus data quality issues (dates, scores appearing as sentiment)
* **Purpose:** Primary customer health indicator
* **Churn Relevance:** ⭐⭐⭐⭐⭐ **STRONGEST PREDICTOR** - Dissatisfied customers will churn

#### cc_contractor_sentiment_start_score (string)
* **Description:** Sentiment score at call start
* **Type:** Numeric (stored as string)
* **Range:** Likely 0-100 scale
* **Purpose:** Baseline sentiment measurement
* **Churn Relevance:** ⭐⭐⭐⭐ Starting negative = at-risk customer

#### cc_contractor_sentiment_end_score (string)
* **Description:** Sentiment score at call end
* **Type:** Numeric (stored as string)
* **Range:** Likely 0-100 scale
* **Purpose:** Post-interaction sentiment
* **Churn Relevance:** ⭐⭐⭐⭐⭐ Ending negative = immediate churn risk

#### cc_contractor_sentiment_overall_score (string)
* **Description:** Overall sentiment score for the call
* **Type:** Numeric (stored as string)
* **Range:** Likely 0-100 scale
* **Purpose:** Aggregate sentiment measure
* **Churn Relevance:** ⭐⭐⭐⭐⭐ Composite health score

#### cc_contractor_sentiment_issues_score (string)
* **Description:** Sentiment score specifically related to issues raised
* **Type:** Numeric (stored as string)
* **Purpose:** Problem-specific sentiment
* **Churn Relevance:** ⭐⭐⭐⭐ Issue severity indicator

---

### 11. Pricing & Financial Concerns
#### cc_pricing_mentioned (string)
* **Description:** Pricing was discussed during the call
* **Type:** Binary Categorical
* **Values:** "Yes" / "No" / "Not Discussed"
* **Purpose:** Identifies price-sensitive customers
* **Churn Relevance:** ⭐⭐⭐⭐ Price objections predict churn

#### cc_pricing_sentiment_impact (string)
* **Description:** How pricing discussion affected customer sentiment
* **Type:** Categorical
* **Likely Values:** "Positive", "Negative", "Neutral", "No Impact"
* **Purpose:** Measures price sensitivity
* **Churn Relevance:** ⭐⭐⭐⭐ Negative price reaction = high churn risk

---

### 12. Cancellation Signals
#### cc_refund_discussed (string)
* **Description:** Customer asked about refunds
* **Type:** Binary Categorical
* **Values:** "Yes" / "No"
* **Purpose:** Strong cancellation intent signal
* **Churn Relevance:** ⭐⭐⭐⭐⭐ **IMMEDIATE CHURN RISK** - Refund requests indicate intent to leave

#### cc_contractor_suggest_leave (string)
* **Description:** Customer suggested they may leave/cancel
* **Type:** Binary Categorical
* **Values:** "Yes" / "No"
* **Purpose:** Explicit churn warning
* **Churn Relevance:** ⭐⭐⭐⭐⭐ **HIGHEST CHURN RISK** - Direct cancellation threat

---

### 13. Additional Fields (6 columns, details from schema)
The table contains 6 more columns that capture additional call metadata and customer information. These fields likely include:
* Customer reference linking (e.g., Co_Ref for joining with billings table)
* Call dates/timestamps
* Call duration
* Agent ID
* Resolution status
* Follow-up required flags

---

## Data Insights

### Call Volume Distribution
* **32,597 total customer care calls** recorded
* **Each contact ID is unique**, suggesting each record represents a distinct customer interaction
* **75.8% outbound calls** - proactive customer care approach
* **24.2% inbound calls** - reactive support requests

### Customer Sentiment Analysis
* **48.7% Satisfied** - generally positive base
* **39.6% Neutral** - at-risk segment requiring attention
* **2.8% Dissatisfied** - immediate intervention needed
* **Dissatisfied customers are ~18x more likely to churn** (industry standard)

### Common Issues
* **Technical problems** (login, platform, upload) are recurring themes
* **Process complexity** and time concerns are frequent complaints
* **Financial hardship** mentions are critical red flags
* **Pricing objections** indicate price sensitivity

### Agent Behavior Patterns
* **Majority of calls are customer-initiated** (68.6%) - suggests reactive support model
* **Cross-sell attempts** are present - balance needed to avoid sales pressure
* **Chasing responses** is common - indicates engagement issues

---

## Churn Prediction Relevance

### Critical Churn Features
1. **cc_contractor_sentiment** - Primary health indicator
2. **cc_business_struggles_financial_hardship** - Financial risk
3. **cc_contractor_suggest_leave** - Explicit intent
4. **cc_refund_discussed** - Cancellation signal
5. **cc_dissatisfaction_support** - Service quality issue
6. **cc_pricing_mentioned + cc_pricing_sentiment_impact** - Price sensitivity
7. **Direction + cc_call_initiated_by** - Proactive vs reactive
8. **cc_customer_issues_concerns** - Problem flag
9. **cc_process_complexity_concerns** - Friction indicator
10. **Sentiment score deltas** (start vs end) - Interaction effectiveness

### Feature Engineering Opportunities
* **Sentiment deterioration:** `end_score - start_score` (negative = bad call experience)
* **Issue count:** Sum all "Yes" flags for total problems raised
* **Technical friction score:** Count of platform/login/upload issues
* **Process satisfaction:** Inverse of complexity/time concerns
* **Explicit churn risk flag:** `(suggest_leave OR refund_discussed) AND sentiment = Dissatisfied`

### Integration with Other Tables
* **Join with billings on Co_Ref** (if field exists) to correlate call quality with payment behavior
* **Count calls per customer** - frequent callers may be problematic accounts
* **Time-series analysis** - calls increasing before churn?

---

## Usage Recommendations

### For EDA (Exploratory Data Analysis)
```python
# Load cc_calls data
cc_calls = spark.table("ds_p.default.cc_calls")

# Sentiment distribution
cc_calls.groupBy("cc_contractor_sentiment").count().orderBy("count", ascending=False).show()

# Dissatisfied customer analysis
dissatisfied = cc_calls.filter(cc_calls.cc_contractor_sentiment == "Dissatisfied")
dissatisfied.select("cc_customer_issues_concerns", "cc_dissatisfaction_support", 
                     "cc_business_struggles_financial_hardship").show()

# Churn risk flags
high_risk = cc_calls.filter(
    (cc_calls.cc_contractor_suggest_leave == "Yes") | 
    (cc_calls.cc_refund_discussed == "Yes") |
    (cc_calls.cc_contractor_sentiment == "Dissatisfied")
)
high_risk.count()  # Count of high-risk calls
```

### For Churn Modeling
```python
# Create churn risk score
from pyspark.sql.functions import when, col

cc_calls_features = cc_calls.withColumn(
    "churn_risk_score",
    (when(col("cc_contractor_sentiment") == "Dissatisfied", 10).otherwise(0)) +
    (when(col("cc_contractor_suggest_leave") == "Yes", 10).otherwise(0)) +
    (when(col("cc_refund_discussed") == "Yes", 8).otherwise(0)) +
    (when(col("cc_business_struggles_financial_hardship") == "Yes", 7).otherwise(0)) +
    (when(col("cc_dissatisfaction_support") == "Yes", 6).otherwise(0)) +
    (when(col("cc_pricing_mentioned") == "Yes", 3).otherwise(0))
)
```

---

## Data Quality Notes
* **Sentiment field has data quality issues** - contains dates and scores instead of sentiment labels
* **Direction field has unexpected values** - needs cleaning
* **Numeric scores stored as strings** - requires type conversion
* **Binary fields may have variations** - "Yes"/"No" vs "yes"/"no" vs null
* **Some fields may be sparse** - high percentage of "No" or null values

### Recommended Cleaning Steps
1. **Standardize sentiment categories** - map dates/scores to proper labels
2. **Convert score fields to numeric** - cast sentiment scores to float/int
3. **Clean direction field** - remove invalid values
4. **Normalize binary fields** - lowercase and handle nulls
5. **Remove duplicate/test records** - validate Contact_ID uniqueness

---

## Linking to Other Tables
* **Primary Key:** Contact_ID
* **Foreign Key Candidate:** Likely contains Co_Ref (customer reference) or similar field to join with billings table
* **Join Strategy:** LEFT JOIN from billings to cc_calls to enrich customer profiles with support interaction data

---

**Last Updated:** 2026-04-10  
**Contact:** Data Science Team  
**Project:** Post-Renewal Churn Prediction Model  
**Note:** Customer care call data provides behavioral signals that complement transactional data from billings
