import numpy as np
from app.data.crop_params import CROP_PARAMS, CROP_ADVICE


def get_rainfall_category(mm: float) -> str:
    if mm < 50:
        return 'Low'
    elif mm < 150:
        return 'Moderate'
    elif mm < 300:
        return 'High'
    else:
        return 'Very High'


def estimate_yield(crop_name: str,
                   rainfall_mm: float,
                   temperature_c: float) -> dict:
    if crop_name not in CROP_PARAMS:
        return {'error': f'{crop_name} not found in crop database.'}

    p = CROP_PARAMS[crop_name]

    # Step 1 - WSI
    if rainfall_mm < p['min_rainfall']:
        wsi = 0.0
    else:
        wsi = min(1.0, rainfall_mm / p['optimal_rainfall'])

    # Step 2 - Yield ratio
    yield_ratio = 1 - p['ky'] * (1 - wsi)
    yield_ratio = float(np.clip(yield_ratio, 0.0, 1.0))

    # Step 3 - Temperature factor
    temp_dev = abs(temperature_c - p['optimal_temp'])
    temp_factor = float(max(0.0, 1 - p['temp_sensitivity'] * temp_dev))

    # Step 4 - Flood penalty
    flood_penalty = 0.30 if rainfall_mm > p['flood_threshold'] else 0.0

    # Step 5 - Final yield
    est_yield = (
        p['potential_yield']
        * yield_ratio
        * temp_factor
        * (1 - flood_penalty)
    )
    est_yield = round(max(0.0, est_yield), 3)

    lower = round(est_yield * 0.85, 3)
    upper = round(est_yield * 1.15, 3)
    pct = round(yield_ratio * temp_factor * (1 - flood_penalty) * 100, 1)

    if wsi == 0:
        viability = 'Crop failure risk - rainfall below minimum threshold'
    elif pct < 30:
        viability = 'Poor - significant stress'
    elif pct < 60:
        viability = 'Moderate - some stress factors present'
    elif pct < 85:
        viability = 'Good - acceptable yield expected'
    else:
        viability = 'Excellent - near-optimal conditions'

    return {
        'crop'                    : crop_name,
        'estimated_yield_tons_ha' : est_yield,
        'yield_range_tons_ha'     : f'{lower}-{upper}',
        'potential_yield_tons_ha' : p['potential_yield'],
        'yield_percentage'        : pct,
        'viability'               : viability,
        'formula_breakdown'       : {
            'WSI'             : round(wsi, 4),
            'yield_ratio_FAO' : round(yield_ratio, 4),
            'temp_factor'     : round(temp_factor, 4),
            'flood_penalty'   : flood_penalty,
            'formula'         : (
                f'Yield = {p["potential_yield"]} x {round(yield_ratio,3)}'
                f' x {round(temp_factor,3)} x (1 - {flood_penalty})'
                f' = {est_yield} tons/ha'
            ),
        },
    }


def estimate_all_crops(rainfall_mm: float,
                       temperature_c: float) -> list:
    category = get_rainfall_category(rainfall_mm)
    viable_crops = CROP_ADVICE[category]['crops']

    results = []
    for crop in viable_crops:
        clean_crop = crop.split('(')[0].strip()
        if clean_crop in CROP_PARAMS:
            est = estimate_yield(clean_crop, rainfall_mm, temperature_c)
            if 'error' not in est and est['estimated_yield_tons_ha'] > 0:
                results.append(est)

    return sorted(results,
                  key=lambda x: x['yield_percentage'],
                  reverse=True)