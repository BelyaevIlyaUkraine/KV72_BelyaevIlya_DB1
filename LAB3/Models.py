from sqlalchemy import Column, Integer, Text, Boolean, ForeignKey,TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship,backref

Base = declarative_base()


class Network(Base):
    __tablename__ = "Network"

    Name = Column(Text, primary_key=True)
    Owner = Column(Text)


class Film(Base):
    __tablename__ = "Film"

    ID = Column(Integer, primary_key=True)
    Name = Column(Text)
    Genre = Column(Text)
    Year = Column(Text)
    Budget = Column(Text)
    Country = Column(Text)
    Duration = Column(Text)
    Oscar = Column(Boolean)


class Session(Base):
    __tablename__ = "Session"

    ID = Column(Integer,primary_key=True)
    Start = Column(TIMESTAMP)
    Film = Column(Integer,ForeignKey("Film.ID"))
    HallNumber = Column(Text)

    film_ref = relationship("Film",backref=backref("sessions"))

    cinemas = relationship("Cinema",secondary="Cinema-Session")


class Cinema(Base):
    __tablename__ = "Cinema"

    Network = Column(Text)
    Address = Column(Text,primary_key=True)
    NumberOfHalls = Column(Text)
    GenNumberOfHalls = Column(Text)

    networks = relationship("Network",backref=backref("cinemas"))

    sessions = relationship("Cinema",secondary = "Cinema-Session")


class CinemaSession(Base):
    __tablename__ = "Cinema-Session"

    ID = Column(Integer,primary_key=True)
    CinemaID = Column(Text,ForeignKey("Cinema.CinemaID"))
    SessionID = Column(Integer,ForeignKey("Session.SessionID"))



