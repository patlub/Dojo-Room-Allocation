from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# engine = create_engine('sqlite:///..\modals\Dojo.db', echo=True)
engine = create_engine('sqlite:///Dojo.db', echo=True)
Base = declarative_base()

########################################################################
class OfficeModel(Base):
    """"""
    __tablename__ = "office"

    office_id = Column(Integer, primary_key=True)
    name = Column(String)
    spaces = Column(Integer)


    # ----------------------------------------------------------------------
    def __init__(self, name, spaces):
        """"""
        self.name = name
        self.spaces = spaces

########################################################################
class LivingSpaceModel(Base):
    """"""
    __tablename__ = "living_space"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    spaces = Column(Integer)


    # ----------------------------------------------------------------------
    def __init__(self, name, spaces):
        """"""
        self.name = name
        self.spaces = spaces

########################################################################
class StaffModel(Base):
    """"""
    __tablename__ = "staff"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    office_id = Column('office_id', Integer, ForeignKey('office.office_id'), nullable=True)

    # office = relationship('Office')


    # ----------------------------------------------------------------------
    def __init__(self, name, office_id):
        """"""
        self.name = name
        self.office_id = office_id

    ########################################################################
class FellowModel(Base):
    """"""
    __tablename__ = "fellow"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    office_id = Column('office_id', Integer, ForeignKey('office.office_id'), nullable=True)
    living_space_id = Column('living_space_id', Integer, ForeignKey('living_space.id'), nullable=True)

    # office = relationship('Office')


    # ----------------------------------------------------------------------
    def __init__(self, name, office_id, living_space_id):
        """"""
        self.name = name
        self.office_id = office_id
        self.living_space_id = living_space_id


# create tables
Base.metadata.create_all(engine)