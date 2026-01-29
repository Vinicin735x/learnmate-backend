from fastapi import FastAPI

app = FastAPI(
    title='Learnmate API',
    description='API para plataforma de estudos personalizados com IA',
    version='0.1.0'
)

@app.get('/health')
def healt_check():
    return {
        'status': 'active',
        'service': 'LearnMate API',
        'version': '0.1.0'
    }

@app.get('/')
def read_root():
    return {'message': 'Bem-vindo à API do LearnMate! Acesse /docs para ver a documentação.'}