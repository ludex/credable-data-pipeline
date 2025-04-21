# 💼 Credable Data Engineering Technical Assessment

This project is a response to Credable's data engineering technical assessment. It involves building an end-to-end pipeline that:

- Ingests data from an SFTP source
- Processes and cleans the data for analytics
- Exposes the results through a structured API (in progress)

Technologies used include `paramiko` for SFTP operations and `pyspark` for distributed data transformation.

---

# 📊 Dataset Summary: Global Financial Inclusion (Global Findex) Data

This project utilizes the **Global Financial Inclusion (Global Findex) Dataset**, compiled by the World Bank and available on Kaggle. The dataset offers comprehensive insights into how adults worldwide manage their finances, including aspects like account ownership, savings, borrowing, and digital payments.

### 🔍 Dataset Description

- **Source**: [Kaggle - Global Financial Inclusion (Global Findex) Data](https://www.kaggle.com/datasets/theworldbank/global-financial-inclusion-global-findex-data)

- **Overview**: The Global Findex database provides over 800 indicators related to financial inclusion, disaggregated by key demographics such as gender, age, education, income, and more. The data is collected through nationally representative surveys conducted in over 140 economies.

- **Key Features**:
  - **Account Ownership**: Data on the percentage of adults with accounts at financial institutions or mobile money services.
  - **Savings and Borrowing**: Information on how individuals save and borrow money.
  - **Digital Payments**: Insights into the usage of digital payment methods.
  - **Risk Management**: Data on how people manage financial risks.

### ✅ Relevance to Credable

Credable focuses on providing embedded digital banking infrastructure, aiming to enhance financial inclusion in emerging markets. This dataset aligns with Credable's mission by:

- **Highlighting Financial Behaviors**: Understanding how different demographics interact with financial services helps in tailoring products that meet specific needs.

- **Identifying Gaps**: The data can reveal areas where financial services are lacking, allowing Credable to target underserved populations effectively.

- **Supporting Data-Driven Decisions**: Leveraging this dataset enables the development of data-driven strategies to improve financial inclusion and product offerings.

---

### 🧪 Project Objectives

This pipeline was designed to fulfill the following:

1. **Data Ingestion via SFTP**
   - Simulated via a Dockerized SFTP server
   - Files uploaded and downloaded using `paramiko`

2. **Data Cleaning and Transformation**
   - PySpark used for scalable data processing
   - Each dataset cleaned with file-specific logic
   - Nulls, unnamed columns, and schema issues handled robustly

3. **Pipeline Modularity**
   - Scripts organized by function: `sftp/`, `processing/`, `api/`
   - Reusable and maintainable folder structure

4. **Future Steps**
   - Implement REST API with FastAPI
   - Add date filtering and cursor-based pagination
   - Enable simple analytics endpoint (e.g., counts per region/income group)

---

### 🚀 How to Use

```bash
# 1. Upload data to simulated SFTP server
python sftp/upload-to-sftp.py

# 2. Download data from SFTP to local dir
python sftp/sftp-downloader.py

# 3. Clean and standardize data using PySpark
python processing/cleaner.py
```

Output files will be stored in the `./processed-data` folder.

---

### 📁 GitHub Usage

Ensure your commits are clear, meaningful, and logical.
Structure your repository as follows:

```
credable-data-pipeline/
├── sftp/
├── processing/
├── api/
├── data/ or sftp-downloads/
├── processed-data/
├── docker-compose.yaml
├── README.md
```

Push your code to a **public GitHub repository**, and share the link as part of your submission.
