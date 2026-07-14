import logging
from pathlib import Path
from catboost import CatBoostRegressor
from app.config import settings

logger = logging.getLogger(__name__)

FEATURE_COLS = [
    'month',
    'quarter',
    'year',
    'is_dry_season',
    'is_peak_wet',
    'is_onset_wet',
    'month_sin',
    'month_cos',
    'rain_lag_1',
    'rain_lag_2',
    'rain_lag_3',
    'rain_lag_4',
    'rain_lag_5',
    'rain_lag_6',
    'rain_lag_7',
    'rain_lag_8',
    'rain_lag_9',
    'rain_lag_10',
    'rain_lag_11',
    'rain_lag_12',
    'rain_roll3_mean',
    'rain_roll6_mean',
    'rain_roll3_std',
    'rain_roll3_min',
    'rain_roll3_max',
    'rain_lag_24',       # added this lag and removed the 12
    'month_clim_mean',
    'month_clim_std',
    'rain_anomaly',
    'rain_trend',
    'rain_trend_3',
    'Temperature_Celsius',
    'Relative_Humidity_percent',
    'Solar_Radiation_MJ_m2_per_month',
    'Surface_Pressure_hPa',
]


class ModelService:
    def __init__(self):
        self.model        = None
        self.feature_cols = FEATURE_COLS
        self._loaded      = False

    def load(self):
        model_dir  = Path(settings.MODEL_DIR)
        model_path = model_dir / 'cat_mul_new.cbm'

        if not model_dir.exists():
            raise FileNotFoundError(
                f'Model directory not found: {model_dir}.')
        if not model_path.exists():
            raise FileNotFoundError(
                f'Model file not found: {model_path}.')

        try:
            self.model = CatBoostRegressor()
            self.model.load_model(str(model_path))
            logger.info('CatBoost model loaded successfully.')
        except Exception as e:
            raise RuntimeError(f'Failed to load CatBoost model: {e}')

        self._loaded = True
        logger.info('ModelService fully loaded.')

    def predict(self, X) -> float:
        if not self._loaded:
            raise RuntimeError('Model not loaded. Call load() first.')
        try:
            pred = float(self.model.predict(X)[0])
            return max(pred, 0.0)
        except Exception as e:
            raise RuntimeError(f'Prediction failed: {e}')

    @property
    def is_loaded(self) -> bool:
        return self._loaded


model_service = ModelService()