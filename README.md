## Customer Churn Analytics (ETL + Dashboard)
This project demonstrates a complete ETL pipeline and analytics dashboard for telecom Call Detail Records (CDR).
The goal is to analyze customer churn behavior by transforming raw CSV data into a Postgres data warehouse (star schema) and building interactive dashboards in Metabase.

### Tech Stack

Python (Pandas, SQLAlchemy) → Data extraction & transformation
Postgres (Docker) → Data warehouse with star schema
Metabase → Business Intelligence dashboards
Docker Compose → Containerized setup

### Pipeline Flow
Extract → Raw CSV (CDR-Call-Details.csv)
Transform → Dimensions & Facts created (dim_customer, dim_time, fact_usage)
Load → Star schema loaded into Postgres
Visualize → Metabase dashboards for churn analysis

### Data Warehouse Schema

#### Dimensions
dim_customer → customer_id, phone_number, account_length, vmail_message
dim_time → snapshot_date, year, month, day, weekday

#### Facts
fact_usage → customer_id, time_id, day/eve/night/intl usage, charges, customer service calls, churn_flag

### Dashboards

Here are some of the dashboards built in Metabase:

Churn Overview → Churn rate % and total churners vs non-churners
Usage Behavior by Churn → Avg day/eve/night/intl mins grouped by churn_flag
Customer Service Calls → Avg calls for churners vs non-churners
High-Value Customers → Top 10 customers by charges
Trend Monitoring → Usage over time (if multiple snapshots available)


(images/dashboard.png)
(images/docker.png)

### Insights
Customers who churned made ~20% more service calls than loyal customers.
Churners had lower night-time usage compared to non-churners.
International usage showed no strong correlation with churn.

### Future Work
Add Airflow for ETL scheduling
Add ML churn prediction model
Deploy dashboards for stakeholders
