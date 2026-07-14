from fastapi import APIRouter
from app.services.model_service import model_service
from app.services.climatology_service import climatology_service

router = APIRouter(prefix='/health', tags=['Health'])


@router.get('/')
def health_check():
    return {
        'status': 'ok',
        'api': 'AgriSense',
        'model_loaded': model_service.is_loaded,
        'climatology_loaded': climatology_service.is_loaded,
        'model': 'CatBoost Multivariate (cat_mul_new.cbm)',
    }