# 🏃‍♂️ Garmin Shoe Performance Audit: Causal Inference in Personal Athletics

> **Project Status:** Complete (Transitioning to ML/Predictive Modeling)
> **Methodology:** OLS Regression & PCA (Econometrics)

## 🎯 Objective
To determine the "true" performance impact of my running shoe rotation by controlling for physiological and environmental confounders. This project moves beyond simple "Average Pace" comparisons (which suffer from selection bias) to isolate the mechanical efficiency of specific footwear.

## 🧐 The Problem: "The Strava Bias"
Most running apps simply average your pace per shoe. This is flawed because:
1.  **Selection Bias:** Faster shoes are chosen for race days; slower shoes for recovery.
2.  **Terrain Bias:** Stable shoes are often worn on hilly or uneven routes.
3.  **Fatigue:** A "slow" shoe might just be a victim of tired legs (high acute load).

## 🧪 Methodology: Dual-Model OLS
To isolate the shoe's effect, I built a rigorous feature set controlling for fitness, fatigue, and elevation. I then ran two competing regression models:

### 1. Feature Engineering
* **Aerobic Power Factor (PCA):** Combined `Efficiency` (Watts/HR) and `VO2 Max` into a single component to eliminate multicollinearity.
* **Training Stress Balance (TSB):** Split mileage into `fitness_42_day_km` (Chronic Load) and `fatigue_7_day_km` (Acute Load) with a `shift(1)` to prevent data leakage.
* **Relative Climb:** Normalized elevation gain (`gain / distance`) to fairly compare hilly vs. flat runs.

### 2. The Models
* **Model A (Mechanical Gain):** Controls for **Stride Length & Cadence**.
    * *Question:* "If I run with the exact same mechanics, does the shoe make me faster?"
* **Model B (Net Performance):** Removes biomechanical controls.
    * *Question:* "Does the shoe encourage a gait change (e.g., faster turnover) that leads to speed?"

## 📊 Key Findings (The "Stability is Speed" Verdict)

The analysis yielded a statistically significant conclusion that contradicted marketing claims but aligned with my specific biomechanics (Midfoot Striker / Stability Needs).

### 🏆 The Winner: Saucony Tempus
* **Model A (Mechanical):** `coef = +0.0009`, **p = 0.007** (Significant)
* **Model B (Net):** `coef = +0.0059`, **p = 0.012** (Significant)
* **Conclusion:** The Tempus provided measurable mechanical efficiency improvements. The "bucket seat" stability frame reduced lateral energy leakage, allowing for more efficient force transfer.

### 📉 The Loser: Saucony Endorphin Speed 3
* **Model A (Mechanical):** `coef = -0.0003`, **p = 0.450** (Not Significant)
* **Model B (Net):** `coef = +0.0044`, **p = 0.173** (Not Significant)
* **Conclusion:** Despite the nylon plate, the shoe provided **no statistically significant advantage** over a standard daily trainer.
* **The "Floorboard on a Waterbed" Effect:** Using a rigid orthotic (Superfeet Green) on the soft/unstable foam of the Speed 3 likely caused adductor fatigue as stabilizers worked to control the platform, negating any energy return from the plate.

## 🛠️ Tech Stack & Setup
* **Language:** Python 3.12+
* **Libraries:** `pandas`, `statsmodels`, `scikit-learn`, `numpy`
* **Data Source:** Garmin Connect (JSON exports)

### Quick Start
1.  Clone the repo.
2.  Install dependencies:
    ```bash
    pip install pandas statsmodels scikit-learn numpy
    ```
3.  Place your Garmin JSON data in `data/raw/`.
4.  Run the analysis:
    ```bash
    python analysis_v2.py
    ```

## 🔄 Future Work
This project successfully applied Causal Inference to historical data. The next phase will pivot to **Machine Learning (XGBoost/LSTM)** to build a predictive "AI Coach" that forecasts recovery scores and suggests workout modifications using Generative AI.
