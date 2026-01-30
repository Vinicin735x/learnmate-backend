import os 
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()
client = AsyncOpenAI(
    api_key=os.environ.get('GROQ_API_KEY'),
    base_url='https://api.groq.com/openai/v1'
)

app = FastAPI(
    title='LearnMate API', 
    version='0.1.0',
    description='API de assistente de estudos utilizando LLMs para resumo e geração de conteúdo.'
    )


class SummarizeRequest(BaseModel):
    text: str = Field(..., min_length=50, description='O texto completo a ser resumido')
    language: str = Field('pt-br', description='O idioma desejado para o resumo')

class SummarizeResponse(BaseModel):
    summary: str
    original_length: int
    summary_length: int


@app.get('/healt', tags=['System'])
def health_check():
    '''
    Verifica se a API está online e respondendo
    '''
    return {'statys': 'active'}

@app.post('/summarize', response_model=SummarizeResponse, tags=['AI Features'])
async def summarize_content(request: SummarizeRequest):
    '''
    Gera um resumo estruturado de um texto fornecido usando LLMs (Llama 3 via Groq).
    
    - **text**: Texto de entrada (mínimo 50 caracteres).
    - **language**: Idioma de saída (padrão: pt-br).
    
    Retorna o resumo, o tamanho original e o tamanho do resumo.
    '''
    if not request.text:
        raise HTTPException(status_code=400, detail= 'O texto não pode estar vazio')
    
    try:
        #chamada assíncrona para a OpenAI
        response = await client.chat.completions.create(
            model='llama-3.3-70b-versatile',
            messages=[
                {
                    'role': 'system',
                    'content': 'Você é um assistente especialista em didática. Resuma o texto fornecido em tópicos claros e educativos.'
                },
                {
                    'role': 'user',
                    'content': f'Resuma isto em {request.language}:\n\n{request.text}'
                }
            ],
            temperature=0.5,
            max_tokens=300
        )

        summary_text = response.choices[0].message.content

        return SummarizeResponse(
            summary=summary_text,
            original_length=len(request.text),
            summary_length=len(summary_text)
        )
    except Exception as e:
        print(f'Erro na OpenAI: {e}')
        raise HTTPException(status_code=500, detail='Falha ao gerar resumo')