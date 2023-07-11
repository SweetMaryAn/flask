import atexit
from sqlalchemy import Column, String, Integer, DateTime, create_engine, func, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

PG_DSN = 'postgresql://app:1234@127.0.0.1:5431/netology_flask'

engine = create_engine(PG_DSN)

Base = declarative_base()
Session = sessionmaker(bind=engine)

atexit.register(engine.dispose)

class Ad(Base):

    __tablename__ = 'app_ads'

    id = Column(Integer, primary_key=True, autoincrement=True)
    heading = Column(String, nullable=False, unique=True)
    description = Column(Text)
    username = Column(String, nullable=False, index=True)
    creationt_time = Column(DateTime, server_default=func.now())


Base.metadata.create_all(bind=engine)

