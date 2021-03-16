from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL=os.getenv('DATABASE_URL')
DATABASE_URL=DATABASE_URL.replace("postgres","postgresql")

engine = create_engine(
    # SQLALCHEMY_DATABASE_URL,connect_args={'client_encoding': 'utf8'}
    DATABASE_URL,connect_args={'client_encoding': 'utf8'}
)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()