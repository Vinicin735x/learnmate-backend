from pydantic import BaseModel, Field
from datetime import datetime

class SummarySchema(BaseModel):
    id: int
    summary_text: str
    created_at: datetime

    # Pydantic V2: Permite ler dados de objetos ORM do SQLAlchemy
    model_config = {"from_attributes": True}

class SummarizeRequest(BaseModel):
    text: str = Field(..., min_length=50, description='O texto completo a ser resumido')
    language: str = Field('pt-br', description='O idioma desejado para o resumo')

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'text': 'O Event Loop do Python é o núcleo central que gerencia tarefas assíncronas...',
                    'language': 'pt-br'
                }
            ]
        }
    }

class SummarizeResponse(BaseModel):
    summary: str
    original_length: int
    summary_length: int

    model_config = {"from_attributes": True}