USE master;
GO

/*
================================================================================
Project         : CloudFlow SaaS Revenue & Churn Analytics
Script          : 01_Create_Database_CloudFlowDW.sql
Database        : CloudFlowDW
Architecture    : Medallion Data Warehouse
Developer       : Ritesh Herkal
Created On      : 13-Oct-2026

Purpose:
    Creates the CloudFlowDW database if it does not already exist.

Execution:
    Run this script using a SQL Server login with permission to create databases.

Safety:
    This script does not drop, recreate, or overwrite an existing database.
    Database-level configuration can be managed separately if required.
================================================================================
*/

SET NOCOUNT ON;
GO

/*==============================================================================
  1. Validate database existence
==============================================================================*/

IF DB_ID(N'CloudFlowDW') IS NULL
	BEGIN
		PRINT 'Creating database CloudFlowDW...';

		CREATE DATABASE [CloudFlowDW];

		PRINT 'Database CloudFlowDW created successfully.';
	END

ELSE
	BEGIN
		PRINT 'Database CloudFlowDW already exists. No changes made.';
	END;
GO

/*==============================================================================
  2. Verify database creation
==============================================================================*/

SELECT
    name AS DatabaseName,
    state_desc AS DatabaseState,
    create_date AS CreatedDate
FROM sys.databases
WHERE name = N'CloudFlowDW';
GO
