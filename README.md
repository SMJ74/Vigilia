Markdown# 🛡️ Vigilia - AML Transaction Monitoring Dashboard

**Vigilia** is a rule-based Anti-Money Laundering (AML) transaction monitoring tool. It helps detect suspicious financial activity such as large transfers, structuring, high-risk country transactions, and rapid movements.

This project demonstrates practical skills in financial compliance, data analysis, rule engines, and building interactive dashboards — excellent for a portfolio in fintech, compliance, or data engineering roles.

---

## ✨ Features

- **Synthetic Transaction Generator** — Creates realistic banking data
- **Custom AML Rules Engine** — Modular and easy to extend
- **Interactive Web Dashboard** — Built with Streamlit
- **Risk Scoring System** — Each transaction gets a risk score and explanation
- **Visualizations** — Charts showing risk distribution, country breakdown, and flagged vs normal transactions
- **Filters & File Upload** — Filter by country/risk level and upload your own CSV
- **Export Functionality** — Download flagged transactions

---

## 🚀 How to Run

### 1. Clone the Repository
```bash
git clone https://github.com/SMJ74/vigilia.git
cd vigilia
2. Create and Activate Virtual Environment
PowerShellpython -m venv venv
.\venv\Scripts\Activate
3. Install Dependencies
PowerShellpip install -r requirements.txt
4. Run the Dashboard
PowerShellstreamlit run app.py
Alternative: Console Version
PowerShellpython main.py

📁 Project Structure
textVigilia/
├── main.py                 # Console version
├── app.py                  # Streamlit web dashboard
├── src/
│   ├── rules.py            # AML Rules Engine + rules
│   └── utils.py            # Synthetic data generator
├── data/
│   └── sample_transactions.csv
├── requirements.txt
└── README.md

🛠️ Tech Stack

Python 3.12+
Streamlit — Web dashboard
Pandas — Data processing
Plotly — Interactive charts
Faker — Synthetic data generation


🔧 Key Components

Rules Engine: Easy to add new AML rules with weighted scoring
Current Rules:
Large Amount (> $10,000)
Structuring (just under reporting threshold)
High-Risk Countries
Rapid Movement (large withdrawals)



Future Enhancements (Planned)

Machine Learning anomaly detection
Graph visualization of money flows
User authentication
Database integration
Real-time monitoring simulation


📄 License
This project is for learning and portfolio purposes.

Made with ❤️ for learning financial compliance and software engineering
