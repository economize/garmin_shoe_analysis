# Garmin Data Analysis & AI Coach

A local-first data pipeline that ingests your Garmin Connect history, calculates physiological metrics (ACWR, TRIMP), and uses a local AI model (DeepSeek via Ollama) to provide personalized training advice without sending your health data to the cloud.

## 🚀 Features

* **Data Ingestion:** Securely fetches activity data using the `garminconnect` API.
* **Physiological Analysis:** Calculates Acute Chronic Workload Ratio (ACWR) and TRIMP scores to detect overtraining risks.
* **AI Coach:** Uses a local LLM (DeepSeek-R1) to analyze your metrics and chat with you about your training status.
* **Privacy First:** All health data and AI processing stay on your local machine.

## 🛠️ Prerequisites

1.  **Python 3.10+**
2.  **Ollama** installed and running ([Download Ollama](https://ollama.com/)).
3.  **DeepSeek Model:** Pull the model you intend to use:
    ```bash
    ollama pull deepseek-r1:14b
    ```

## 📦 Installation

1.  Clone the repository:
    ```bash
    git clone [https://github.com/economize/garmin_shoe_analysis.git](https://github.com/economize/garmin_shoe_analysis.git)
    cd garmin_shoe_analysis
    ```

2.  Install Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## 🏃 Usage

Run the pipeline in sequence:

```bash
# 1. Fetch latest data from Garmin
python src/ingestion.py

# 2. Calculate metrics (ACWR/TRIMP)
python src/physio.py

# 3. Chat with your AI Coach
python src/coach.py

### The "Green Light" System
The analysis script calculates your **Acute:Chronic Workload Ratio (ACWR)**:
* **< 0.80:** Undertraining (Risk of detraining)
* **0.80 - 1.30:** 🟢 **Sweet Spot** (Optimal training load)
* **> 1.50:** 🔴 **Danger Zone** (High injury risk)

## ⚠️ Disclaimer
This tool is for informational purposes only. The "Coach" is an AI model and can hallucinate. Always consult a real medical professional or physical therapist for injury advice.
---

### 3. Terminal Commands (PowerShell)
Once you have saved those two files, run these commands to push the changes to GitHub:

```powershell
# 1. Add the new files
git add requirements.txt README.md

# 2. Commit
git commit -m "Update docs: Add requirements and Coach documentation"

# 3. Push to GitHub
git push origin main