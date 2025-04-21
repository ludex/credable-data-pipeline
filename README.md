# 💼 Credable Data Engineering Technical Assessment

This project is a response to Credable's data engineering technical assessment. It involves building an end-to-end pipeline that:

- Ingests data from an SFTP source
- Processes and cleans the data for analytics
- Exposes the results through a structured, rate-limited REST API

Technologies used include `paramiko` for SFTP operations, `pyspark` for distributed data transformation, and `FastAPI` for the backend API. Rate limiting is implemented using `slowapi` backed by Redis.

---

### 📊 Dataset Summary: Global Financial Inclusion (Global Findex) Data

This project utilizes the **Global Financial Inclusion (Global Findex) Dataset**, compiled by the World Bank and available on Kaggle. The dataset offers comprehensive insights into how adults worldwide manage their finances.

🔗 [Kaggle - Global Financial Inclusion (Global Findex) Data](https://www.kaggle.com/datasets/theworldbank/global-financial-inclusion-global-findex-data)

---

### ✅ Relevance to Credable

Credable focuses on embedded digital banking infrastructure in emerging markets. This dataset supports Credable’s mission by highlighting financial behaviors, identifying inclusion gaps, and guiding data-driven strategy development.

---

## 🧪 Project Objectives

This pipeline was designed to fulfill the following:

1. **Data Ingestion via SFTP**
   - Simulated with Docker
   - Automated upload/download using `paramiko`

2. **Data Cleaning with PySpark**
   - File-specific schema validation
   - Null handling, standardization, and normalization

3. **API Implementation with FastAPI**
   - Dataset browsing (`/data/datasets`)
   - Data retrieval with date filtering and pagination (`/data`)
   - Analytics summary per dataset (`/data/analytics`)
   - Rate limiting: 100 requests/minute using Redis (`slowapi`)

4. **Production Readiness**
   - Dockerized deployment
   - Redis-based persistence
   - Gunicorn + Uvicorn app server

---

## 🔧 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/ludex/credable-data-pipeline.git
cd credable-data-pipeline
```

### 2. Create a Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Prepare the Environment

Make sure Docker is installed. Then run:

```bash
docker compose up --build
```

This will:
- Start Redis for rate limiting
- Build and run the API using Gunicorn

### 4. Upload and Clean the Data

```bash
python sftp/upload-to-sftp.py
python sftp/sftp-downloader.py
python processing/cleaner.py
```

### 5. Access the API

Visit the Swagger docs at:
```
http://localhost:8000/docs
```

Use:
```
Authorization: Bearer secret123
```

### 6. Sample Endpoints

- `GET /data?dataset=FINDEXData&start_date=2014&limit=5`
- `GET /data/analytics?dataset=FINDEXData`
- `GET /data/datasets`

---

### 📁 GitHub Usage

Keep commits clear and logical. Repo structure:

```
credable-data-pipeline/
├── sftp/
├── processing/
├── api/
├── data/                  
├── processed-data/       
├── docker-compose.yaml
├── Dockerfile
├── requirements.txt
├── README.md
```

---
