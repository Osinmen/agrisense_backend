import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.config import settings
from app.routers import forecast, crops, health
from app.services.model_service import model_service
from app.services.climatology_service import climatology_service

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s  %(levelname)s  %(name)s  %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info('AgriSense API starting up ...')
    try:
        model_service.load()
        climatology_service.load()
        logger.info('All services loaded. API is ready.')
    except FileNotFoundError as e:
        logger.error(f'Startup failed - file not found: {e}')
        raise
    except RuntimeError as e:
        logger.error(f'Startup failed - runtime error: {e}')
        raise
    except Exception as e:
        logger.error(f'Startup failed - unexpected error: {e}')
        raise
    yield
    logger.info('AgriSense API shutting down.')


app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description='AgriSense - Rainfall forecasting and crop advisory API for Ondo State Nigeria.',
    lifespan=lifespan,
)

app.include_router(health.router)
app.include_router(forecast.router)
app.include_router(crops.router)


@app.get('/')
def root():
    return {
        'api': 'AgriSense',
        'version': settings.API_VERSION,
        'status': 'running',
        'docs': '/docs',
        'endpoints': {
            'health': '/health/',
            'forecast': '/forecast/',
            'crops': '/crops/',
        }
    }

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)