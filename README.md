# 🌿 WildSync  
## AI-Powered Forest Intelligence & Conservation Platform

WildSync is a **responsible AI-powered forest management platform** that helps forest authorities, NGOs, and researchers **analyze ecosystem data**, detect risks early, and take **data-driven conservation actions**.

The platform unifies ecological datasets, applies AI models for analysis, and visualizes insights through **interactive dashboards and geospatial heatmaps**, enabling faster and more informed conservation decisions.

---

## 🧠 Problem Statement
Forest ecosystems are often monitored using **fragmented, manual, and delayed data collection processes**, leading to:

- Scattered datasets across regions and departments  
- Late identification of high-risk or degraded zones  
- Limited adoption of AI for predictive conservation  
- Poor visualization of large-scale forest health indicators  

**WildSync solves this by combining AI, data analytics, and geospatial visualization into a single unified system.**

---

## 🎯 Hackathon Theme Alignment (Thales GenTech India)

| Theme | Alignment |
|------|----------|
| **AI-Powered Solutions** | Environmental sustainability & biodiversity protection |
| **Cybersecurity & Digital Trust** | Secure handling of sensitive ecological & geospatial data |
| **Scalable Systems** | Cloud-ready architecture with future IoT & drone integration |

---

## ✨ Key Features
- 📊 Unified data upload (CSV / Excel / PDF)
- 🧠 AI-driven risk & scarcity analysis
- 🗺️ Geospatial heatmaps (PostGIS + Leaflet)
- 🚨 Anomaly detection & early alerts
- 🤖 Explainable AI chatbot assistant
- 🔐 Role-based access control (RBAC)
- 📈 Actionable conservation recommendations

---

## 🏗️ System Architecture

### High-Level Overview
WildSync follows a **3-tier architecture** designed for scalability and real-world deployment:

- **Frontend:** User interaction, dashboards, visualization  
- **Backend:** APIs, data processing, AI inference  
- **Database:** Structured ecological + geospatial storage  

---
![WhatsApp Image 2026-01-03 at 3 01 06 PM](https://github.com/user-attachments/assets/2f57d7af-7822-459e-85e2-af2a5f7b629a)

##🧩 Architecture Component Explanation
###Frontend(React)

- Dataset upload & management

- Interactive dashboards & charts

- Geospatial heatmaps using Leaflet

- AI chatbot interface

- Built with React + Tailwind CSS

###Backend

- REST APIs using Flask

- Authentication & RBAC

- Data validation & preprocessing

- AI inference & recommendation logic

- Chatbot orchestration

###Database

- PostgreSQL for structured data

- PostGIS for spatial queries

- JSONB for flexible ecological metadata

##🤖 AI & Machine Learning
###Technology Stack
Layer	Tools
Frontend	React, Tailwind CSS, Leaflet
Backend	Flask, SQLAlchemy, Flask-Login
AI / ML	Python, Pandas, NumPy, Scikit-Learn
NLP	Hugging Face Transformers
Database	PostgreSQL, PostGIS
Deployment	Docker, Nginx, Cloud-ready

##AI Capabilities
1️⃣ Anomaly Detection

Detects unusual patterns such as:

- Sudden drops in tree density

- Soil degradation trends

- Abnormal wildlife population changes

- Used for early alerts and proactive intervention.

2️⃣ Risk & Scarcity Scoring

- Each forest zone receives a risk score derived from:

- Tree density

- Soil health indicators

- Wildlife population data

- Historical calamities (fires, droughts, illegal logging)

These scores power heatmaps and priority zoning.

3️⃣ Recommendation Engine

Combines:

- AI model outputs

- Rule-based expert logic

- Produces human-readable conservation actions, such as:

- Reforestation priority zones

- Increased monitoring areas

- Immediate intervention alerts

##🧪 Model Training Approach
###Training Data

- Forest survey datasets

- Soil quality metrics

- Wildlife population records

- Historical calamity data

- Zone-based geospatial metadata

##Training Pipeline

1. Feature engineering & normalization

- Tabular models (Random Forest / Gradient Boosting)

- Anomaly detection (Isolation Forest)

- Region-wise validation & explainability

- Periodic retraining with new uploads

##🔄 Data Pipeline (End-to-End)
<img width="917" height="263" alt="Screenshot 2026-01-03 150517" src="https://github.com/user-attachments/assets/284db5df-2e08-425e-bf22-909e0f873fb7" />

##📂 Supported Data Inputs

- CSV

- Excel

- PDF

##Typical Fields:

- zone_id

- latitude / longitude

- tree_count

- soil_moisture / pH

- wildlife_count

- calamity_type & severity

- timestamp

##🔐 Security & Responsible AI

- Role-Based Access Control (RBAC)

- Secure dataset storage

- Explainable outputs (why a zone is risky)

- Designed for government-grade deployment

##🚀 Deployment Strategy

- Dockerized frontend & backend

- PostgreSQL + PostGIS (managed DB)

- Cloud-ready (AWS / Azure / GCP)

- CI/CD via GitHub Actions

##🧭 Roadmap (Future Enhancements)

- IoT & drone data ingestion

- Real-time alerts via WebSockets

- Offline-first PWA mode

- Multilingual interface

- Predictive wildfire & drought models

## 🔗 Project Links
- 🏗️ **Technical Architecture & System Diagrams:**  
  [View Architecture Diagrams](./WildSync%20Architecture%20Diagrams.md)

- 🔴 **Live Demo (UI Preview):**  
  https://wildsync.mgx.world  
  *(This link is for demo/UI preview purposes. The full application is not continuously hosted.  
  To experience the complete working system, please run the project locally or using Docker as described below.)*

- 🎥 **Demo Video:** https://youtu.be/6qApxHCXO2Y  
- 🧑‍💻 **GitHub Repository:** https://github.com/2k6ayush/WildSync  

 ##👥 Team

NexTechies
Submission for Thales GenTech India Hackathon 2025
