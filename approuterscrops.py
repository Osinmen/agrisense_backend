import logging
from fastapi import APIRouter, HTTPException
from app.data.crop_params import CROP_PARAMS, CROP_ADVICE, PEST_DATABASE

logger = logging.getLogger(__name__)
router = APIRouter(prefix='/crops', tags=['Crops'])

MONTH_NAMES = [
    '', 'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
]


@router.get('/')
def get_all_crops():
    details = {}
    for crop, params in CROP_PARAMS.items():
        details[crop] = {
            'potential_yield'  : params['potential_yield'],
            'optimal_rainfall' : params['optimal_rainfall'],
            'min_rainfall'     : params['min_rainfall'],
            'flood_threshold'  : params['flood_threshold'],
            'optimal_temp'     : params['optimal_temp'],
            'growth_days'      : params['growth_days'],
            'planting_months'  : params['planting_months'],
        }
    return {
        'total_crops': len(CROP_PARAMS),
        'crops'      : list(CROP_PARAMS.keys()),
        'details'    : details,
    }


@router.get('/calendar/')
def get_crop_calendar():
    crop_calendar = {}
    for crop, params in CROP_PARAMS.items():
        crop_calendar[crop] = {
            'planting_months'      : params['planting_months'],
            'planting_months_names': [MONTH_NAMES[m] for m in params['planting_months']],
            'growth_days'          : params['growth_days'],
            'potential_yield_t_ha' : params['potential_yield'],
            'optimal_rainfall_mm'  : params['optimal_rainfall'],
            'optimal_temp_c'       : params['optimal_temp'],
        }
    return crop_calendar


@router.get('/advice/')
def get_crop_advice():
    return CROP_ADVICE


@router.get('/pests/')
def get_pest_database():
    result = {}
    for pest, data in PEST_DATABASE.items():
        result[pest] = {
            'crops_affected'     : data['crops_affected'],
            'risk_level'         : data['risk_level'],
            'season'             : data['season'],
            'active_months_names': [MONTH_NAMES[m] for m in data['season']],
            'description'        : data['description'],
            'prevention'         : data['prevention'],
        }
    return {'total_pests': len(PEST_DATABASE), 'pests': result}
