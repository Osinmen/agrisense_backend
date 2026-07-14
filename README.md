# 🌧️ AgriSense — Rainfall Forecasting & Agricultural Advisory API

> A hybrid machine learning system for seasonal rainfall prediction and crop advisory generation for smallholder farmers in Ondo State, Nigeria.

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com)
[![CatBoost](https://img.shields.io/badge/CatBoost-Multivariate-orange.svg)](https://catboost.ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📌 Overview

AgriSense is a REST API backend for a seasonal agricultural planning system targeting smallholder farmers in Ondo State, Nigeria. The system forecasts monthly rainfall up to 12 months ahead using a multivariate CatBoost gradient boosting model trained on 42 years of NASA POWER climate data (1984–2025), and translates forecast outputs into actionable crop advisory recommendations covering planting windows, expected pest and disease pressures, and estimated crop yield ranges.

A key innovation is the **Macro-Seasonal Adaptive Winsorization Pipeline (MSAW)** — a novel post-processing layer that dynamically constrains recursive forecast outputs using historically calibrated monthly volumetric tiers, preventing autoregressive error propagation while preserving full predictive freedom during the main wet season.

---

## 🏗️ System Architecture
┌─────────────────────────────────────────────────────────────┐
│                    Flutter Mobile App                        │
│         (English + Yoruba | iOS + Android)                  │
│                                                             │
│   ┌─────────────────┐    ┌──────────────────────────────┐  │
│   │ OpenMeteo API   │    │  AgriSense FastAPI Backend   │  │
│   │ (Daily Weather) │    │  (Seasonal ML Forecast)      │  │
│   └─────────────────┘    └──────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
│
┌──────────────▼──────────────┐
│      FastAPI Backend         │
│                             │
│  ┌─────────────────────┐    │
│  │  CatBoost Model     │    │
│  │  (.cbm artefact)    │    │
│  └──────────┬──────────┘    │
│             │               │
│  ┌──────────▼──────────┐    │
│  │   MSAW Layer        │    │
│  │ (Post-Processing)   │    │
│  └──────────┬──────────┘    │
│             │               │
│  ┌──────────▼──────────┐    │
│  │  Advisory Engine    │    │
│  │  (Crop + Pest +     │    │
│  │   Yield Rules)      │    │
│  └──────────┬──────────┘    │
│             │               │
│  ┌──────────▼──────────┐    │
│  │  Firebase Firestore  │    │
│  │  + Local Push       │    │
│  │  Notifications      │    │
│  └─────────────────────┘    │
└─────────────────────────────┘
---

## 🤖 Model Performance

The CatBoost Multivariate model was selected as the deployment model following empirical comparison across eight forecasting architectures.

| Metric | CatBoost Multivariate | LightGBM Multivariate | Prophet Multivariate |
|--------|----------------------|----------------------|---------------------|
| RMSE (mm/month) | **56.44** | 64.40 | 77.99 |
| MAE (mm/month) | **43.96** | 49.54 | 53.52 |
| R² | **0.7638** | 0.6924 | 0.6083 |
| NSE | **0.7638** | 0.6924 | 0.6083 |
| KGE | **0.8178** ✅ | 0.7154 ✅ | 0.6867 |
| PBIAS (%) | **1.36** ✅ | 9.80 ✅ | 6.79 |

> KGE > 0.75 is classified as good performance in hydrometeorological forecasting (Gupta et al., 2009). PBIAS within ±10% is classified as very good (Moriasi et al., 2007).

---

## 🔬 Novel Contributions

### 1. Macro-Seasonal Adaptive Winsorization Pipeline (MSAW)
A data-driven Dynamic Post-Processing Bounding Layer that constrains recursive forecast outputs using three climatological tiers based on historical monthly mean volume:

| Tier | Condition | Multiplier | Target Months |
|------|-----------|------------|---------------|
| Deep Dry Season | μ < 50 mm | λ = 0.20 | Dec, Jan, Feb |
| Seasonal Transition | 50 ≤ μ < 100 mm | λ = 0.50 | Mar, Nov |
| Main Wet Season | μ ≥ 100 mm | λ = 1.50 | Apr – Oct |

dynamic_cap   = μ_m + (λ_m × σ_m)
dynamic_floor = max(0, μ_m − (λ_m × σ_m))
prediction    = clip(raw_pred, dynamic_floor, dynamic_cap)

**Verified outcomes:** December 2026 hallucination suppressed from 94mm → 26mm. November transition spike constrained from 99.9mm → 92mm. July wet season prediction left unconstrained at 193mm.

### 2. Recursive Multi-Step Evaluation
Unlike conventional one-step-ahead evaluation, this system evaluates model performance under live recursive autoregressive multi-step forecasting — the actual deployment condition — directly exposing and resolving the error cascade vulnerability.

### 3. End-to-End Operational Pipeline
Raw 42-year climate data → feature engineering → CatBoost training → MSAW post-processing → crop advisory rules → JSON payloads → Flutter mobile application serving English and Yoruba language users.

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/forecast/` | Generate recursive multi-month rainfall forecast with MSAW post-processing |
| `GET` | `/advisory/{month}` | Retrieve crop advisory for a specific forecast month |
| `GET` | `/historical/` | Access historical climate data |
| `GET` | `/health` | API health check |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| API Framework | FastAPI (Python) |
| ML Model | CatBoost Multivariate |
| Post-Processing | MSAW (custom) |
| Database | Firebase Firestore |
| Notifications | Flutter Local Notifications |
| Mobile Frontend | Flutter (Dart) — iOS + Android |
| Weather (real-time) | OpenMeteo API |
| Training Data | NASA POWER API |
| Deployment | Render |

---

## 📊 Data Sources

- **Climate Data** — NASA POWER API (rainfall, temperature, relative humidity, solar radiation, surface pressure) — 42 years (1984–2025), 504 monthly observations
- **Crop Parameters** — FAO AquaCrop documentation and IITA West Africa agronomic guidelines
- **Pest and Disease Database** — OSSADEP (Ondo State Agricultural Development Programme) field records

---

## ⚙️ Installation and Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/agrisense-api.git
cd agrisense-api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the API locally
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Environment Variables

Create a `.env` file in the root directory:

```env
MODEL_DIR=models/
HISTORICAL_DATA_PATH=models/historical_data.csv
N_LAGS=12
TARGET_COL=Rainfall_mm_per_month
DATE_COL=DATE
```

---

## 🌱 Crop Advisory System

The advisory engine maps forecast rainfall to agricultural recommendations covering:

- **Recommended crops** — based on Water Satisfaction Index (WSI) and FAO AquaCrop yield model
- **Crops to avoid** — waterlogging or drought risk assessment
- **Estimated yield ranges** — per-crop yield prediction with temperature and flood penalty factors
- **Pest and disease alerts** — humidity and temperature driven pest pressure warnings
- **Planting window guidance** — onset and cessation of rainy season detection

---

## 🔑 Key References

- Gupta, H.V. et al. (2009). Decomposition of the mean squared error and NSE. *Journal of Hydrology*, 377(1-2), 80-91.
- Moriasi, D.N. et al. (2007). Model evaluation guidelines for systematic quantification of accuracy in watershed simulations. *Transactions of the ASABE*, 50(3), 885-900.
- Prokhorenkova, L. et al. (2018). CatBoost: unbiased boosting with categorical features. *NeurIPS*, 31.
- Nash, J.E. and Sutcliffe, J.V. (1970). River flow forecasting through conceptual models. *Journal of Hydrology*, 10(3), 282-290.

---

## 📄 License

MIT License — free to use for academic research and non-commercial purposes.

---

## 👨‍💻 Author

**Airen Victory Osinmen**  
Final Year Computer Engineering Student  
Capstone Project — Agricultural AI and Climate Forecasting  
Ondo State, Nigeria

---

## 🎓 Research Context

This API was developed as a final year capstone project investigating machine learning approaches for seasonal rainfall forecasting and agricultural decision support in Ondo State, Nigeria. The study compares eight forecasting architectures including SARIMA, SARIMAX, Prophet, LightGBM, and CatBoost, with CatBoost Multivariate achieving the best performance across all hydrometeorological evaluation metrics. A novel post-processing framework — the Macro-Seasonal Adaptive Winsorization Pipeline — was developed to address the documented extrapolation blindness of tree-based gradient boosting models in recursive multi-step forecasting contexts, making this system suitable for operational agricultural deployment.

> *"While advanced gradient-boosting architectures achieve high statistical accuracy globally, they lack inherent physical and climatological constraints, often producing severe predictive anomalies during dry seasonal transitions. The MSAW framework addresses this gap through data-driven adaptive climatological bounding."*

---

*Last updated: July 2026*
