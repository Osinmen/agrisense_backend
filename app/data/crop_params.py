CROP_PARAMS = {
    'Maize': {
        'potential_yield'  : 4.5,
        'optimal_rainfall' : 120.0,
        'min_rainfall'     : 40.0,
        'flood_threshold'  : 280.0,
        'optimal_temp'     : 25.0,
        'temp_sensitivity' : 0.04,
        'ky'               : 1.25,
        'growth_days'      : 90,
        'planting_months'  : [3, 4, 8, 9],
    },
    'Cassava': {
        'potential_yield'  : 25.0,
        'optimal_rainfall' : 150.0,
        'min_rainfall'     : 50.0,
        'flood_threshold'  : 320.0,
        'optimal_temp'     : 27.0,
        'temp_sensitivity' : 0.03,
        'ky'               : 0.75,
        'growth_days'      : 365,
        'planting_months'  : [3, 4, 5],
    },
    'Yam': {
        'potential_yield'  : 20.0,
        'optimal_rainfall' : 175.0,
        'min_rainfall'     : 80.0,
        'flood_threshold'  : 300.0,
        'optimal_temp'     : 28.0,
        'temp_sensitivity' : 0.035,
        'ky'               : 1.0,
        'growth_days'      : 210,
        'planting_months'  : [2, 3, 4],
    },
    'Rice': {
        'potential_yield'  : 4.0,
        'optimal_rainfall' : 200.0,
        'min_rainfall'     : 150.0,
        'flood_threshold'  : 350.0,
        'optimal_temp'     : 28.0,
        'temp_sensitivity' : 0.04,
        'ky'               : 1.15,
        'growth_days'      : 120,
        'planting_months'  : [5, 6, 7],
    },
    'Cowpea': {
        'potential_yield'  : 1.2,
        'optimal_rainfall' : 70.0,
        'min_rainfall'     : 25.0,
        'flood_threshold'  : 180.0,
        'optimal_temp'     : 27.0,
        'temp_sensitivity' : 0.045,
        'ky'               : 0.85,
        'growth_days'      : 75,
        'planting_months'  : [7, 8],
    },
    'Groundnut': {
        'potential_yield'  : 1.5,
        'optimal_rainfall' : 80.0,
        'min_rainfall'     : 30.0,
        'flood_threshold'  : 200.0,
        'optimal_temp'     : 28.0,
        'temp_sensitivity' : 0.04,
        'ky'               : 0.70,
        'growth_days'      : 100,
        'planting_months'  : [7, 8],
    },
    'Plantain': {
        'potential_yield'  : 25.0,
        'optimal_rainfall' : 160.0,
        'min_rainfall'     : 80.0,
        'flood_threshold'  : 320.0,
        'optimal_temp'     : 27.0,
        'temp_sensitivity' : 0.03,
        'ky'               : 0.85,
        'growth_days'      : 300,
        'planting_months'  : [3, 4, 5, 6, 7, 8, 9, 10],
    },
    'Soybean': {
        'potential_yield'  : 2.0,
        'optimal_rainfall' : 100.0,
        'min_rainfall'     : 40.0,
        'flood_threshold'  : 220.0,
        'optimal_temp'     : 26.0,
        'temp_sensitivity' : 0.04,
        'ky'               : 0.85,
        'growth_days'      : 100,
        'planting_months'  : [6, 7],
    },
    'Cocoa': {
        'potential_yield'  : 0.5,
        'optimal_rainfall' : 175.0,
        'min_rainfall'     : 100.0,
        'flood_threshold'  : 300.0,
        'optimal_temp'     : 25.0,
        'temp_sensitivity' : 0.05,
        'ky'               : 1.2,
        'growth_days'      : 365,
        'planting_months'  : [3, 4, 5, 6, 7, 8, 9, 10],
    },
    'Millet': {
        'potential_yield'  : 1.5,
        'optimal_rainfall' : 60.0,
        'min_rainfall'     : 20.0,
        'flood_threshold'  : 160.0,
        'optimal_temp'     : 28.0,
        'temp_sensitivity' : 0.035,
        'ky'               : 0.65,
        'growth_days'      : 75,
        'planting_months'  : [6, 7],
    },
    'Sorghum': {
        'potential_yield'  : 1.8,
        'optimal_rainfall' : 80.0,
        'min_rainfall'     : 25.0,
        'flood_threshold'  : 200.0,
        'optimal_temp'     : 28.0,
        'temp_sensitivity' : 0.035,
        'ky'               : 0.90,
        'growth_days'      : 100,
        'planting_months'  : [6, 7],
    },
    'Rubber': {
        'potential_yield'  : 1.5,    # tons/ha dry rubber
        'optimal_rainfall' : 200.0,
        'min_rainfall'     : 120.0,
        'flood_threshold'  : 350.0,
        'optimal_temp'     : 27.0,
        'temp_sensitivity' : 0.04,
        'ky'               : 0.90,
        'growth_days'      : 2555,   # 7 years to first tapping
        'planting_months'  : [3, 4, 5, 6],
    },
    'Oil Palm': {
        'potential_yield'  : 20.0,   # tons/ha fresh fruit bunch
        'optimal_rainfall' : 180.0,
        'min_rainfall'     : 100.0,
        'flood_threshold'  : 350.0,
        'optimal_temp'     : 27.0,
        'temp_sensitivity' : 0.03,
        'ky'               : 0.85,
        'growth_days'      : 1095,   # 3 years to first harvest
        'planting_months'  : [4, 5, 6, 7],
    },
    'Tomato': {
        'potential_yield'  : 20.0,   # tons/ha fresh weight
        'optimal_rainfall' : 100.0,
        'min_rainfall'     : 50.0,
        'flood_threshold'  : 200.0,
        'optimal_temp'     : 24.0,
        'temp_sensitivity' : 0.06,
        'ky'               : 1.05,
        'growth_days'      : 90,
        'planting_months'  : [10, 11, 12, 1, 2],  # dry season crop
    },
    'Pepper': {
        'potential_yield'  : 8.0,
        'optimal_rainfall' : 90.0,
        'min_rainfall'     : 40.0,
        'flood_threshold'  : 200.0,
        'optimal_temp'     : 26.0,
        'temp_sensitivity' : 0.05,
        'ky'               : 0.90,
        'growth_days'      : 120,
        'planting_months'  : [10, 11, 12, 1, 2],
    },
    'Onion': {
        'potential_yield'  : 15.0,
        'optimal_rainfall' : 70.0,
        'min_rainfall'     : 20.0,
        'flood_threshold'  : 150.0,
        'optimal_temp'     : 24.0,
        'temp_sensitivity' : 0.05,
        'ky'               : 1.10,
        'growth_days'      : 120,
        'planting_months'  : [11, 12, 1, 2],  # strictly dry season
    },
}


CROP_ADVICE = {
    'Low': {
        'range'  : '0-50mm',
        'season' : 'Dry Season',
        'crops'  : ['Cowpea', 'Millet', 'Sorghum', 'Groundnut',
                    'Tomato', 'Pepper', 'Onion'],
        'avoid'  : ['Rice', 'Yam', 'Cassava', 'Cocoa',
                    'Rubber', 'Oil Palm'],
        'advice' : (
            'Dry conditions expected. Plant drought-tolerant crops. '
            'Use mulching to conserve soil moisture. '
            'Tomato, pepper and onion thrive in dry season with irrigation. '
            'Do NOT establish new cocoa, rubber or oil palm.'
        ),
    },
    'Moderate': {
        'range'  : '50-150mm',
        'season' : 'Early/Late Wet Season',
        'crops'  : ['Maize', 'Groundnut', 'Soybean', 'Cowpea',
                    'Plantain', 'Cassava', 'Oil Palm'],
        'avoid'  : ['Rice', 'Onion', 'Tomato'],
        'advice' : (
            'Good planting conditions for most staple crops. '
            'Ideal for maize and legumes. '
            'Oil palm establishment suitable this period. '
            'Cocoa farms in maintenance — monitor for black pod disease.'
        ),
    },
    'High': {
        'range'  : '150-300mm',
        'season' : 'Peak Wet Season',
        'crops'  : ['Cassava', 'Yam', 'Rice', 'Plantain',
                    'Maize', 'Cocoa', 'Rubber', 'Oil Palm'],
        'avoid'  : ['Groundnut', 'Millet', 'Onion', 'Tomato', 'Pepper'],
        'advice' : (
            'Peak wet season. Excellent for high-water crops. '
            'Best period for cocoa and rubber establishment in Ondo State. '
            'Monitor for fungal diseases. '
            'Avoid vegetables — excess rain causes rot and disease.'
        ),
    },
    'Very High': {
        'range'  : '300mm+',
        'season' : 'Flood Risk Period',
        'crops'  : ['Cassava', 'Plantain', 'Rubber'],
        'avoid'  : ['Maize', 'Yam', 'Groundnut', 'Cowpea',
                    'Cocoa', 'Tomato', 'Pepper', 'Onion', 'Rice'],
        'advice' : (
            'Flood risk. Avoid planting in low-lying areas. '
            'Ensure drainage channels are cleared. '
            'Only flood-tolerant crops recommended. '
            'Apply copper-based fungicide on cocoa farms immediately.'
        ),
    },
}


# Common pests and diseases for Ondo State
PEST_DATABASE = {
    'Fall Armyworm': {
        'crops_affected' : ['Maize', 'Sorghum', 'Millet'],
        'humidity_threshold': 70,
        'season'         : [5, 6, 7, 8, 9, 10],
        'risk_level'     : 'High',
        'description'    : (
            'Fall armyworm can destroy entire maize fields within days. '
            'Most active during wet season in Ondo State.'
        ),
        'prevention'     : (
            'Scout fields twice weekly. '
            'Apply Emamectin benzoate at first sign of damage. '
            'Use pheromone traps for early detection. '
            'Report outbreaks to local OSSADEP office.'
        ),
    },
    'Black Pod Disease': {
        'crops_affected'    : ['Cocoa'],
        'humidity_threshold': 80,
        'season'            : [5, 6, 7, 8, 9, 10],
        'risk_level'        : 'High',
        'description'       : (
            'Phytophthora black pod is the biggest threat to cocoa '
            'in Ondo State causing up to 80% yield loss if uncontrolled.'
        ),
        'prevention'        : (
            'Apply Kocide 2000 or Nordox every 3 weeks. '
            'Remove and destroy infected pods. '
            'Maintain farm sanitation.'
        ),
    },
    'Stem Borer': {
        'crops_affected'    : ['Maize', 'Sorghum'],
        'humidity_threshold': 65,
        'season'            : [4, 5, 6, 7, 8],
        'risk_level'        : 'Moderate',
        'description'       : (
            'Stem borers tunnel into maize stalks reducing yield '
            'by 20-40% if not controlled.'
        ),
        'prevention'        : (
            'Apply Furadan granules into maize whorl at 2 and 4 WAE. '
            'Plant early to avoid peak borer population. '
            'Use resistant varieties.'
        ),
    },
    'Cassava Mosaic Virus': {
        'crops_affected'    : ['Cassava'],
        'humidity_threshold': 75,
        'season'            : [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        'risk_level'        : 'Moderate',
        'description'       : (
            'Spread by whiteflies. Causes leaf distortion and '
            'significant yield loss in cassava.'
        ),
        'prevention'        : (
            'Use certified disease-free stems only. '
            'Plant resistant varieties TMS 30572 or TMS 4(2)1425. '
            'Control whitefly with insecticide.'
        ),
    },
    'Root Rot': {
        'crops_affected'    : ['Yam', 'Cassava', 'Oil Palm'],
        'humidity_threshold': 85,
        'season'            : [6, 7, 8, 9],
        'risk_level'        : 'High',
        'description'       : (
            'Excess moisture causes root and tuber rot reducing '
            'yield drastically in waterlogged soils.'
        ),
        'prevention'        : (
            'Ensure proper drainage on farm. '
            'Plant on ridges or mounds. '
            'Apply fungicide drench at planting.'
        ),
    },
    'Aphids': {
        'crops_affected'    : ['Maize', 'Cowpea', 'Groundnut',
                               'Tomato', 'Pepper'],
        'humidity_threshold': 0,    # active in dry conditions
        'temp_threshold'    : 30,   # active when hot
        'season'            : [11, 12, 1, 2, 3],
        'risk_level'        : 'Moderate',
        'description'       : (
            'Aphids multiply rapidly in hot dry conditions '
            'and spread viral diseases to vegetables and legumes.'
        ),
        'prevention'        : (
            'Apply neem oil spray or insecticidal soap. '
            'Use Lambda-cyhalothrin for severe infestation. '
            'Encourage natural predators.'
        ),
    },
    'Tomato Blight': {
        'crops_affected'    : ['Tomato', 'Pepper'],
        'humidity_threshold': 80,
        'season'            : [1, 2, 3, 10, 11, 12],
        'risk_level'        : 'High',
        'description'       : (
            'Early and late blight caused by Alternaria and '
            'Phytophthora destroy tomato and pepper crops quickly.'
        ),
        'prevention'        : (
            'Apply Mancozeb or Ridomil every 7-10 days. '
            'Avoid overhead irrigation. '
            'Remove and destroy infected plant material.'
        ),
    },
    'Rubber Leaf Blight': {
        'crops_affected'    : ['Rubber'],
        'humidity_threshold': 85,
        'season'            : [5, 6, 7, 8, 9],
        'risk_level'        : 'Moderate',
        'description'       : (
            'South American leaf blight and Colletotrichum '
            'cause defoliation reducing rubber yield.'
        ),
        'prevention'        : (
            'Apply copper-based fungicide during refoliation. '
            'Ensure proper spacing for air circulation. '
            'Monitor during high humidity periods.'
        ),
    },
    'Oil Palm Bunch Rot': {
        'crops_affected'    : ['Oil Palm'],
        'humidity_threshold': 85,
        'season'            : [6, 7, 8, 9],
        'risk_level'        : 'Moderate',
        'description'       : (
            'Bunch rot caused by Marasmius destroys '
            'fresh fruit bunches reducing palm oil yield.'
        ),
        'prevention'        : (
            'Remove and destroy infected bunches. '
            'Improve drainage around palm base. '
            'Apply fungicide to cut surfaces.'
        ),
    },
}