from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL=os.getenv('DATABASE_URL')

# SQLALCHEMY_DATABASE_URL = "postgres://upjumigwrlyrft:c97ced32104ca7965b303eb9d0e728aae7d755c9975e38d8ee9e86e5e4a53e25@ec2-54-157-234-29.compute-1.amazonaws.com:5432/dbgm4vp87c40j8"

engine = create_engine(
    # SQLALCHEMY_DATABASE_URL,connect_args={'client_encoding': 'utf8'}
    DATABASE_URL,connect_args={'client_encoding': 'utf8'}
)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()