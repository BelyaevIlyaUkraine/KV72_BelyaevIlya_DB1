from sqlalchemy import Column, Integer, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Film(Base):
    __tablename__ = "Film"

    ID = Column(Integer, primary_key=True)
    Name = Column(Text)
    Genre = Column(Text)
    Year = Column(Text)
    Budget = Column(Text)
    Country = Column(Text)
    Duration = Column(Text)
    Oscar = Column(Boolean,default=False)



