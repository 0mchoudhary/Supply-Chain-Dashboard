-- Snowflake Security & Governance Configuration

-- 1. Role-Based Access Control (RBAC)
USE ROLE SECURITYADMIN;

-- Create Roles
CREATE ROLE supply_chain_analyst;
CREATE ROLE supply_chain_admin;
CREATE ROLE data_engineer;

-- Grant Privileges
GRANT USAGE ON DATABASE supply_chain_db TO ROLE supply_chain_analyst;
GRANT USAGE ON SCHEMA supply_chain_db.public TO ROLE supply_chain_analyst;
GRANT SELECT ON ALL TABLES IN SCHEMA supply_chain_db.public TO ROLE supply_chain_analyst;

GRANT ALL PRIVILEGES ON DATABASE supply_chain_db TO ROLE supply_chain_admin;

-- 2. Data Masking (Snowflake Dynamic Data Masking)
USE ROLE ACCOUNTADMIN;

-- Create a masking policy for sensitive supplier information (e.g., email/phone)
CREATE OR REPLACE MASKING POLICY contact_info_mask AS (val string) 
  RETURNS string ->
  CASE
    WHEN CURRENT_ROLE() IN ('SUPPLY_CHAIN_ADMIN', 'DATA_ENGINEER') THEN val
    ELSE '***MASKED***'
  END;

-- Apply policy to columns
ALTER TABLE Dim_Suppliers MODIFY COLUMN email SET MASKING POLICY contact_info_mask;
ALTER TABLE Dim_Suppliers MODIFY COLUMN phone SET MASKING POLICY contact_info_mask;

-- 3. Row-Level Security (RLS) example
-- Policy to restrict Analysts to see only shipments from their specific country
CREATE OR REPLACE ROW ACCESS POLICY shipment_country_policy
  AS (country STRING) RETURNS BOOLEAN ->
  UPPER(CURRENT_ROLE()) = 'SUPPLY_CHAIN_ADMIN'
  OR (UPPER(CURRENT_ROLE()) = 'SUPPLY_CHAIN_ANALYST' AND country = 'USA'); -- Simplified example

ALTER TABLE Dim_Warehouses ADD ROW ACCESS POLICY shipment_country_policy ON (country);

-- 4. Governance: Tagging for PII
CREATE TAG pii_data COMMENT = 'Sensitive Personal Identifiable Information';
ALTER TABLE Dim_Suppliers MODIFY COLUMN contact_person SET TAG pii_data = 'Level1';
