from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MODEL_DIR: str = './trained_models'
    DATA_DIR: str = './app/data'
    HISTORICAL_DATA_PATH: str = './app/data/ondo_climate_merged.csv'
    API_TITLE: str = 'AgriSense'
    API_VERSION: str = '1.0.0'
    DEBUG: bool = True
    TARGET_COL: str = 'Rainfall_mm_per_month'
    DATE_COL: str = 'DATE'
    N_LAGS: int = 6
    EXOG_FEATURES: list = [
        'Temperature_Celsius',
        'Relative_Humidity_percent',
        'Solar_Radiation_MJ_m2_per_month',
        'Surface_Pressure_hPa',
    ]
    MODELLED_TARGETS: list = ['Rainfall_mm_per_month']

    class Config:
        env_file = '.env'


settings = Settings()
