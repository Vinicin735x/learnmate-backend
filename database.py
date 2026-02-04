from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql+asyncpg://user:pass@localhost/learnmate')

engine = create_async_engine(DATABASE_URL, echo=True)

async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

class Base(DeclarativeBase):
    '''
    Classe base para os modelos utilizando o mapeamento delcarativo do SQLAlchemy 2.0.
    '''
    pass

async def get_db():
    '''
    Dependency provider para injetar a sessão nas rotas do FastAPI
    '''
    async with async_session() as session:
        yield session