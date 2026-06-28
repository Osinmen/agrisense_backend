from pydantic import BaseModel, Field
from typing import List, Optional


class ForecastRequest(BaseModel):
    n_months        : int = Field(3, ge=1, le=6, description='Number of months to forecast (1-6)')
    temperature     : Optional[List[float]] = Field(None, description='Future Temperature_Celsius per month')
    humidity        : Optional[List[float]] = Field(None, description='Future Relative_Humidity_percent per month')
    solar_radiation : Optional[List[float]] = Field(None, description='Future Solar_Radiation_MJ_m2_per_month per month')
    pressure        : Optional[List[float]] = Field(None, description='Future Surface_Pressure_hPa per month')


class YieldEstimate(BaseModel):
    crop                    : str
    estimated_yield_tons_ha : float
    yield_range_tons_ha     : str
    potential_yield_tons_ha : float
    yield_percentage        : float
    viability               : str
    formula_breakdown       : dict


class PestWarning(BaseModel):
    type         : str
    risk_level   : str
    description  : str
    action       : str
    crops_at_risk: List[str]


class MonthForecast(BaseModel):
    month                 : str
    rainfall_mm           : float
    category              : str
    season                : str
    farming_advice        : str
    recommended_crops     : List[str]
    crops_to_avoid        : List[str]
    crop_yield_estimates  : List[YieldEstimate]
    best_crop_this_month  : str
    pest_disease_warnings : List[PestWarning] = []


class ForecastResponse(BaseModel):
    model_used             : str = 'CatBoost Multivariate'
    forecast_start         : str
    n_months               : int
    exog_source            : str
    monthly_forecast       : List[MonthForecast]
    best_crop_overall      : str
    overall_season_summary : str
