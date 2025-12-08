# 📈 Tech Talent Pulse
### *Automated ETL Pipeline for Tracking Tech Job Market Trends*

## 📊 Overview
The tech job market moves fast. **Tech Talent Pulse** is a fully automated data pipeline that tracks which programming skills are in highest demand. 

Instead of relying on static reports, this system **scrapes** live job postings daily, **extracts** key technologies (e.g., Python, AWS, Kubernetes) using NLP techniques, and **visualizes** the rising trends on an interactive dashboard.

---

## 🏗️ Architecture
This project runs entirely on a **Serverless Architecture** using GitHub Actions.

```mermaid
graph LR
    A[WeWorkRemotely RSS] -->|Daily Scrape| B(GitHub Actions Runner)
    B -->|Extract Description| C{Data Processor}
    C -->|Regex & NLP| D[Structured Data CSV]
    D -->|Commit & Push| E[(GitHub Repo)]
    E -->|Read Data| F[Streamlit Dashboard]