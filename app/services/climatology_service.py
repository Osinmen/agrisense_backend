import pandas as pd
import logging
from pathlib import Path
from app.config import settings
from app.utils.helpers import get_climatology

logger = logging.getLogger(__name__)


class ClimatologyService:
    def __init__(self):
        self.historical_df = None
        self.climatology = None
        self._loaded = False

    def load(self):
        data_path = Path(settings.HISTORICAL_DATA_PATH)

        if not data_path.exists():
            raise FileNotFoundError(
                f'Historical data not found: {data_path}. '
                f'Place ondo_climate_merged.csv inside app/data/.'
            )

        try:
            self.historical_df = pd.read_csv(str(data_path))
            self.historical_df[settings.DATE_COL] = pd.to_datetime(
                self.historical_df[settings.DATE_COL]
            )
            self.historical_df = self.historical_df.sort_values(
                settings.DATE_COL
            ).reset_index(drop=True)
            logger.info(
                f'Historical data loaded: {len(self.historical_df)} rows'
            )
        except Exception as e:
            raise RuntimeError(f'Failed to load historical data: {e}')

        try:
            self.climatology = get_climatology(
                self.historical_df,
                settings.DATE_COL,
                settings.EXOG_FEATURES
            )
            logger.info('Monthly climatology computed.')
        except Exception as e:
            raise RuntimeError(f'Failed to compute climatology: {e}')

        self._loaded = True

    def get_rainfall_history(self) -> list:
        if not self._loaded:
            raise RuntimeError('ClimatologyService not loaded.')
        return self.historical_df[settings.TARGET_COL].values.tolist()

    def get_exog_for_month(self, calendar_month: int) -> dict:
        if not self._loaded:
            raise RuntimeError('ClimatologyService not loaded.')
        if calendar_month not in self.climatology.index:
            raise ValueError(
                f'No climatology data for month {calendar_month}.'
            )
        row = self.climatology.loc[calendar_month]
        return {feat: round(float(row[feat]), 4)
                for feat in settings.EXOG_FEATURES}

    def get_last_date(self):
        if not self._loaded:
            raise RuntimeError('ClimatologyService not loaded.')
        return self.historical_df[settings.DATE_COL].max()

    @property
    def is_loaded(self) -> bool:
        return self._loaded


climatology_service = ClimatologyService()