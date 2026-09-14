# 🏦 Customer Segmentation & Churn Pattern Analytics in European Banking

## 📌 Project Overview

This project analyzes customer segmentation and churn patterns in a European banking dataset containing 10,000 customer records.

The objective is to identify customer groups associated with higher observed churn, understand how churn varies across demographic and financial segments, and identify high-value customers who represent significant financial exposure.

The project combines exploratory data analysis, customer segmentation, churn analysis, high-value customer analysis, KPI development, and an interactive Streamlit dashboard.

> **Important:** This project focuses on descriptive and diagnostic analytics. The observed relationships do not establish causal relationships or predict future customer churn.

---

## 🎯 Business Problem

Customer churn can reduce customer lifetime value, increase customer acquisition costs, and create revenue instability.

A bank therefore needs to understand:

* Which customer groups show higher observed churn?
* How does churn vary across countries?
* Which age groups are more affected?
* Is churn associated with customer engagement?
* Are high-balance customers disproportionately represented among churners?
* Which combinations of customer characteristics represent the highest observed churn risk?

This project addresses these questions through structured customer segmentation and churn analytics.

---

## 🎯 Project Objectives

### Primary Objectives

1. Measure the overall customer churn rate.
2. Identify churn patterns across customer segments.
3. Compare churn behavior across European countries.
4. Analyze demographic and financial characteristics associated with churn.
5. Identify high-value customers among churners.

### Secondary Objectives

* Analyze customer engagement and tenure patterns.
* Investigate geographic and age interactions.
* Identify combined high-risk customer profiles.
* Quantify financial exposure associated with high-balance churners.
* Provide actionable recommendations for customer-retention strategies.

---

## 📊 Dataset

The dataset contains **10,000 customers** and includes the following information:

| Feature         | Description                 |
| --------------- | --------------------------- |
| CustomerId      | Unique customer identifier  |
| Surname         | Customer surname            |
| CreditScore     | Customer credit score       |
| Geography       | Customer country            |
| Gender          | Customer gender             |
| Age             | Customer age                |
| Tenure          | Years with the bank         |
| Balance         | Customer account balance    |
| NumOfProducts   | Number of banking products  |
| HasCrCard       | Credit card ownership       |
| IsActiveMember  | Customer activity indicator |
| EstimatedSalary | Estimated customer salary   |
| Exited          | Customer churn indicator    |

The target variable is:

* `Exited = 1` → Customer churned
* `Exited = 0` → Customer retained

---

## 🔧 Methodology

The project follows a structured analytics workflow:

```text
Data Ingestion
      ↓
Data Understanding
      ↓
Exploratory Data Analysis
      ↓
Data Cleaning & Preparation
      ↓
Customer Segmentation
      ↓
Churn Analysis
      ↓
High-Value Customer Analysis
      ↓
KPI Development
      ↓
Interactive Dashboard
      ↓
Strategic Recommendations
```

---

## 👥 Customer Segmentation

The project creates derived segmentation variables to support detailed analysis.

### Geography

* France
* Germany
* Spain

### Age Group

* `<30`
* `30-45`
* `46-60`
* `60+`

### Credit Score Band

* Low
* Medium
* High

### Tenure Group

* New
* Mid-term
* Long-term

### Balance Segment

* Zero-balance
* Low-balance
* High-balance

The high-balance segment is used as a proxy for **high-value customers** in this analysis.

### Engagement Status

* Active
* Inactive

---

# 📈 Key Findings

## Overall Churn

* Total customers: **10,000**
* Churned customers: **2,037**
* Retained customers: **7,963**
* Overall churn rate: **20.37%**

---

## 🌍 Geographic Churn

Germany shows the highest observed churn rate:

| Country | Churn Rate |
| ------- | ---------: |
| France  |     16.15% |
| Germany | **32.44%** |
| Spain   |     16.67% |

Germany therefore represents an important geographic segment for further retention investigation.

---

## 👥 Age-Based Churn

The 46–60 age group shows the highest observed churn rate:

| Age Group | Churn Rate |
| --------- | ---------: |
| <30       |      7.56% |
| 30–45     |     15.30% |
| 46–60     | **51.12%** |
| 60+       |     24.78% |

The 46–60 segment should therefore receive particular attention in retention analysis.

---

## 🔥 Customer Engagement

Customer engagement shows one of the strongest observed differences in churn:

| Engagement | Churn Rate |
| ---------- | ---------: |
| Active     |     14.27% |
| Inactive   | **26.85%** |

Inactive customers account for approximately **63.92% of all churners**.

This suggests that customer re-engagement should be an important retention priority.

---

## 💰 High-Value Customer Analysis

High-balance customers are treated as high-value customers for this project.

Key results:

* High-value customers: **5,000**
* High-value churners: **1,249**
* High-value churn rate: **24.98%**
* High-value churn contribution: **61.32% of all churners**
* High-value churn financial exposure: approximately **€163.24 million**

The exposure figure represents the combined balance associated with high-balance customers who churned.

> It should not be interpreted as actual revenue loss because the dataset does not contain customer revenue or profit information.

---

## ⚠️ Highest-Risk Combined Profile

The strongest observed combined segment identified in the analysis consists of customers who are:

* Located in **Germany**
* Aged **46–60**
* **Inactive**
* **High-balance**

This segment contains:

* Customers: **237**
* Churners: **195**
* Observed churn rate: **82.28%**

Because this is an observational analysis, the result should be interpreted as a high-risk pattern rather than evidence that these characteristics cause churn.

---

# 📊 Dashboard

The project includes an interactive **Streamlit dashboard**.

### Dashboard Features

* Executive KPI overview
* Geographic churn analysis
* Age-group analysis
* Engagement analysis
* High-value customer analysis
* Geography × Age analysis
* Balance segment analysis
* Product-level churn analysis
* Customer Risk Explorer
* Dynamic filtering
* Customer-level drill-down
* CSV download of selected customer segments
* Strategic insights and recommendations

### Risk Explorer

Users can filter customers by:

* Geography
* Age Group
* Engagement Status
* Balance Segment

The dashboard dynamically calculates:

* Customer count
* Churner count
* Churn rate
* Churned balance exposure

---

# 🗂️ Project Structure

```text
European_Bank_Customer_Churn/
│
├── data/
│   ├── European_Bank.csv
│   └── European_Bank_Processed.csv
│
├── notebooks/
│   ├── 01_Data_Understanding.ipynb
│   ├── 02_EDA.ipynb
│   ├── 03_Data_Preprocessing.ipynb
│   ├── 04_Customer_Segmentation.ipynb
│   ├── 05_Churn_Analysis.ipynb
│   ├── 06_High_Value_Customer_Analysis.ipynb
│   └── 07_Final_Insights.ipynb
│
├── dashboard/
│   └── app.py
│
├── outputs/
│   ├── figures/
│   └── tables/
│
├── reports/
│   ├── research_paper/
│   └── executive_summary/
│
├── README.md
└── requirements.txt
```

---

# 🛠️ Technologies Used

* Python
* Pandas
* NumPy
* Matplotlib
* Streamlit
* Jupyter Notebook
* CSV
* Git/GitHub compatible project structure

---

# ▶️ How to Run the Project

## 1. Open the project directory

```powershell
cd "F:\projects\internship_projects\Customer Segmentation & Churn Pattern Analytics in European Banking"
```

## 2. Activate the virtual environment

If the project contains a virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

## 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

## 4. Launch the dashboard

```powershell
streamlit run dashboard\app.py
```

Streamlit will provide a local URL where the dashboard can be viewed.

---

# 📁 Outputs

The project generates analytical tables and visualizations in:

```text
outputs/
├── figures/
└── tables/
```

These outputs support the research paper, executive summary, and dashboard.

---

# ⚠️ Project Limitations

1. The analysis is based on observational customer data.
2. Observed relationships do not establish causality.
3. The dataset does not contain actual customer revenue or profit.
4. Balance exposure should therefore not be interpreted as revenue loss.
5. Some customer segments, particularly customers with 3 or 4 products, are relatively small and should be interpreted carefully.
6. The project focuses on descriptive and diagnostic analytics rather than predictive churn modeling.
7. External factors such as customer service quality, pricing, competitor activity, economic conditions, and individual customer interactions are not included in the dataset.

---

# 🚀 Future Improvements

Potential extensions include:

* Develop a predictive churn model.
* Apply feature importance and explainable AI techniques.
* Introduce customer lifetime value analysis.
* Add time-based churn monitoring.
* Incorporate transaction and product-usage data.
* Add automated retention recommendations.
* Deploy the Streamlit dashboard online.
* Integrate real-time banking data where appropriate.

---

# 🏁 Conclusion

This project demonstrates how customer segmentation and exploratory churn analytics can be used to identify important patterns within a banking customer base.

The analysis highlights Germany, customers aged 46–60, inactive customers, and high-balance customers as important areas for retention investigation.

The interactive dashboard transforms the analytical findings into a practical decision-support tool by allowing stakeholders to explore customer segments, evaluate observed churn rates, investigate high-risk profiles, and download filtered customer data.

Overall, the project provides a structured foundation for understanding customer churn patterns and developing targeted customer-retention strategies.
