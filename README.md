# CloudFlow SaaS Revenue & Churn Analytics

An end-to-end Data Engineering and Business Intelligence portfolio project focused on analyzing subscription revenue, customer churn, payment performance, and customer support operations for a fictional SaaS company.

## Project Overview

CloudFlow Technologies is a fictional subscription-based software company. This project aims to build a centralized data warehouse that integrates data from multiple business functions and transforms it into reliable, analytics-ready datasets.

The project follows a Medallion Architecture using Microsoft SQL Server, with Power BI serving as the reporting and visualization layer.

## Business Objectives

- Analyze recurring revenue and subscription performance.
- Understand customer churn and retention trends.
- Monitor payment success and collection performance.
- Evaluate customer support operations.
- Compare sales performance against targets.
- Provide consistent metrics for business reporting.

## Architecture

**Planned data flow:**

Synthetic Source Files → Bronze → Silver → Gold → SQL Reporting Views → Power BI

Audit and data-quality checks will support the data processing workflow.

## Technology Stack

| Technology | Purpose |
|---|---|
| Microsoft SQL Server | Data warehouse and SQL transformations |
| SQL | Data ingestion, transformation, validation, and analytics |
| CSV, JSON, Excel | Synthetic source data formats |
| Power BI | Data visualization and dashboards |
| DAX | Business metrics and analytical calculations |
| Git and GitHub | Version control and portfolio publication |
| Notion | Project planning and documentation |

## Planned Data Sources

The project will use synthetic datasets representing:

- Customer master data
- Subscription plans
- Subscription lifecycle events
- Sales transactions
- Payment transactions
- Customer support tickets
- Sales targets

## Planned Warehouse Layers

- **Bronze:** Raw ingested data with ingestion metadata.
- **Silver:** Cleaned, standardized, and validated data.
- **Gold:** Business-ready fact tables, dimension tables, and business rules.

## Planned Analytics

The Power BI reporting layer is planned to include:

- Executive Overview
- Revenue & Subscription Analysis
- Customer Churn Analysis
- Payment Performance
- Customer Support Analysis
- Sales Target Tracking

Additional planned capabilities include DAX measures, data-quality testing, audit logging, historical dimension tracking, and regional Row-Level Security.

## Project Status

**Current phase:** Project Initialization

The initial database, warehouse schemas, and repository structure have been established. Synthetic data generation, warehouse implementation, and reporting development are planned next.

## Repository Structure

```text
data/       - Source files, generated data, and samples
sql/        - Database setup, warehouse layers, views, and tests
scripts/    - Data-generation scripts
powerbi/    - Power BI assets and documentation
docs/       - Technical documentation and diagrams
```

## Disclaimer

CloudFlow Technologies and all datasets used in this project are fictional. The project is intended for educational purposes and portfolio demonstration.

## Author

**Ritesh Herkal**

Data Engineering | SQL Server | Data Warehousing | Power BI
