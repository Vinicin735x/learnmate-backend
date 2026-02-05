import os 
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from openai import AsyncOpenAI
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from models import Summary
from sqlalchemy import select
from typing import List
from datetime import datetime

load_dotenv()
client = AsyncOpenAI(
    api_key=os.environ.get('GROQ_API_KEY'),
    base_url='https://api.groq.com/openai/v1'
)

app = FastAPI(
    title='LearnMate API', 
    version='0.1.0',
    description='Backend para processamento de resumos e trilhas de estudo utilizando Llama 3 via Groq.',
    contact={
        'name': 'Vinícius Castelhano Mantovani'
    }
    )


class SummarySchema(BaseModel):
    id: int
    summary_text: str
    created_at: datetime

    class Config:
        from_attributes = True 

class SummarizeRequest(BaseModel):
    text: str = Field(..., min_length=50, description='O texto completo a ser resumido')
    language: str = Field('pt-br', description='O idioma desejado para o resumo')

    class Config:
        schema_extra = {
            'example': {
                'content': 'O Event Loop do Python é o núcleo central que gerencia tarefas assíncronas...'
            }
        }

class SummarizeResponse(BaseModel):
    summary: str
    original_length: int
    summary_length: int

    model_config = {"from_attributes": True}

@app.get('/healt', tags=['System'])
def health_check():
    '''
    Verifica se a API está online e respondendo
    '''
    return {'statys': 'active'}

@app.get('/summaries', response_model=List[SummarizeResponse], tags=['History'])
async def get_all_summaries(
    limit: int = 10,
    offset: int = 0,
    db: AsyncSession = Depends(get_db)
):
    '''
    Retorna o histórico de resumos gerados com paginação simples.
    '''
    query = select(Summary).order_by(Summary.created_at.desc()).offset(offset).limit(limit)
    result = await db.execute(query)
    summaries = result.scalars().all()

    return [
        SummarizeResponse(
            summary=s.summary_text,
            original_length=len(s.original_content),
            summary_length=len(s.summary_text)
        ) for s in summaries
    ]

@app.get('/summaries/{summary_id}', response_model=SummarizeResponse, tags=['History'])
async def get_summary_by_id(
    summary_id: int,
    db:AsyncSession = Depends(get_db)
):
    '''
    Busca um resumo específico no banco de dados pelo ID.
    Utiliza o método select() do SQLAlchemy 2.0 para uma query assíncrona
    '''
    query = select(Summary).where(Summary.id == summary_id)
    result = await db.execute(query)

    db_summary = result.scalars().first()

    if not db_summary:
        raise HTTPException(status_code=404, detail='Resumo não encontrado.')
    
    return SummarizeResponse(
        summary=db_summary.summary_text,
        original_length=len(db_summary.original_content),
        summary_length=len(db_summary.summary_text)
    )

@app.delete('/summaries/{summary_id}', status_code=204, tags=['History'])
async def delete_summary(
    summary_id: int,
    db: AsyncSession = Depends(get_db)
):
    '''
    Remove um resumo do banco de dados permanentemente
    '''
    query = select(Summary).where(Summary.id == summary_id)
    result = await db.execute(query)
    db_summary = result.scalars().first()

    if not db_summary:
        raise HTTPException(status_code=404, detail='Resumo não encontrado.')
    
    await db.delete(db_summary)
    await db.commit()

    return None

@app.post('/summarize', response_model=SummarizeResponse, tags=['AI Features'], status_code=201)
async def summarize_content(
    request: SummarizeRequest,
    db: AsyncSession = Depends(get_db)
    ):
    '''
    Gera um resumo estruturado e persiste os dados no PostgreSQL.
    
    - **text**: Texto de entrada (mínimo 50 caracteres).
    - **language**: Idioma de saída (padrão: pt-br).
    
    Retorna o resumo, o tamanho original e o tamanho do resumo.
    '''
    if not request.text:
        raise HTTPException(status_code=400, detail= 'O texto não pode estar vazio')
    
    try:
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

        new_summary = Summary(
            original_content=request.text,
            summary_text=summary_text
        )

        db.add(new_summary)
        await db.commit()
        await db.refresh(new_summary)

        return SummarizeResponse(
            summary=summary_text,
            original_length=len(request.text),
            summary_length=len(summary_text)
        )
    except Exception as e:
        await db.rollback()
        print(f'Erro na OpenAI: {e}')
        raise HTTPException(status_code=500, detail=f'ERRO REAL: {type(e).__name__} - {str(e)}')