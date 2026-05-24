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
                               exog_values=None, n_lags=6):
    quarter = (month - 1) // 3 + 1
    is_dry_season = 1 if month in [11, 12, 1, 2, 3] else 0
    month_sin = np.sin(2 * np.pi * month / 12)
    month_cos = np.cos(2 * np.pi * month / 12)

    row = {
        'month': month,
        'quarter': quarter,
        'year': year,
        'is_dry_season': is_dry_season,
        'month_sin': month_sin,
        'month_cos': month_cos,
    }

    for lag in range(1, n_lags + 1):
        row[f'rain_lag_{lag}'] = (
            history[-lag] if len(history) >= lag else 0.0
        )

    recent3 = history[-3:] if len(history) >= 3 else history
    recent6 = history[-6:] if len(history) >= 6 else history

    row['rain_roll3_mean'] = float(np.mean(recent3))
    row['rain_roll6_mean'] = float(np.mean(recent6))
    row['rain_roll3_std'] = float(np.std(recent3)) if len(recent3) > 1 else 0.0
    row['rain_roll3_min'] = float(np.min(recent3))
    row['rain_roll3_max'] = float(np.max(recent3))
    row['rain_lag_12'] = (history[-12] if len(history) >= 12
                          else float(np.mean(history)))
    row['rain_lag_24'] = (history[-24] if len(history) >= 24
                          else float(np.mean(history)))

    if exog_values:
        row.update(exog_values)

    return row