-- Table Creation and Data Loading Queries

-- 1. Create Database
CREATE DATABASE Loan_Db;

-- 2. Connect to Database
--\c loan_default_db;
-- 3. Create Loan Data Table
DROP TABLE loan_data; 
CREATE TABLE IF NOT EXISTS loan_data (
    credit_policy       INTEGER,
    purpose             VARCHAR(50),
    int_rate            DECIMAL(6,4),
    installment         DECIMAL(10,2),
    log_annual_inc      DECIMAL(10,4),
    dti                 DECIMAL(10,2),
    fico                INTEGER,
    days_with_cr_line   DECIMAL(12,2),
    revol_bal           BIGINT,
    revol_util          DECIMAL(10,2),
    inq_last_6mths      INTEGER,
    delinq_2yrs         INTEGER,
    pub_rec             INTEGER,
    not_fully_paid      INTEGER
);
--/d loan_data;
-- 4. Load CSV Data(USING COPY COMMAND)
COPY loan_data(
    credit_policy,
    purpose,
    int_rate,
    installment,
    log_annual_inc,
    dti,
    fico,
    days_with_cr_line,
    revol_bal,
    revol_util,
    inq_last_6mths,
    delinq_2yrs,
    pub_rec,
    not_fully_paid
)
FROM 'E:\INFYNTREK_DA\Loan Default Risk Prediction\data\loan_data.csv'
DELIMITER ','
CSV HEADER;

SELECT * FROM loan_data;

-- Check Missing Values
SELECT
    COUNT(*) - COUNT(purpose) AS missing_purpose,
    COUNT(*) - COUNT(int_rate) AS missing_int_rate,
    COUNT(*) - COUNT(fico) AS missing_fico,
    COUNT(*) - COUNT(dti) AS missing_dti,
    COUNT(*) - COUNT(revol_util) AS missing_revol_util
FROM loan_data;

-- Check Duplicate Rows
SELECT *,
       COUNT(*)
FROM loan_data
GROUP BY
    credit_policy,
    purpose,
    int_rate,
    installment,
    log_annual_inc,
    dti,
    fico,
    days_with_cr_line,
    revol_bal,
    revol_util,
    inq_last_6mths,
    delinq_2yrs,
    pub_rec,
    not_fully_paid
HAVING COUNT(*) > 1;

-- Remove Duplicate Rows
DELETE FROM loan_data a
USING loan_data b
WHERE a.ctid < b.ctid
AND a.credit_policy = b.credit_policy
AND a.purpose = b.purpose
AND a.int_rate = b.int_rate
AND a.installment = b.installment
AND a.log_annual_inc = b.log_annual_inc
AND a.dti = b.dti
AND a.fico = b.fico
AND a.days_with_cr_line = b.days_with_cr_line
AND a.revol_bal = b.revol_bal
AND a.revol_util = b.revol_util
AND a.inq_last_6mths = b.inq_last_6mths
AND a.delinq_2yrs = b.delinq_2yrs
AND a.pub_rec = b.pub_rec
AND a.not_fully_paid = b.not_fully_paid;

-- One-Hot Encoding
-- Create Processed ML Table
CREATE TABLE processed_loan_data AS

SELECT

    credit_policy,
    int_rate,
    installment,
    log_annual_inc,
    dti,
    fico,
    days_with_cr_line,
    revol_bal,
    revol_util,
    inq_last_6mths,
    delinq_2yrs,
    pub_rec,
    not_fully_paid,

    CASE
        WHEN purpose = 'all_other'
        THEN 1 ELSE 0
    END AS purpose_all_other,

    CASE
        WHEN purpose = 'debt_consolidation'
        THEN 1 ELSE 0
    END AS purpose_debt_consolidation,

    CASE
        WHEN purpose = 'educational'
        THEN 1 ELSE 0
    END AS purpose_educational,

    CASE
        WHEN purpose = 'credit_card'
        THEN 1 ELSE 0
    END AS purpose_credit_card,

    CASE
        WHEN purpose = 'major_purchase'
        THEN 1 ELSE 0
    END AS purpose_major_purchase,

    CASE
        WHEN purpose = 'home_improvement'
        THEN 1 ELSE 0
    END AS purpose_home_improvement,

    CASE
        WHEN purpose = 'small_business'
        THEN 1 ELSE 0
    END AS purpose_small_business

FROM loan_data;

SELECT *
FROM processed_loan_data
LIMIT 10;

-- Detect Outliers in Revolving Balance
WITH stats AS (

    SELECT

        PERCENTILE_CONT(0.25)
        WITHIN GROUP (ORDER BY revol_bal) AS q1,

        PERCENTILE_CONT(0.75)
        WITHIN GROUP (ORDER BY revol_bal) AS q3

    FROM loan_data
)

SELECT *

FROM loan_data, stats

WHERE revol_bal <
      (q1 - 1.5 * (q3 - q1))

   OR revol_bal >
      (q3 + 1.5 * (q3 - q1));

-- Count Total Outliers
WITH stats AS (

    SELECT

        PERCENTILE_CONT(0.25)
        WITHIN GROUP (ORDER BY revol_bal) AS q1,

        PERCENTILE_CONT(0.75)
        WITHIN GROUP (ORDER BY revol_bal) AS q3

    FROM loan_data
)

SELECT COUNT(*) AS total_outliers

FROM loan_data, stats

WHERE revol_bal <
      (q1 - 1.5 * (q3 - q1))

   OR revol_bal >
      (q3 + 1.5 * (q3 - q1));

-- Detect Outliers in DTI
WITH stats AS (

    SELECT

        PERCENTILE_CONT(0.25)
        WITHIN GROUP (ORDER BY dti) AS q1,

        PERCENTILE_CONT(0.75)
        WITHIN GROUP (ORDER BY dti) AS q3

    FROM loan_data
)

SELECT *

FROM loan_data, stats

WHERE dti <
      (q1 - 1.5 * (q3 - q1))

   OR dti >
      (q3 + 1.5 * (q3 - q1));

-- Cap Revolving Balance at 99th Percentile (Winsorization)
UPDATE loan_data

SET revol_bal = (

    SELECT
    PERCENTILE_CONT(0.99)
    WITHIN GROUP (ORDER BY revol_bal)

    FROM loan_data
)

WHERE revol_bal >

(
    SELECT
    PERCENTILE_CONT(0.99)
    WITHIN GROUP (ORDER BY revol_bal)

    FROM loan_data
);


-- =======Statistical Summary========
-- Statistical Summary
SELECT

    AVG(fico) AS avg_fico,
    MIN(fico) AS min_fico,
    MAX(fico) AS max_fico,
    STDDEV(fico) AS std_fico,

    AVG(dti) AS avg_dti,
    MIN(dti) AS min_dti,
    MAX(dti) AS max_dti,
    STDDEV(dti) AS std_dti,

    AVG(revol_util) AS avg_revol_util,
    MIN(revol_util) AS min_revol_util,
    MAX(revol_util) AS max_revol_util,
    STDDEV(revol_util) AS std_revol_util

FROM loan_data;

-- Export Clean Dataset to Python

COPY processed_loan_data
TO 'E:/INFYNTREK_DA/Loan Default Risk Prediction/data/processed_loan_data.csv'
DELIMITER ','
CSV HEADER;



-- Average Interest Rate
SELECT AVG(int_rate) AS avg_interest_rate
FROM loan_data;

-- Default Distribution
SELECT 
    not_fully_paid,
    COUNT(*) AS total_loans,
    ROUND(
        COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (),
        2
    ) AS percentage
FROM loan_data
GROUP BY not_fully_paid;

-- Loan Purpose Distribution
SELECT 
    purpose,
    COUNT(*) AS total_loans
FROM loan_data
GROUP BY purpose
ORDER BY total_loans DESC;

-- High Risk Borrower Query
SELECT *
FROM loan_data
WHERE dti > 20
AND fico < 680
AND revol_util > 70;