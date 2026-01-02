from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class TestModel(Base):
    __tablename__ = 'test_model'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))

print("Model defined successfully")
print(f"Table name: {TestModel.__tablename__}")
print(f"Primary key: {TestModel.__table__.primary_key}")
