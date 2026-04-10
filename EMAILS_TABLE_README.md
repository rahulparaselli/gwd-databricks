# EMAILS TABLE DOCUMENTATION

## Table Overview
**Table Name:** `ds_p.default.emails`  
**Source:** emails.xlsx  
**Total Records:** 115,866  
**Unique Customers:** 37,891  
**Columns:** 27

## Purpose
This table captures email communications and CRM interactions between agents and contractors throughout the membership lifecycle. It tracks customer engagement, sentiment evolution, accreditation progress, payment intentions, and competitive threats. This data provides longitudinal behavioral signals essential for understanding customer journey and predicting churn.

---

## Column Documentation

### 1. Customer Identification & Timing
#### Co_Ref (string)
* **Description:** Customer Reference ID - links to billings table
* **Type:** Categorical (Identifier)
* **Purpose:** Foreign key for joining with billings and other tables
* **Churn Relevance:** ⭐⭐⭐⭐⭐ Essential for customer-level churn prediction

#### Time_to_Renewal (string)
* **Description:** Time remaining until renewal date
* **Type:** Temporal/Categorical
* **Purpose:** Indicates urgency/proximity to renewal decision
* **Churn Relevance:** ⭐⭐⭐⭐⭐ Closer to renewal = critical engagement period

---

### 2. Accreditation Progress
#### crm_accreditation_completed (string)
* **Description:** Whether customer completed accreditation process
* **Type:** Binary Categorical
* **Values:** "Yes" / "No"
* **Purpose:** Tracks completion of certification
* **Churn Relevance:** ⭐⭐⭐⭐⭐ **CRITICAL** - Incomplete accreditation = likely non-renewal

#### crm_timely_completion (string)
* **Description:** Accreditation completed on time
* **Type:** Binary Categorical
* **Values:** "Yes" / "No"
* **Purpose:** Measures process efficiency
* **Churn Relevance:** ⭐⭐⭐ Delays may cause frustration

#### crm_progress_towards_accreditation (string)
* **Description:** Customer making progress toward certification
* **Type:** Binary Categorical
* **Values:** "Yes" / "No"
* **Purpose:** Early indicator of engagement
* **Churn Relevance:** ⭐⭐⭐⭐ No progress = disengagement

#### crm_delays_in_accreditation (string)
* **Description:** Customer experienced delays in the process
* **Type:** Binary Categorical
* **Values:** "Yes" / "No"
* **Purpose:** Identifies process friction
* **Churn Relevance:** ⭐⭐⭐⭐ Delays create dissatisfaction

#### crm_accreditation_issues (string)
* **Description:** Customer reported problems with accreditation
* **Type:** Binary Categorical
* **Values:** "Yes" / "No"
* **Purpose:** Problem flag
* **Churn Relevance:** ⭐⭐⭐⭐ Issues predict abandonment

---

### 3. Customer Intent Signals
#### crm_contractor_suggested_leave (string)
* **Description:** Customer explicitly mentioned leaving/canceling
* **Type:** Binary Categorical
* **Values:** "Yes" / "No"
* **Purpose:** **EXPLICIT CHURN WARNING**
* **Churn Relevance:** ⭐⭐⭐⭐⭐ **HIGHEST RISK** - Direct cancellation threat

#### crm_customer_payment_intention (string)
* **Description:** Customer's stated intention to pay/renew
* **Type:** Categorical
* **Categories:** 
  * "Not Discussed" (64,511) - 55.7% - No clear intent
  * "Yes" (26,204) - 22.6% - **POSITIVE** - Will pay
  * "No" (4,337) - 3.7% - **CHURN RISK** - Won't pay
  * Plus data issues
* **Purpose:** Direct measure of renewal likelihood
* **Churn Relevance:** ⭐⭐⭐⭐⭐ **STRONGEST PREDICTOR** - "No" = immediate churn

---

### 4. Customer Engagement & Sentiment
#### crm_contractor_engagement (string)
* **Description:** Level of customer engagement with communications
* **Type:** Categorical
* **Likely Values:** "High", "Medium", "Low", "Unresponsive"
* **Purpose:** Measures responsiveness
* **Churn Relevance:** ⭐⭐⭐⭐⭐ Low engagement predicts churn

#### crm_contractor_sentiment (string)
* **Description:** Customer sentiment expressed in emails
* **Type:** Categorical
* **Categories:** 
  * "Neutral" (49,804) - 43.0% - **WATCH** - Could go either way
  * "Not Discussed" (29,264) - 25.3%
  * "Satisfied" (10,218) - 8.8% - **POSITIVE**
  * "Dissatisfied" (5,765) - 5.0% - **HIGH RISK**
  * Plus variations
* **Purpose:** Emotional state tracking
* **Churn Relevance:** ⭐⭐⭐⭐⭐ Dissatisfied = high churn probability

#### crm_contractor_sentiment_score (string)
* **Description:** Numeric sentiment score
* **Type:** Numeric (stored as string)
* **Range:** Likely 0-100
* **Purpose:** Quantifiable sentiment metric
* **Churn Relevance:** ⭐⭐⭐⭐⭐ Lower scores = churn risk

---

### 5. Certification Requirements
#### crm_dts_or_ssip_mentioned (string)
* **Description:** DTS (Diffusion Tensor Spectroscopy) or SSiP certification discussed
* **Type:** Binary Categorical
* **Values:** "Yes" / "No"
* **Purpose:** Tracks specific certification needs
* **Churn Relevance:** ⭐⭐⭐ Alternative certifications may reduce need

---

### 6. Competitive Threats
#### crm_competitors_mentioned (string)
* **Description:** Customer mentioned competing services
* **Type:** Binary Categorical
* **Values:** "Yes" / "No"
* **Purpose:** **COMPETITIVE THREAT FLAG**
* **Churn Relevance:** ⭐⭐⭐⭐⭐ Competitor mentions = high switching risk

---

### 7. Membership Status
#### crm_membership_level (string)
* **Description:** Customer's membership tier/level
* **Type:** Categorical
* **Likely Values:** "Basic", "Standard", "Premium", "Enterprise"
* **Purpose:** Service tier segmentation
* **Churn Relevance:** ⭐⭐⭐ Different tiers have different retention patterns

#### crm_membership_overdue (string)
* **Description:** Membership payment is overdue
* **Type:** Binary Categorical
* **Values:** "Yes" / "No"
* **Purpose:** Payment delinquency flag
* **Churn Relevance:** ⭐⭐⭐⭐⭐ **CRITICAL** - Overdue payment = imminent churn

---

### 8. Platform & Service Issues
#### crm_platform_issues_raised (string)
* **Description:** Customer reported technical/platform problems
* **Type:** Binary Categorical
* **Values:** "Yes" / "No"
* **Purpose:** Technical satisfaction metric
* **Churn Relevance:** ⭐⭐⭐⭐ Platform problems drive churn

---

### 9. Agent Behavior & Communication
#### crm_agent_chased_contractor (string)
* **Description:** Agent had to follow up/chase customer
* **Type:** Binary Categorical
* **Values:** "Yes" / "No"
* **Purpose:** Engagement difficulty indicator
* **Churn Relevance:** ⭐⭐⭐⭐ Chasing = disengagement = churn risk

#### crm_agent_chase_count (string)
* **Description:** Number of times agent chased customer
* **Type:** Numeric (stored as string)
* **Purpose:** Quantifies disengagement severity
* **Churn Relevance:** ⭐⭐⭐⭐⭐ High chase count = very high risk

---

### 10. Auto-Renewal
#### crm_auto_renewal_status (string)
* **Description:** Auto-renewal setup status
* **Type:** Categorical
* **Categories:** 
  * "0" (97,834) - 84.4% - No auto-renewal / Status 0
  * "2" (4,440) - 3.8% - Status 2 (possibly active)
  * "1" (2,304) - 2.0% - Status 1 (possibly pending)
  * "Not Discussed" (18)
  * "Yes" (3)
  * "No" (7)
* **Purpose:** Auto-pay enrollment tracking
* **Churn Relevance:** ⭐⭐⭐⭐⭐ No auto-renewal = higher manual churn risk

---

### 11. Pricing & Financial Concerns
#### crm_dissatisified_with_renewal_price (string)
* **Description:** Customer expressed pricing objections
* **Type:** Binary Categorical
* **Values:** "Yes" / "No"
* **Purpose:** Price sensitivity flag
* **Churn Relevance:** ⭐⭐⭐⭐⭐ **MAJOR CHURN DRIVER** - Price objections

---

### 12. Complaint & Negative Experience
#### crm_customer_complained (string)
* **Description:** Customer filed a complaint
* **Type:** Binary Categorical
* **Values:** "Yes" / "No"
* **Purpose:** Dissatisfaction escalation
* **Churn Relevance:** ⭐⭐⭐⭐⭐ Complaints = high churn risk

#### crm_refund_mentioned (string)
* **Description:** Customer asked about refunds
* **Type:** Binary Categorical
* **Values:** "Yes" / "No"
* **Purpose:** Cancellation intent signal
* **Churn Relevance:** ⭐⭐⭐⭐⭐ Refund request = likely churning

#### crm_negative_customer_experience (string)
* **Description:** Customer had a negative experience
* **Type:** Binary Categorical
* **Values:** "Yes" / "No"
* **Purpose:** General dissatisfaction flag
* **Churn Relevance:** ⭐⭐⭐⭐ Bad experiences reduce loyalty

---

### 13. Additional Fields (3 columns)
The table contains 3 more fields that likely include metadata or additional tracking information.

---

## Data Insights

### Email Volume & Coverage
* **115,866 total email interactions** across 37,891 unique customers
* **Average 3.06 emails per customer** - indicates ongoing communication
* **Email data complements call data** (cc_calls) for full engagement picture

### Customer Sentiment Distribution
* **43.0% Neutral** - largest segment, requires nurturing
* **25.3% Not Discussed** - sentiment not captured
* **8.8% Satisfied** - lowest risk group
* **5.0% Dissatisfied** - immediate intervention needed
* **Neutral customers are conversion opportunities** (could go positive or negative)

### Payment Intent Analysis
* **22.6% expressed intent to pay** - good conversion prospects
* **3.7% explicitly said "No"** - lost customers
* **55.7% not discussed** - need to engage and clarify

### Accreditation Challenges
* Accreditation completion, delays, and issues are tracked
* Customers struggling with certification are at risk
* Timely completion predicts renewal

### Engagement Patterns
* **Agent chasing is common** - indicates responsiveness issues
* **High chase counts** correlate with disengagement
* **Platform issues** create friction

### Competitive Threats
* Competitor mentions are tracked - direct churn threat
* Pricing dissatisfaction is common - main objection

---

## Churn Prediction Relevance

### Critical Churn Features
1. **crm_customer_payment_intention** - "No" = churn, "Yes" = renew
2. **crm_contractor_suggested_leave** - Explicit churn intent
3. **crm_contractor_sentiment** - Dissatisfied = high risk
4. **crm_refund_mentioned** - Cancellation signal
5. **crm_dissatisified_with_renewal_price** - Price objection
6. **crm_customer_complained** - Escalated dissatisfaction
7. **crm_accreditation_completed** - Incomplete = won't renew
8. **crm_membership_overdue** - Payment delinquency
9. **crm_competitors_mentioned** - Switching risk
10. **crm_agent_chase_count** - Disengagement severity
11. **crm_auto_renewal_status** - No auto-pay = higher risk
12. **crm_contractor_engagement** - Low engagement = churn

### Feature Engineering Opportunities
* **Churn risk score:** Weighted sum of negative flags
* **Engagement score:** Inverse of chase count + response rate
* **Sentiment trend:** Change in sentiment over time (requires temporal join)
* **Issue count:** Sum of platform_issues + accreditation_issues + delays
* **Payment risk flag:** (payment_intention='No' OR membership_overdue='Yes')
* **Explicit churn intent:** (suggested_leave='Yes' OR refund_mentioned='Yes')

### Integration with Other Tables
* **Join with billings on Co_Ref** - correlate email behavior with payment history
* **Join with renewal_calls** - combine email and call interaction data
* **Aggregate email features by customer** - total emails, latest sentiment, issue counts

---

## Usage Recommendations

### For EDA (Exploratory Data Analysis)
```python
# Load emails data
emails = spark.table("ds_p.default.emails")

# Payment intention analysis
emails.groupBy("crm_customer_payment_intention").count().show()

# Sentiment distribution
emails.groupBy("crm_contractor_sentiment").count().orderBy("count", ascending=False).show()

# High-risk customers
high_risk = emails.filter(
    (emails.crm_customer_payment_intention == "No") |
    (emails.crm_contractor_suggested_leave == "Yes") |
    (emails.crm_contractor_sentiment == "Dissatisfied")
)
print(f"High-risk customers: {high_risk.select('Co_Ref').distinct().count()}")

# Accreditation completion rate
emails.groupBy("crm_accreditation_completed").count().show()
```

### For Churn Modeling
```python
# Create churn risk features
from pyspark.sql.functions import when, col, sum as _sum

email_features = emails.groupBy("Co_Ref").agg(
    _sum(when(col("crm_contractor_sentiment") == "Dissatisfied", 1).otherwise(0)).alias("dissatisfied_email_count"),
    _sum(when(col("crm_customer_payment_intention") == "No", 1).otherwise(0)).alias("no_payment_intent_count"),
    _sum(when(col("crm_contractor_suggested_leave") == "Yes", 1).otherwise(0)).alias("leave_mention_count"),
    _sum(when(col("crm_competitors_mentioned") == "Yes", 1).otherwise(0)).alias("competitor_mention_count"),
    _sum(when(col("crm_refund_mentioned") == "Yes", 1).otherwise(0)).alias("refund_request_count")
)

# Churn risk score
email_features = email_features.withColumn(
    "email_churn_risk_score",
    col("no_payment_intent_count") * 10 +
    col("leave_mention_count") * 10 +
    col("dissatisfied_email_count") * 5 +
    col("refund_request_count") * 8 +
    col("competitor_mention_count") * 6
)
```

---

## Data Quality Notes
* **Auto-renewal status uses numeric codes** - needs mapping
* **Some fields have data quality issues** - narrative text instead of values
* **Binary fields may have variations** - standardization needed
* **Sentiment field has sparse "Not Discussed"** - imputation or separate flag
* **Multiple emails per customer** - requires aggregation for customer-level features

### Recommended Cleaning Steps
1. **Standardize binary fields** - "Yes"/"No" consistency
2. **Map auto_renewal_status codes** - 0/1/2 to meaningful categories
3. **Convert sentiment_score to numeric** - currently stored as string
4. **Remove narrative text entries** - clean categorical fields
5. **Handle "Not Discussed" values** - treat as missing or neutral
6. **Aggregate to customer level** - for modeling

---

## Linking to Other Tables
* **Primary Key:** Co_Ref (customer reference)
* **Foreign Key Relationships:**
  * → `billings.Co_Ref` (customer billing info)
  * → `renewal_calls.Co_Ref` (renewal call interactions)
  * → `cc_calls` (may link via customer reference if available)
* **Join Strategy:** LEFT JOIN from billings to emails to enrich customer profiles with email engagement data

---

**Last Updated:** 2026-04-10  
**Contact:** Data Science Team  
**Project:** Post-Renewal Churn Prediction Model  
**Note:** Email data provides longitudinal behavioral signals and explicit customer intent that are highly predictive of churn
