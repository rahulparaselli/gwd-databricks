# RENEWAL_CALLS TABLE DOCUMENTATION

## Table Overview
**Table Name:** `ds_p.default.renewal_calls`  
**Source:** renewal_calls.xlsx  
**Total Records:** 186,528  
**Unique Customers:** 36,303  
**Columns:** 38  
**Call Date Range:** 2024-04-02 to 2026-02-13

## Purpose
🎯 **THIS IS THE MOST CRITICAL TABLE FOR POST-RENEWAL CHURN PREDICTION**

This table captures detailed renewal conversation data including customer reactions, agent pitches, churn reasons, pricing discussions, competitive threats, and final renewal decisions. 

**KEY PROJECT REQUIREMENT:** According to the project specifications, **post-renewal features must be extracted from renewal calls where Call_Date occurs AFTER the Prospect_Renewal_Date from the billings table**. This temporal filtering is essential for building a model that predicts churn in the post-renewal period.

---

## Column Documentation

### 1. Call Identification & Timing

#### Call_ID (long)
* **Description:** Unique identifier for each renewal call
* **Type:** Numeric (Identifier)
* **Purpose:** Primary key for this table
* **Churn Relevance:** ⭐⭐⭐ Essential for tracking individual interactions

#### Co_Ref (string)
* **Description:** Customer Reference ID
* **Type:** Categorical (Identifier)
* **Purpose:** Foreign key linking to billings table
* **Churn Relevance:** ⭐⭐⭐⭐⭐ **ESSENTIAL** - Links calls to customer records and billings.Prospect_Renewal_Date

#### Call_Date (timestamp)
* **Description:** **🔥 CRITICAL FIELD** - Date when renewal call occurred
* **Type:** Date/Timestamp
* **Range:** 2024-04-02 to 2026-02-13
* **Purpose:** **DEFINES POST-RENEWAL PERIOD** - Filter where Call_Date > billings.Prospect_Renewal_Date
* **Churn Relevance:** ⭐⭐⭐⭐⭐ **MOST IMPORTANT** - Temporal filter for post-renewal feature engineering

---

### 2. Churn Category & Primary Reason

#### Churn_Category (string)
* **Description:** **PRIMARY CHURN REASON** - Why customer might churn
* **Type:** Categorical
* **Top Categories:** 
  * "Unnecessary / Not needed" (1,689) - No longer require service
  * "Cost / Price / Too expensive" (1,527) - **PRICE SENSITIVITY**
  * "Financial struggles / Business Problems" (948) - **FINANCIAL DISTRESS**
  * "Left / Not with client anymore" (811) - Lost client requirement
  * "Not Mentioned" (588) - No reason given
  * "Lack of Benefits" (529) - Value perception issue
  * "Accreditation / Certification" (335) - Compliance concerns
  * "Switch / Change / Alternate Provider" (289) - **COMPETITIVE LOSS**
  * "Customer Service / Support" (233) - Service quality issue
  * "Payment / Invoice Issue" (207) - Billing problems
  * Plus 8 more categories
* **Purpose:** **TARGET VARIABLE INSIGHTS** - Categorizes churn drivers
* **Churn Relevance:** ⭐⭐⭐⭐⭐ **CRITICAL** - Direct churn causation

---

### 3. Complaint & Issues

#### Complaint_Category (string)
* **Description:** Type of complaint raised during call
* **Type:** Categorical
* **Purpose:** Issue categorization
* **Churn Relevance:** ⭐⭐⭐⭐ Complaints indicate dissatisfaction

#### Serious_Complaint (string)
* **Description:** Severe/escalated complaint flagged
* **Type:** Binary Categorical
* **Values:** "Yes" / "No"
* **Purpose:** Urgent issue indicator
* **Churn Relevance:** ⭐⭐⭐⭐⭐ Serious complaints = high churn risk

#### Other_Complaint (string)
* **Description:** Additional non-serious complaints
* **Type:** Binary Categorical
* **Values:** "Yes" / "No"
* **Purpose:** General dissatisfaction
* **Churn Relevance:** ⭐⭐⭐ Multiple complaints compound risk

---

### 4. Customer Reactions & Responses

#### Customer_Reaction_Category (string)
* **Description:** How customer reacted during the renewal conversation
* **Type:** Categorical
* **Likely Values:** "Positive", "Neutral", "Negative", "Hesitant", "Angry"
* **Purpose:** Emotional response tracking
* **Churn Relevance:** ⭐⭐⭐⭐⭐ Negative reactions predict churn

#### Customer_Renewal_Response_Category (string)
* **Description:** Customer's specific response to renewal pitch
* **Type:** Categorical
* **Top Categories:** 
  * "Agreement" (10,683) - **POSITIVE** - Agreed to renew
  * "Payments and Billings / Invoice" (8,233) - Payment concerns
  * "Communication" (7,894) - Communication issues
  * "Confusion / Uncertainty / Hesitation" (6,367) - **AT RISK** - Unsure about renewal
  * "Price and Cost" (3,349) - **PRICE OBJECTION**
  * "Accreditation and Certification" (3,263) - Process concerns
  * "Cancellation / Termination / Non-Renewal / Withdrawal" (3,118) - **CHURNING**
  * "Not Mentioned" (3,085)
  * "Auto / Automatic" (2,679) - Auto-renewal discussion
  * "Financial Hardship / Struggles" (1,564) - **HIGH RISK**
  * Plus 10 more categories
* **Purpose:** Response sentiment and intent
* **Churn Relevance:** ⭐⭐⭐⭐⭐ **STRONGEST BEHAVIORAL PREDICTOR**

---

### 5. Agent Actions & Pitch

#### Agent_Renewal_Pitch_Category (string)
* **Description:** Type of renewal pitch agent delivered
* **Type:** Categorical
* **Likely Values:** "Value-based", "Discount offer", "Feature highlight", "Relationship-based"
* **Purpose:** Sales approach tracking
* **Churn Relevance:** ⭐⭐⭐ Pitch effectiveness varies

#### Agent_Response_Category (string)
* **Description:** How agent responded to customer concerns
* **Type:** Categorical
* **Likely Values:** "Addressed concerns", "Offered discount", "Escalated", "Standard response"
* **Purpose:** Agent effectiveness measure
* **Churn Relevance:** ⭐⭐⭐⭐ Good responses can save at-risk customers

#### Agent_Renewal_Initiation (string)
* **Description:** Whether agent initiated the renewal conversation
* **Type:** Binary Categorical
* **Values:** "Yes" / "No"
* **Purpose:** Proactive vs reactive engagement
* **Churn Relevance:** ⭐⭐⭐ Proactive outreach may improve retention

#### Agent_Flagged_Membership_Status_Alert (string)
* **Description:** Agent flagged an issue with membership status
* **Type:** Binary Categorical
* **Values:** "Yes" / "No"
* **Purpose:** Status problem indicator
* **Churn Relevance:** ⭐⭐⭐⭐ Status issues block renewal

---

### 6. Final Renewal Decision

#### Membership_Renewal_Decision (string)
* **Description:** **🎯 TARGET VARIABLE** - Customer's final renewal decision
* **Type:** Categorical
* **Categories:** 
  * "No" (77,544) - **CHURNED** - 41.6% did not renew
  * "Yes" (9,010) - **RENEWED** - 4.8% confirmed renewal
  * "Yes/No" (14) - Ambiguous/pending
* **Purpose:** **PRIMARY CHURN LABEL FOR MODELING**
* **Churn Relevance:** ⭐⭐⭐⭐⭐ **THIS IS THE TARGET VARIABLE**

**⚠️ IMPORTANT NOTE:** The high proportion of "No" (41.6%) vs "Yes" (4.8%) suggests:
- Many calls are tracking churn/non-renewal events
- Missing values (53.6% unlabeled) may be "pending" or "unclear" decisions
- For modeling, may need to define churn label logic (e.g., "No" = 1, "Yes" = 0, handle nulls)

---

### 7. Pricing & Discounts

#### Discussion_on_Price_Increase (string)
* **Description:** Price increase was discussed during call
* **Type:** Binary Categorical
* **Values:** "Yes" / "No"
* **Purpose:** Identifies price-sensitive conversations
* **Churn Relevance:** ⭐⭐⭐⭐⭐ Price increases are major churn drivers

#### Renewal_Impact_Due_to_Price_Increase (string)
* **Description:** How price increase affected renewal decision
* **Type:** Categorical
* **Likely Values:** "Positive", "Negative", "Neutral", "Decided not to renew"
* **Purpose:** Measures price elasticity
* **Churn Relevance:** ⭐⭐⭐⭐⭐ Negative impact = churn

#### Discount_or_Waiver_Requested (string)
* **Description:** Customer asked for discount or fee waiver
* **Type:** Binary Categorical
* **Values:** "Yes" / "No"
* **Purpose:** Price negotiation flag
* **Churn Relevance:** ⭐⭐⭐⭐ Discount requests indicate price sensitivity

#### Price_Switching_Mentioned (string)
* **Description:** Customer mentioned switching due to price
* **Type:** Binary Categorical
* **Values:** "Yes" / "No"
* **Purpose:** Price-driven churn threat
* **Churn Relevance:** ⭐⭐⭐⭐⭐ Explicit price-based switching intent

---

### 8. Call Scheduling & Follow-up

#### Call_Reschedule_Request (string)
* **Description:** Customer requested to reschedule the call
* **Type:** Binary Categorical
* **Values:** "Yes" / "No"
* **Purpose:** Engagement delay signal
* **Churn Relevance:** ⭐⭐⭐ Avoidance behavior may indicate churn

---

### 9. Competitive Intelligence

#### Explicit_Competitor_Mention (string)
* **Description:** Customer explicitly named a competitor
* **Type:** Binary Categorical
* **Values:** "Yes" / "No"
* **Purpose:** Direct competitive threat
* **Churn Relevance:** ⭐⭐⭐⭐⭐ Competitor mentions = switching risk

#### Implied_Competitor_Mention (string)
* **Description:** Customer implied competitor without naming
* **Type:** Binary Categorical
* **Values:** "Yes" / "No"
* **Purpose:** Indirect competitive signal
* **Churn Relevance:** ⭐⭐⭐⭐ Still a threat

#### Explicit_Switching_Intent (string)
* **Description:** Customer stated intent to switch providers
* **Type:** Binary Categorical
* **Values:** "Yes" / "No"
* **Purpose:** **IMMEDIATE CHURN THREAT**
* **Churn Relevance:** ⭐⭐⭐⭐⭐ **CRITICAL** - Direct switching statement

#### Implied_Switching_Intent (string)
* **Description:** Customer suggested might switch
* **Type:** Binary Categorical
* **Values:** "Yes" / "No"
* **Purpose:** Potential churn signal
* **Churn Relevance:** ⭐⭐⭐⭐ Exploration phase

#### Mentioned_Competitors (string)
* **Description:** Specific competitor names mentioned
* **Type:** Categorical (Text)
* **Purpose:** Competitive analysis
* **Churn Relevance:** ⭐⭐⭐⭐ Identify main threats

#### Competitor_Benefits_Mentioned (string)
* **Description:** Customer discussed competitor advantages
* **Type:** Binary Categorical
* **Values:** "Yes" / "No"
* **Purpose:** Value proposition comparison
* **Churn Relevance:** ⭐⭐⭐⭐⭐ Competitor benefits attract customers away

---

### 10. Conversation Dynamics

#### Topic_Introduced_By (string)
* **Description:** Who brought up the topic (agent vs customer)
* **Type:** Categorical
* **Values:** "Agent", "Customer", "Both"
* **Purpose:** Initiative tracking
* **Churn Relevance:** ⭐⭐⭐ Customer-initiated concerns = higher risk

---

### 11. Additional Fields (12 columns)
The table contains 12 more columns capturing additional call metadata, possibly including:
* Call duration
* Agent ID
* Call outcome tags
* Follow-up required flags
* Resolution status
* Customer account details
* Temporal indicators (year, month)
* Call direction
* Other behavioral flags

---

## Data Insights

### Call Volume & Coverage
* **186,528 total renewal calls** across 36,303 unique customers
* **Average 5.14 calls per customer** - indicates multiple touchpoints per customer
* **Call timeline spans nearly 2 years** (2024-04 to 2026-02)

### Churn Decision Distribution
* **41.6% "No"** - High proportion of non-renewals captured
* **4.8% "Yes"** - Lower proportion of confirmed renewals
* **53.6% unlabeled** - Missing decisions (likely pending, unclear, or not asked)
* **Class imbalance:** More churn events than renewals in labeled data

### Top Churn Drivers
1. **"Unnecessary / Not needed"** (1,689) - No longer required
2. **"Cost / Price / Too expensive"** (1,527) - Price sensitivity #1 controllable factor
3. **"Financial struggles"** (948) - Economic hardship
4. **"Left client"** (811) - Lost anchoring
5. **"Switch to competitor"** (289) - Direct competition

### Customer Response Patterns
* **"Agreement"** (10,683) - Positive engagement
* **"Confusion / Hesitation"** (6,367) - At-risk segment
* **"Cancellation"** (3,118) - Explicit churn
* **"Financial Hardship"** (1,564) - High-risk segment
* **"Price and Cost"** (3,349) - Price objections

### Price Sensitivity
* **Price increases discussed frequently**
* **Discount requests are common**
* **Price-driven switching is a major threat**
* **Pricing is a controllable lever for retention**

### Competitive Landscape
* **Competitor mentions tracked**
* **Both explicit and implied switching intent captured**
* **Competitor benefits are discussed**
* **Provides intelligence for competitive positioning**

---

## Post-Renewal Churn Prediction Relevance

### 🎯 Project Requirement Reminder
**"Post renewal features should be extracted from the renewal calls dataset through the call_date column (i.e., the call_date should be after the prospect_renewal_date)."**

### Critical Implementation Steps

#### 1. Temporal Filtering (ESSENTIAL)
```python
# Load tables
billings = spark.table("ds_p.default.billings")
renewal_calls = spark.table("ds_p.default.renewal_calls")

# Extract POST-RENEWAL calls only
post_renewal_calls = billings.join(
    renewal_calls,
    on="Co_Ref",
    how="inner"
).filter(
    renewal_calls.Call_Date > billings.Prospect_Renewal_Date
)

# These are the calls that happened AFTER the renewal deadline
# Use these for post-renewal churn prediction
```

#### 2. Target Variable Definition
```python
# Option 1: Direct target from renewal_calls
target = post_renewal_calls.withColumn(
    "churned",
    when(col("Membership_Renewal_Decision") == "No", 1).otherwise(0)
)

# Option 2: Target from billings.Prospect_Outcome
target = billings.withColumn(
    "churned",
    when(col("Prospect_Outcome") == "Lost", 1)
    .when(col("Prospect_Outcome") == "Won", 0)
    .otherwise(None)
)
```

#### 3. Feature Engineering from Post-Renewal Calls
```python
from pyspark.sql.functions import count, sum as _sum, avg, max as _max

# Aggregate post-renewal call features per customer
post_renewal_features = post_renewal_calls.groupBy("Co_Ref").agg(
    # Call volume
    count("Call_ID").alias("post_renewal_call_count"),
    
    # Churn signals
    _sum(when(col("Explicit_Switching_Intent") == "Yes", 1).otherwise(0)).alias("switching_intent_count"),
    _sum(when(col("Serious_Complaint") == "Yes", 1).otherwise(0)).alias("serious_complaint_count"),
    _sum(when(col("Explicit_Competitor_Mention") == "Yes", 1).otherwise(0)).alias("competitor_mention_count"),
    
    # Price sensitivity
    _sum(when(col("Discount_or_Waiver_Requested") == "Yes", 1).otherwise(0)).alias("discount_request_count"),
    _sum(when(col("Discussion_on_Price_Increase") == "Yes", 1).otherwise(0)).alias("price_increase_discussion_count"),
    
    # Financial hardship
    _sum(when(col("Churn_Category") == "Financial struggles / Business Problems", 1).otherwise(0)).alias("financial_hardship_mentions"),
    
    # Response sentiment
    _sum(when(col("Customer_Renewal_Response_Category").contains("Cancellation"), 1).otherwise(0)).alias("cancellation_response_count"),
    _sum(when(col("Customer_Renewal_Response_Category") == "Agreement", 1).otherwise(0)).alias("agreement_count")
)
```

---

### Critical Churn Features (Post-Renewal)

#### Tier 1: Strongest Predictors (⭐⭐⭐⭐⭐)
1. **Membership_Renewal_Decision** - Direct label
2. **Explicit_Switching_Intent** - Intent to leave
3. **Customer_Renewal_Response_Category** - "Cancellation" response
4. **Churn_Category** - Primary reason
5. **Discussion_on_Price_Increase + Renewal_Impact_Due_to_Price_Increase** - Price reaction
6. **Serious_Complaint** - Major issue
7. **Explicit_Competitor_Mention** - Competitive threat

#### Tier 2: Strong Predictors (⭐⭐⭐⭐)
8. **Customer_Reaction_Category** - Emotional response
9. **Discount_or_Waiver_Requested** - Price sensitivity
10. **Competitor_Benefits_Mentioned** - Value comparison
11. **Implied_Switching_Intent** - Potential switch
12. **Agent_Response_Category** - Recovery effectiveness

#### Tier 3: Moderate Predictors (⭐⭐⭐)
13. **Complaint_Category** - Issue type
14. **Agent_Renewal_Pitch_Category** - Pitch effectiveness
15. **Call_Reschedule_Request** - Avoidance behavior
16. **Other_Complaint** - Additional issues
17. **Topic_Introduced_By** - Initiative

---

## Usage Recommendations

### For EDA (Exploratory Data Analysis)
```python
# Load renewal_calls
renewal_calls = spark.table("ds_p.default.renewal_calls")

# Churn decision distribution
renewal_calls.groupBy("Membership_Renewal_Decision").count().show()

# Top churn reasons
renewal_calls.groupBy("Churn_Category").count().orderBy("count", ascending=False).show()

# Customer response patterns
renewal_calls.groupBy("Customer_Renewal_Response_Category").count().orderBy("count", ascending=False).show()

# Competitive threats
competitive_threats = renewal_calls.filter(
    (renewal_calls.Explicit_Competitor_Mention == "Yes") |
    (renewal_calls.Explicit_Switching_Intent == "Yes")
)
print(f"Competitive threats: {competitive_threats.count()}")

# Price sensitivity
price_sensitive = renewal_calls.filter(
    (renewal_calls.Discount_or_Waiver_Requested == "Yes") |
    (renewal_calls.Churn_Category == "Cost / Price / Too expensive")
)
print(f"Price-sensitive customers: {price_sensitive.count()}")
```

### For Post-Renewal Churn Modeling
```python
# CRITICAL: Extract POST-RENEWAL calls only
billings = spark.table("ds_p.default.billings")
renewal_calls = spark.table("ds_p.default.renewal_calls")

# Join and filter for post-renewal period
post_renewal = billings.join(renewal_calls, on="Co_Ref", how="inner") \
    .filter(renewal_calls.Call_Date > billings.Prospect_Renewal_Date)

# Create target variable
post_renewal = post_renewal.withColumn(
    "churned",
    when(col("Membership_Renewal_Decision") == "No", 1)
    .when(col("Membership_Renewal_Decision") == "Yes", 0)
    .otherwise(None)
)

# Aggregate post-renewal features
from pyspark.sql.functions import count, sum as _sum

customer_features = post_renewal.groupBy("Co_Ref").agg(
    # Target
    _max("churned").alias("churned"),
    
    # Call volume
    count("Call_ID").alias("post_renewal_calls"),
    
    # Churn signals
    _sum(when(col("Explicit_Switching_Intent") == "Yes", 1).otherwise(0)).alias("switching_intent"),
    _sum(when(col("Serious_Complaint") == "Yes", 1).otherwise(0)).alias("serious_complaints"),
    _sum(when(col("Discount_or_Waiver_Requested") == "Yes", 1).otherwise(0)).alias("discount_requests"),
    
    # Churn reasons (one-hot encoding)
    _sum(when(col("Churn_Category") == "Cost / Price / Too expensive", 1).otherwise(0)).alias("churn_price_reason"),
    _sum(when(col("Churn_Category") == "Financial struggles / Business Problems", 1).otherwise(0)).alias("churn_financial_reason"),
    _sum(when(col("Churn_Category") == "Switch / Change / Alternate Provider", 1).otherwise(0)).alias("churn_competitor_reason")
)

# Join back to billings for full feature set
final_dataset = billings.join(customer_features, on="Co_Ref", how="left")
```

---

## Data Quality Notes
* **Missing values in Membership_Renewal_Decision** (53.6%) - requires handling strategy
* **Class imbalance:** More "No" than "Yes" - may need resampling
* **Multiple calls per customer** - requires aggregation for customer-level modeling
* **Call_Date temporal filtering is ESSENTIAL** - must filter for post-renewal period
* **Churn_Category has 18 categories** - may need grouping for modeling

### Recommended Preprocessing
1. **Filter for post-renewal calls** - Call_Date > Prospect_Renewal_Date
2. **Handle missing Membership_Renewal_Decision** - impute or remove
3. **Aggregate to customer level** - one row per customer
4. **One-hot encode categorical features** - Churn_Category, Customer_Renewal_Response_Category
5. **Create composite features** - churn risk score, sentiment score
6. **Balance classes** - SMOTE or class weights

---

## Linking to Other Tables
* **Primary Key:** Call_ID
* **Foreign Key:** Co_Ref (links to billings table)
* **Temporal Join:** Call_Date > billings.Prospect_Renewal_Date (POST-RENEWAL FILTER)
* **Join Strategy:**
  ```python
  # Correct join for post-renewal analysis
  post_renewal = billings.join(
      renewal_calls,
      on="Co_Ref",
      how="inner"
  ).filter(
      renewal_calls.Call_Date > billings.Prospect_Renewal_Date
  )
  ```

---

## Project-Specific Notes

### Post-Renewal Churn Model Requirements
1. **Temporal Filtering:** MUST filter where Call_Date > Prospect_Renewal_Date
2. **Target Variable:** Membership_Renewal_Decision ("No" = churned)
3. **Feature Source:** This table provides post-renewal behavioral features
4. **Integration:** Combine with billings (baseline), emails (communication), cc_calls (support)

### Model Architecture Suggestion
* **Baseline features:** From billings (scores, payment history, tenure)
* **Pre-renewal features:** From emails and cc_calls (sentiment, engagement)
* **Post-renewal features:** From renewal_calls (THIS TABLE, filtered by date)
* **Target:** Churn label from Membership_Renewal_Decision or billings.Prospect_Outcome

---

**Last Updated:** 2026-04-10  
**Contact:** Data Science Team  
**Project:** Post-Renewal Churn Prediction Model  
**⚠️ CRITICAL:** Always filter Call_Date > Prospect_Renewal_Date for post-renewal analysis
