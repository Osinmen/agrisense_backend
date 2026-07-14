import numpy as np
import pandas as pd
from typing import List, Optional


def get_rainfall_category(mm: float) -> str:
    if mm < 50:
        return 'Low'
    elif mm < 150:
        return 'Moderate'
    elif mm < 300:
        return 'High'
    else:
        return 'Very High'


def get_climatology(historical_df, date_col, exog_features):
    df = historical_df.copy()
    df['_month'] = pd.to_datetime(df[date_col]).dt.month
    return df.groupby('_month')[exog_features].mean()


def build_single_row_features(history, month, year,
                               exog_values=None, n_lags=12,
                               climatology_means=None,
                               climatology_stds=None):
    """
    Builds a single feature row matching the retrained CatBoost model.
    Includes all new features: season flags, climatology, anomaly, trend.
    """
    quarter       = (month - 1) // 3 + 1
    is_dry_season = 1 if month in [11, 12, 1, 2, 3] else 0
    is_peak_wet   = 1 if month in [8, 9, 10]         else 0
    is_onset_wet  = 1 if month in [4, 5, 6]           else 0
    month_sin     = np.sin(2 * np.pi * month / 12)
    month_cos     = np.cos(2 * np.pi * month / 12)

    row = {
        'month'        : month,
        'quarter'      : quarter,
        'year'         : year,
        'is_dry_season': is_dry_season,
        'is_peak_wet'  : is_peak_wet,
        'is_onset_wet' : is_onset_wet,
        'month_sin'    : month_sin,
        'month_cos'    : month_cos,
    }

    # Lag features 1 to n_lags
    for lag in range(1, n_lags + 1):
        row[f'rain_lag_{lag}'] = (
            history[-lag] if len(history) >= lag else 0.0
        )

    # Rolling statistics
    recent3 = history[-3:] if len(history) >= 3 else history
    recent6 = history[-6:] if len(history) >= 6 else history

    row['rain_roll3_mean'] = float(np.mean(recent3))
    row['rain_roll6_mean'] = float(np.mean(recent6))
    row['rain_roll3_std']  = float(np.std(recent3)) if len(recent3) > 1 else 0.0
    row['rain_roll3_min']  = float(np.min(recent3))
    row['rain_roll3_max']  = float(np.max(recent3))

    # Same month previous years
    row['rain_lag_24'] = (history[-24] if len(history) >= 24
                          else float(np.mean(history)))

    # Climatological features
    clim_mean = (climatology_means.get(month, float(np.mean(history)))
                 if climatology_means else float(np.mean(history)))
    clim_std  = (climatology_stds.get(month, float(np.std(history)))
                 if climatology_stds else float(np.std(history)))

    row['month_clim_mean'] = clim_mean
    row['month_clim_std']  = clim_std

    # Anomaly — last month deviation from its climatological normal
    last_month     = (month - 2) % 12 + 1  # previous calendar month
    last_clim_mean = (climatology_means.get(last_month, float(np.mean(history)))
                      if climatology_means else float(np.mean(history)))
    last_rain      = history[-1] if len(history) >= 1 else 0.0
    row['rain_anomaly'] = last_rain - last_clim_mean

    # Trend features
    rain_lag1 = history[-1] if len(history) >= 1 else 0.0
    rain_lag2 = history[-2] if len(history) >= 2 else 0.0
    rain_lag4 = history[-4] if len(history) >= 4 else 0.0

    row['rain_trend']   = rain_lag1 - rain_lag2
    row['rain_trend_3'] = rain_lag1 - rain_lag4

    if exog_values:
        row.update(exog_values)

    return row