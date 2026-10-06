# Supply Chain Capital Optimization Pipeline

## Executive Summary
This project is an end-to-end data engineering and analytics pipeline designed to identify and liquidate stagnant working capital within a supply chain network. By processing a 365-day inventory snapshot across 50 SKUs, this analysis uncovered **$476M in trapped dead capital** and provides a tactical liquidation strategy to immediately recover **$190M in liquid cash**.

## Tech Stack
* **Data Processing & Engineering:** Python (Pandas)
* **Exploratory Data Analysis (EDA) & Logic:** SQL (CTEs, Aggregations, Window Functions)
* **Visualization & Reporting:** Power BI, DAX, *Storytelling With Data* (SWD) Design Principles

## Business Problem
Working capital is frequently trapped in stagnant inventory, generating massive holding costs without driving revenue. The objective was to move beyond transactional data to identify structural supply chain bottlenecks and provide procurement teams with a targeted, data-backed liquidation "Hit List."

## Data Architecture & Pipeline
**1. Ingestion & Feature Engineering (Python)**
* Ingested raw dataset via a Python scratchpad notebook to evaluate data quality, nulls, and duplicates.
* Engineered critical business logic columns: `total_holding_cost` (financial risk) and `months_stagnant` (aging threshold).

**2. SQL Exploratory Data Analysis**
* Executed a structured 4-phase SQL pipeline to perform data sanity checks and establish baseline metrics.
* Identified transactional duplication and applied `GROUP BY` logic to accurately aggregate inventory levels and financial exposure by `sku_id` and `warehouse_id`.

**3. Executive Presentation (Power BI)**
* Built a two-page, executive-facing dashboard strictly adhering to *Storytelling With Data* (SWD) principles.
* Stripped out default visual clutter (gridlines, borders, excessive axes) and utilized strategic color contrast to immediately direct stakeholder attention to critical liabilities.

## Strategic Insights & ROI
* **The Imbalance:** The *Furniture* category drives the vast majority of supply chain holding costs despite its sales volume.
* **The Stagnation Point:** The financial risk is highly concentrated in "Dead Stock" (inventory stagnant for 6+ months). 
* **The Tactical Target:** **SKU_43** is the primary network-wide liability, holding nearly $38M in dead capital alone.
* **Business Impact:** Executing a targeted liquidation of 6+ month dead stock at a 40% markdown immediately injects **$190.70M** in liquid cash, clears physical warehouse capacity, and permanently halts ongoing holding cost bleed.

## Dashboards
### 1. The Diagnostic View (The Problem)
*Focuses on macro financial exposure and identifying the root cause of capital drain.*
<img width="1192" height="674" alt="image" src="https://github.com/user-attachments/assets/5fa9b83a-7904-491c-bba0-8533ee6fe63f" />


### 2. The Action & Impact View (The Solution)
*Provides a direct operational hit list and calculates the projected cash recovery ROI.*
<img width="1181" height="669" alt="image" src="https://github.com/user-attachments/assets/7b141a4d-fdc3-4e39-b6d3-d1f3307d988f" />


## Repository Structure
```text
├── data/
│   ├── raw_inventory_data.csv
│   └── processed_inventory_data.csv
├── scripts/
│   ├── 01_data_cleaning.py
│   └── 02_eda_and_aggregation.sql
├── dashboard/
│   ├── supply_chain_dashboard.pbix
│   └── supply_chain_executive_summary.pdf
└── README.md
