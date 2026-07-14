import pandas as pd
import logging
from pathlib import Path
from app.config import settings
from app.utils.helpers import get_climatology

logger = logging.getLogger(__name__)


class ClimatologyService:
    def __init__(self):
        self.historical_df    = None
        self.climatology      = None
        self.monthly_means    = {}   # month → mean rainfall
        self.monthly_stds     = {}   # month → std rainfall
        self._loaded          = False

    def load(self):
        data_path = Path(settings.HISTORICAL_DATA_PATH)

        if not data_path.exists():
            raise FileNotFoundError(
                f'Historical data not found: {data_path}.')

        try:
            self.historical_df = pd.read_csv(str(data_path))
            self.historical_df[settings.DATE_COL] = pd.to_datetime(
                self.historical_df[settings.DATE_COL]
            )
            self.historical_df = self.historical_df.sort_values(
                settings.DATE_COL
            ).reset_index(drop=True)
            logger.info(
                f'Historical data loaded: {len(self.historical_df)} rows')
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

        # Compute monthly rainfall climatology (mean + std per month)
        try:
            self.historical_df['_month'] = pd.to_datetime(
                self.historical_df[settings.DATE_COL]
            ).dt.month

            self.monthly_means = (
                self.historical_df
                .groupby('_month')[settings.TARGET_COL]
                .mean()
                .to_dict()
            )
            self.monthly_stds = (
                self.historical_df
                .groupby('_month')[settings.TARGET_COL]
                .std()
                .to_dict()
            )
            logger.info('Monthly rainfall climatology (mean/std) computed.')
        except Exception as e:
            raise RuntimeError(
                f'Failed to compute monthly rainfall climatology: {e}')

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
                f'No climatology data for month {calendar_month}.')
        row = self.climatology.loc[calendar_month]
        return {feat: round(float(row[feat]), 4)
                for feat in settings.EXOG_FEATURES}

    def get_monthly_means(self) -> dict:
        if not self._loaded:
            raise RuntimeError('ClimatologyService not loaded.')
        return self.monthly_means

    def get_monthly_stds(self) -> dict:
        if not self._loaded:
            raise RuntimeError('ClimatologyService not loaded.')
        return self.monthly_stds

    def get_last_date(self):
        if not self._loaded:
            raise RuntimeError('ClimatologyService not loaded.')
        return self.historical_df[settings.DATE_COL].max()

    @property
    def is_loaded(self) -> bool:
        return self._loaded


climatology_service = ClimatologyService()