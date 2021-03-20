from sqlalchemy import Column, Integer, String, UniqueConstraint, ForeignKey, Date, Enum,  Time, DateTime, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

def clamp(number, upper_bound, lower_bound):
  return max(lower_bound,min(upper_bound,number))


class Penguin(Base):
    __tablename__ = 'Penguin'

    PenguinID = Column(Integer, primary_key=True)
    FirstName = Column(VARCHAR(255))
    LastName = Column(VARCHAR(255))
    Birthday = Column(Date)
    District = Column(Integer)
    VaccineNumber = Column(Integer)
    PenguinPriority = Column(Integer)
 

    def __repr__(self) -> str:
        return f'{self.FirstName}: {self.LastName}'

class VaccinationCenter(Base):
    __tablename__ = 'VaccinationCenter'

    CenterID = Column(Integer, primary_key=True)
    District = Column(Integer)
    WorkFrom = Column(DateTime)
    WorkTill = Column(DateTime)
    FreeVaccines = Column(Integer)
 

    def __repr__(self) -> str:
        return str(self.CenterID)

class ValidCenters(Base):
    __tablename__ = 'ValidCenters'

    PenguinID = Column(Integer,ForeignKey(Penguin.PenguinID), primary_key=True)
    CenterID = Column(Integer, ForeignKey(VaccinationCenter.CenterID), primary_key=True)

    def __repr__(self) -> str:
        return f'{self.PenguinID}: {self.CenterID}'

class ValidTimes(Base):
    __tablename__ = 'ValidTimes'

    PenguinID = Column(Integer,ForeignKey(Penguin.PenguinID), primary_key=True)
    Day = Column(Integer, primary_key=True)
    From = Column(Time)
    To = Column(Time)

    self.Day = clamp(Day, 6, 0)

    def __repr__(self) -> str:
        return f'{self.PenguinID}: {self.Day} , from: {self.From} , to: {self.To}'

class WaitingList(Base):
    __tablename__ = 'WaitingList'
    
    RegistrationID = Column(Integer, primary_key=True)
    PenguinID = Column(Integer,ForeignKey(Penguin.PenguinID))

    def __repr__(self) -> str:
        return f'{self.RegistrationID}: {self.PenguinID}'

class TimeTable(Base):
    __tablename__ = 'TimeTable'
    
    RegistrationID = Column(Integer, primary_key=True)
    VaccinationCenterID = Column(Integer, ForeignKey(VaccinationCenter.CenterID))
    Time = Column(DateTime)
    PenguinID = Column(Integer,ForeignKey(Penguin.PenguinID))

    def __repr__(self) -> str:
        return f'{self.RegistrationID}: {self.PenguinID}, {self.VaccinationCenterID}, {self.Time}'

class VaccinationLog(Base):
    __tablename__ = 'VaccinationLog'
    
    RegistrationID = Column(Integer, primary_key=True)
    PenguinID = Column(Integer,ForeignKey(Penguin.PenguinID))
    VaccinationNumber = Column(Integer)
    VaccinationCenter = Column(Integer, ForeignKey(VaccinationCenter.CenterID))
    VaccinationTime = Column(DateTime)

    def __repr__(self) -> str:
        return (f'{self.RegistrationID}: {self.PenguinID},'
                f' Vaccine number: {self.VaccinationNumber}, Center: {self.VaccinationCenter},'
                f'At: {self.VaccinationTime}')
