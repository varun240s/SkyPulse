# Climate Change Analysis and Dashboard

## Project Overview
This project analyzes climate change trends, including **CO₂ levels, global temperature, deforestation, and sea level rise**, and presents them through an **interactive JavaScript-based dashboard**. The dashboard is deployed using **Docker** on a home server with **Nginx** for hosting and proxy configuration.

---

## **Folder Structure**
```
climate-change-dashboard/
│── data/                # Datasets
│   ├── raw/             # Original datasets (NASA, NOAA, etc.)
│   ├── processed/       # Cleaned, normalized datasets
│   ├── external/        # Additional datasets (IPCC scenarios, maps)
│
│── notebooks/           # Jupyter notebooks for EDA, modeling
│
│── scripts/             # Reusable Python scripts (data processing, analysis)
│
│── models/              # Saved ML models (ARIMA, Prophet, etc.)
│
│── dash_app/            # JavaScript-based dashboard
│   ├── assets/          # CSS, JS, images
│   ├── public/          # Static files, JSON data
│   ├── components/      # Reusable UI components
│   ├── app.js           # Main dashboard entry file
│
│── tests/               # Unit tests (data validation, dashboard functionality)
│
│── logs/                # Debugging logs for data processing, models
│
│── docker/              # Docker configuration
│   ├── Dockerfile       # Docker image setup
│   ├── nginx.conf       # Nginx reverse proxy configuration
│
│── docs/                # Project documentation, reports
│── requirements.txt     # Python dependencies for data processing
│── README.md            # Project overview, setup instructions
│── .gitignore           # Ignore large files (datasets, logs)
```

---

## **Deployment Setup (Using Docker & Nginx)**  
The dashboard is containerized using **Docker** and hosted locally using **Nginx**.

### **1️⃣ Build the Docker Image**
```bash
docker build -t climate_dashboard .
```

### **2️⃣ Run the Container**
```bash
docker run -d -p 80:80 climate_dashboard
```
This runs the dashboard on **port 80**.

---

## **Installation & Running Locally**
1. **Clone the repository**:
   ```bash
   git clone https://github.com/varun240s/climate-change-dashboard.git
   cd climate-change-dashboard
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt  # Install Python dependencies (for data processing)
   ```

3. **Run the dashboard**:
   - Open `dash_app/index.html` in a web browser  
   - Or serve it using a simple HTTP server:
     ```bash
     python -m http.server 8000
     ```
   - Open **http://localhost:8000** in your browser.

---

## **Data Sources**
- **Temperature:** NASA GISTEMP  
- **CO₂ Emissions:** NOAA Annual Greenhouse Gas Index  
- **Deforestation:** Global Forest Watch  
- **Sea Level:** CSIRO & NOAA  

---

## **Best Practices**
✅ **Version Control**:  
- Use `.gitignore` to exclude large files (datasets, logs).  
- Commit frequently with descriptive messages.  

✅ **Modular Code**:  
- Keep scripts reusable (e.g., `process_data.py`, `fetch_data.js`).  
- Organize dashboard components for maintainability.  

✅ **Testing**:  
- Write unit tests for data validation and dashboard performance.  

✅ **Scalability**:  
- Future enhancements could include **cloud deployment** (AWS, GCP, Azure) and **database integration**.  

---

## **Contributors**
- [Alluri Varun Reddy](https://github.com/varun240s)
- [Keerthi Sathvik](https://github.com/Skullkick)  

---
🚀 **This project enables data-driven insights into climate change trends, helping visualize and analyze key environmental metrics.** 🌍  
