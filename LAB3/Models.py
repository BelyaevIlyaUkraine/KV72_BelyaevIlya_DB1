from sqlalchemy import Column, Integer, Text, BOOLEAN,ForeignKey,TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship,backref

Base = declarative_base()


class Network(Base):
    __tablename__ = "Network"

    Name = Column(Text,primary_key=True)
    Owner = Column(Text)

    def __str__(self):
        return "({},{})\n".format(self.Name,self.Owner)

    def __repr__(self):
        return str(self)


class Cinema(Base):
    __tablename__ = "Cinema"

    Network = Column(Text,ForeignKey('Network.Name'))
    Address = Column(Text,primary_key=True)
    NumberOfHalls = Column(Text)
    GenNumberOfSeats = Column(Text)

    #network = relationship("Network",backref=backref("cinemas"))
    #sessn = relationship("Session",secondary = "Cinema-Session")

    def __str__(self):
        return "({},{},{},{})\n".format(self.Network,self.Address,self.NumberOfHalls,self.GenNumberOfSeats)

    def __repr__(self):
        return str(self)



class Film(Base):
    __tablename__ = "Film"

    ID = Column(Integer, primary_key=True)
    Name = Column(Text)
    Genre = Column(Text)
    Year = Column(Text)
    Budget = Column(Text)
    Country = Column(Text)
    Duration = Column(Text)
    Oscar = Column(BOOLEAN)

    def __str__(self):
        return "({},{},{},{},{},{},{},{})\n".format(self.ID,self.Name,self.Genre,self.Year,self.Budget,self.Country,
                                                  self.Duration,self.Oscar)

    def __repr__(self):
        return str(self)


class Session(Base):
    __tablename__ = "Session"

    ID = Column(Integer,primary_key=True)
    Start = Column(TIMESTAMP)
    Film = Column(Integer,ForeignKey('Film.ID'))
    HallNumber = Column(Text)

    def __str__(self):
        return "({},{},{},{})\n".format(self.ID,self.Start,self.Film,self.HallNumber)

    def __repr__(self):
        return str(self)

    #film = relationship("Film", backref=backref("sessions"))
    #cinem = relationship("Cinema",secondary = "Cinema-Session")


class Cinema_Session(Base):
    __tablename__ = "Cinema-Session"

    ID = Column(Integer,primary_key = True)
    CinemaID = Column(Text,ForeignKey('Cinema.Address'))
    SessionID = Column(Integer,ForeignKey('Session.ID'))

    def __str__(self):
        return "({},{},{})\n".format(self.ID,self.CinemaID,self.SessionID)
