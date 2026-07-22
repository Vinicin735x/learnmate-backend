from fastapi import APIRouter

router = APIRouter(tags=['System'])

@router.get('/health')
async def root_health_check() -> dict:
    '''
    Verifica se a API está online e respondendo.
    '''
    return {'status': 'active'}