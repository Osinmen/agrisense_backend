# agrisense_backend
# AgriSense Rainfall Advisory API

A FastAPI-powered machine learning backend for rainfall forecasting and crop advisory in Ondo State, Nigeria.

## Overview

AgriSense API provides monthly rainfall predictions using a CatBoost multivariate regression model trained on 42 years (1984–2025) of historical climate data from Ondo State. The system integrates rainfall forecasting with FAO AquaCrop yield estimation, pest and disease risk assessment, and SHAP explainability.

## Features

- **Rainfall Forecasting**: Recursive multi-step predictions up to 6 months ahead using CatBoost with lag features, rolling statistics and exogenous climate variables
- **Crop Yield Estimation**: FAO AquaCrop water stress index formula applied to 16 crops specific to Ondo State
- **Pest & Disease Warnings**: Rule-based pest risk detection based on predicted humidity and seasonal patterns
- **SHAP Explainability**: Feature importance explanations for every prediction using CatBoost native SHAP values
- **Crop Calendar**: Monthly planting windows for all supported crops
- **Climatological Bounds**: Per-month prediction constraints derived from 42-year historical analysis to prevent outlier-driven anomalies

## Tech Stack

- **Framework**:  FastAPI
- **ML Model**: CatBoost Regressor (Optuna-tuned)
- **Data**: NASA POWER reanalysis climate dataset (1984–2025)
- **Python**: 3.10+

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/forecast/` | Generate monthly rainfall forecast and crop advisory |
| GET | `/crops/` | All crop parameters and optimal conditions |
| GET | `/crops/calendar/` | Monthly planting calendar for all crops |
| GET | `/crops/advice/` | Farming advice by rainfall category |
| GET | `/crops/pests/` | Pest and disease database |
| GET | `/health/` | API health check |

## Model Performance

| Metric | Value |
|--------|-------|
| RMSE | 0.76 |
| MAE | 56mm |
| R² | 0.76 |
| NSE | 0.76 |
| KGE | 0.81 |
| PBIAS | 1.36 % |


## Installation

```bash
git clone https://github.com/yourusername/agrisense-api.git
cd agrisense-api
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

## Running the API

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Visit `http://localhost:8000/docs` for interactive API documentation.

## Project Structure
rainfall_advisory_api/
├── app/
│   ├── data/
│   │   ├── crop_params.py          # Crop parameters and advice
│   │   └── ondo_climate_merged.csv # 42-year historical dataset
│   ├── routers/
│   │   ├── forecast.py             # Forecast endpoints
│   │   ├── crops.py                # Crop endpoints
│   │   └── health.py               # Health check
│   ├── schemas/
│   │   └── forecast_schema.py      # Pydantic request/response models
│   ├── services/
│   │   ├── model_service.py        # CatBoost model loader
│   │   ├── forecast_service.py     # Recursive forecasting logic
│   │   ├── climatology_service.py  # Historical data service
│   │   └── yield_service.py        # FAO AquaCrop yield estimation
│   ├── utils/
│   │   └── helpers.py              # Feature engineering
│   └── main.py                     # FastAPI app entry point
├── trained_models/
│   └── cat_mul.cbm                 # Trained CatBoost model
├── requirements.txt
└── README.md

## Data Sources

- **Climate Data**: NASA POWER API (temperature, humidity, solar radiation, surface pressure)
- **Rainfall Data**: NASA POWER API
- **Crop Parameters**: FAO AquaCrop documentation and IITA West Africa agronomic guidelines
- **Pest Database**: OSSADEP (Ondo State Agricultural Development Programme) field records

## Research Context

This API was developed as part of postgraduate research on rainfall forecasting for smallholder farmers in Ondo State, Nigeria. The model compares CatBoost, LightGBM and Prophet approaches, with CatBoost multivariate achieving the best performance across RMSE, NSE and KGE metrics.

## License

MIT License — free to use for research and non-commercial purposes.

## Author

Victory Airen — Undergraduate Researcher, Agricultural AI
