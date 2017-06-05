"""
Table Definitions for Dojo objects
"""
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


# engine = create_engine('sqlite:///..\modals\Dojo.db', echo=True)
engine = create_engine('sqlite:///Dojo.db', echo=True)
Base = declarative_base()


class OfficeModel(Base):
    """
    DB model for office object
    """
    __tablename__ = "office"

    office_id = Column(Integer, primary_key=True)
    name = Column(String)
    spaces = Column(Integer)

    # ----------------------------------------------------------------------
    def __init__(self, name, spaces):
        """
        Attributes
        :param name: 
        :param spaces: 
        """
        self.name = name
        self.spaces = spaces


class LivingSpaceModel(Base):
    """
    DB modal for LivingSpace object
    """
    __tablename__ = "living_space"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    spaces = Column(Integer)

    def __init__(self, name, spaces):
        """
        Attributes
        :param name: 
        :param spaces: 
        """
        self.name = name
        self.spaces = spaces


class StaffModel(Base):
    """
    DB modal for Staff object
    """
    __tablename__ = "staff"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    office = Column(String(25))

    def __init__(self, name, office):
        """
        Attributes
        :param name: 
        :param office_id: 
        """
        self.name = name
        self.office = office


class FellowModel(Base):
    """
    DB modal for Fellow object
    """
    __tablename__ = "fellow"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    office = Column(String(25))
    living_space = Column(String(25))
    wants_accomodation = Column(String(2))

    def __init__(self, name, office, living_space, wants_accomadation):
        """
        Attributes
        :param name: 
        :param office_id: 
        :param living_space_id: 
        """
        self.name = name
        self.office = office
        self.living_space = living_space
        self.wants_accomodation = wants_accomadation


# create tables
Base.metadata.create_all(engine)
