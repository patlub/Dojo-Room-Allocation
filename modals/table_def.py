from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///Dojo.db', echo=True)
Base = declarative_base()

########################################################################
class OfficeModel(Base):
    """"""
    __tablename__ = "office"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    spaces = Column(Integer)


    # ----------------------------------------------------------------------
    def __init__(self, name):
        """"""
        self.name = name
        self.spaces = None


########################################################################
class LivingSpaceModel(Base):
    """"""
    __tablename__ = "living_space"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    spaces = Column(Integer)


    # ----------------------------------------------------------------------
    def __init__(self, name):
        """"""
        self.name = name
        self.spaces = None

########################################################################
class StaffModel(Base):
    """"""
    __tablename__ = "staff"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    office_id = Column('office_id', Integer, ForeignKey('office.id'), nullable=True)

    # office = relationship('Office')


    # ----------------------------------------------------------------------
    def __init__(self, name):
        """"""
        self.name = name

    ########################################################################
class FellowModel(Base):
    """"""
    __tablename__ = "fellow"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    office_id = Column('office_id', Integer, ForeignKey('office.id'), nullable=True)
    living_space_id = Column('living_space_id', Integer, ForeignKey('living_space.id'), nullable=True)

    # office = relationship('Office')


    # ----------------------------------------------------------------------
    def __init__(self, name):
        """"""
        self.name = name

# create tables
Base.metadata.create_all(engine)