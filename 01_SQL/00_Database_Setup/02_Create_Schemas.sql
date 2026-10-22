USE [CloudFlowDW];
GO

/*
================================================================================
Project         : CloudFlow SaaS Revenue & Churn Analytics
Script          : 02_Create_Schemas.sql
Database        : CloudFlowDW
Developer       : Ritesh Herkal
Created On      : 13-Oct-2026

Purpose:
    Creates the schemas required for the data warehouse architecture.

Schemas:
    Bronze  - Raw source data and ingestion metadata.
    Silver  - Cleaned, standardized, and validated data.
    Gold    - Business-ready dimensions, facts, and reporting objects.
    Audit   - Pipeline execution logs and data-quality audit records.

Safety:
    Creates only schemas that do not already exist.
    Does not drop or modify existing schemas or objects.
================================================================================
*/

SET NOCOUNT ON;
GO

/*==============================================================================
  1. Validate database context
==============================================================================*/

IF DB_NAME() <> N'CloudFlowDW'
BEGIN
    THROW 50001,
          'Incorrect database context. Execute this script in CloudFlowDW.',
          1;
END;
GO

/*==============================================================================
  2. Create Bronze schema
==============================================================================*/

IF SCHEMA_ID(N'Bronze') IS NULL
	BEGIN
		EXEC(N'CREATE SCHEMA [Bronze] AUTHORIZATION [dbo];');
		PRINT 'Schema Bronze created.';
	END

ELSE
	BEGIN
		PRINT 'Schema Bronze already exists. No changes made.';
	END;
GO

/*==============================================================================
  3. Create Silver schema
==============================================================================*/

IF SCHEMA_ID(N'Silver') IS NULL
	BEGIN
		EXEC(N'CREATE SCHEMA [Silver] AUTHORIZATION [dbo];');
		PRINT 'Schema Silver created.';
	END

ELSE
	BEGIN
		PRINT 'Schema Silver already exists. No changes made.';
	END;
GO

/*==============================================================================
  4. Create Gold schema
==============================================================================*/

IF SCHEMA_ID(N'Gold') IS NULL
	BEGIN
		EXEC(N'CREATE SCHEMA [Gold] AUTHORIZATION [dbo];');
		PRINT 'Schema Gold created.';
	END

ELSE
	BEGIN
		PRINT 'Schema Gold already exists. No changes made.';
	END;
GO

/*==============================================================================
  5. Create Audit schema
==============================================================================*/

IF SCHEMA_ID(N'Audit') IS NULL
	BEGIN
		EXEC(N'CREATE SCHEMA [Audit] AUTHORIZATION [dbo];');
		PRINT 'Schema Audit created.';
	END

ELSE
	BEGIN
		PRINT 'Schema Audit already exists. No changes made.';
	END;
GO

/*==============================================================================
  6. Verify schema creation
==============================================================================*/

SELECT
    s.name AS SchemaName,
    USER_NAME(s.principal_id) AS SchemaOwner
FROM sys.schemas AS s
WHERE s.name IN (N'Bronze', N'Silver', N'Gold', N'Audit')
ORDER BY
    CASE s.name
        WHEN N'Bronze' THEN 1
        WHEN N'Silver' THEN 2
        WHEN N'Gold'   THEN 3
        WHEN N'Audit'  THEN 4
    END;
GO
