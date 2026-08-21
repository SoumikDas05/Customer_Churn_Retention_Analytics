# Customer_Churn_Retention_Analytics

# <h2> Problem Statement

<p> Customer churn directly impacts recurring revenue and long-term business growth. Understanding which customers are leaving, where churn is concentrated, and which factors are associated with churn can help businesses improve customer retention and reduce revenue loss.
  
This project analyzes customer, subscription, and support data to identify churn patterns and generate actionable insights. The analysis focuses on customer churn and retention rates, plan- and location-based churn behavior, customer tenure, revenue at risk, complaints, escalations, and churn-risk segmentation. <p>

<h2>Objective</h2>

<p>The objective of this project is to analyze customer churn and retention by combining customer, subscription, and support data. The analysis aims to understand overall churn and retention rates, identify which subscription plans and locations experience higher churn, and measure important business metrics such as average customer tenure, average revenue, revenue at risk, escalation rate, and customer complaints. The project also explores the relationship between customer behavior and churn using correlation analysis and classifies customers into Low, Medium, and High churn-risk groups based on their churn scores. Finally, the findings are presented through visualizations such as monthly churn trends, plan-wise and state-wise churn analysis, correlation heatmaps, and other charts to provide clear insights that can support better customer retention decisions.</p>

<h2>Churn Analysis Steps</h2>
<p>
•	Connect SQL database to Python – pandas and sqlite3
  
•	Data import using SQL query in Python – pandas and sqlite3

•	Data Cleaning – numpy and pandas

•	data types, rename cols, select specific cols, QCs, handle missing/null values  

•	Feature Engineering – numpy and pandas 

•	Create new calculated cols, data transformation, use filters  

•	Data Analysis – numpy and pandas 

•	EDA - aggregation, group by, pivot table  

•	Data Visualization – matplotlib and seaborn

</p>

<h2>Churn Definition</h2>
<p>
  Customer churn occurs when a customer stops using a company's service or ends their subscription. In this project, a customer is considered churned when a cancellation date is recorded in the subscription data. Customers without a cancellation date are considered active.

The analysis focuses on three main questions: Who is churning by examining customer segments such as plan type, contract type, location, and churn risk; Why customers may be churning by analyzing factors such as churn score, complaints, escalations, and subscription characteristics; and When customers churn by analyzing cancellation dates, monthly churn trends, and customer tenure.

Business Type	                          Churn Definition

Subscription Service	         Customer has a recorded cancellation date

Churned Customer	             cancellation_date is available → churn_flag = 1

Active Customer	               cancellation_date is missing → churn_flag = 0

</p>

