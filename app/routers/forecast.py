import logging
import numpy as np
from fastapi import APIRouter, HTTPException
from app.schemas.forecast_schema import ForecastRequest, ForecastResponse
from app.services.forecast_service import (
    generate_future_dates,
    build_exog_list,
    recursive_forecast,
)
from app.services.yield_service import estimate_all_crops, get_rainfall_category
from app.services.climatology_service import climatology_service
from app.data.crop_params import CROP_ADVICE, PEST_DATABASE

logger = logging.getLogger(__name__)

router = APIRouter(prefix='/forecast', tags=['Forecast'])


def _get_pest_warnings(month: int, humidity: float) -> list:
    warnings = []
    for pest, info in PEST_DATABASE.items():
        if month not in info['season']:
            continue
        if humidity < info.get('humidity_threshold', 0):
            continue
        warnings.append({
            'type'         : pest,
            'risk_level'   : info['risk_level'],
            'description'  : info['description'],
            'action'       : info['prevention'],
            'crops_at_risk': info['crops_affected'],
        })
    return warnings


@router.post('/', response_model=ForecastResponse)
def predict_rainfall(request: ForecastRequest):
    if not climatology_service.is_loaded:
        raise HTTPException(
            status_code=503,
            detail='Climatology service not ready. Try again shortly.'
        )

    try:
        future_dates = generate_future_dates(None, request.n_months)

        exog_list = build_exog_list(
            future_dates    = future_dates,
            temperature     = request.temperature,
            humidity        = request.humidity,
            solar_radiation = request.solar_radiation,
            pressure        = request.pressure,
        )

        exog_source = (
            'user-supplied'
            if any([request.temperature, request.humidity,
                    request.solar_radiation, request.pressure])
            else 'climatology'
        )

        predictions = recursive_forecast(future_dates, exog_list)

    except FileNotFoundError as e:
        logger.error(f'File error: {e}')
        raise HTTPException(status_code=500, detail=str(e))
    except RuntimeError as e:
        logger.error(f'Runtime error: {e}')
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f'Unexpected error: {e}')
        raise HTTPException(status_code=500, detail=f'Unexpected error: {str(e)}')

    monthly_forecast = []
    all_yield_scores = {}

    for i, (dt, mm) in enumerate(zip(future_dates, predictions)):
        category     = get_rainfall_category(mm)
        db           = CROP_ADVICE[category]
        temp_c       = exog_list[i]['Temperature_Celsius']
        humidity_val = exog_list[i].get('Relative_Humidity_percent', 75)

        yield_estimates = estimate_all_crops(mm, temp_c)
        best_crop       = yield_estimates[0]['crop'] if yield_estimates else 'None'
        pest_warnings   = _get_pest_warnings(dt.month, humidity_val)

        for est in yield_estimates:
            crop = est['crop']
            all_yield_scores.setdefault(crop, [])
            all_yield_scores[crop].append(est['yield_percentage'])

        monthly_forecast.append({
            'month'                : dt.strftime('%B %Y'),
            'rainfall_mm'          : mm,
            'category'             : category,
            'season'               : db['season'],
            'farming_advice'       : db['advice'],
            'recommended_crops'    : db['crops'],
            'crops_to_avoid'       : db['avoid'],
            'crop_yield_estimates' : yield_estimates,
            'best_crop_this_month' : best_crop,
            'pest_disease_warnings': pest_warnings,
        })

    best_overall = (
        max(all_yield_scores,
            key=lambda c: np.mean(all_yield_scores[c]))
        if all_yield_scores else 'None'
    )

    avg_rain = round(float(np.mean(predictions)), 2)
    avg_cat  = get_rainfall_category(avg_rain)

    summary = (
        f'Over the next {request.n_months} month(s), '
        f'average predicted rainfall is {avg_rain}mm/month '
        f'({avg_cat} category). '
        f'Best crop recommendation: {best_overall}. '
        f'{CROP_ADVICE[avg_cat]["advice"]}'
    )

    return ForecastResponse(
        model_used             = 'CatBoost Multivariate',
        forecast_start         = future_dates[0].strftime('%B %Y'),
        n_months               = request.n_months,
        exog_source            = exog_source,
        monthly_forecast       = monthly_forecast,
        best_crop_overall      = best_overall,
        overall_season_summary = summary,
    )
