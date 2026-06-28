import pandas as pd
import numpy as np
import logging
from datetime import datetime
from typing import List, Optional
from app.config import settings
from app.utils.helpers import build_single_row_features
from app.services.model_service import model_service
from app.services.climatology_service import climatology_service

logger = logging.getLogger(__name__)


def generate_future_dates(last_date, n_months: int) -> pd.DatetimeIndex:
    """
    Generates future dates starting from NEXT month.
    If today is May 2026 and n_months=3, returns June, July, August 2026.
    """
    today = datetime.now()
    if today.month == 12:
        start_date = today.replace(year=today.year + 1, month=1, day=1)
    else:
        start_date = today.replace(month=today.month + 1, day=1)

    return pd.date_range(
        start   = start_date,
        periods = n_months,
        freq    = 'MS'
    )


def build_exog_list(future_dates: pd.DatetimeIndex,
                    temperature: Optional[List[float]],
                    humidity: Optional[List[float]],
                    solar_radiation: Optional[List[float]],
                    pressure: Optional[List[float]]) -> List[dict]:
    exog_list = []
    for i, dt in enumerate(future_dates):
        clim = climatology_service.get_exog_for_month(dt.month)

        def _get(user_vals, key):
            if user_vals and i < len(user_vals):
                return float(user_vals[i])
            return clim[key]

        exog = {
            'Temperature_Celsius'            : _get(temperature,    'Temperature_Celsius'),
            'Relative_Humidity_percent'      : _get(humidity,       'Relative_Humidity_percent'),
            'Solar_Radiation_MJ_m2_per_month': _get(solar_radiation,'Solar_Radiation_MJ_m2_per_month'),
            'Surface_Pressure_hPa'           : _get(pressure,       'Surface_Pressure_hPa'),
        }
        exog_list.append(exog)

    return exog_list

def recursive_forecast(future_dates: pd.DatetimeIndex,
                       exog_list: List[dict]) -> List[float]:
    history = climatology_service.get_rainfall_history()
    predictions = []

    for i, dt in enumerate(future_dates):
        row = build_single_row_features(
            history=history,
            month=dt.month,
            year=dt.year,
            exog_values=exog_list[i],
            n_lags=settings.N_LAGS
        )

        X_row = pd.DataFrame([row])[model_service.feature_cols]
        pred = model_service.predict(X_row)
        predictions.append(round(pred, 2))
        history.append(pred)
        logger.debug(f'{dt.strftime("%b %Y")} predicted: {pred:.2f} mm')

    return predictions