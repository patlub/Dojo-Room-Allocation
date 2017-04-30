from classes.office import Office
from classes.living_space import LivingSpace
from classes.fellow import Fellow
from classes.staff import Staff
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Union
# from modals.table_def import OfficeModel, LivingSpaceModel, StaffModel, FellowModel
from random import shuffle


class Dojo:
    """
    Dojo class to handle all responsibilities of the dojo
    """

    def __init__(self):
        """
        Initialise lists and dictionaries to to hold data
        for different objects
        """

        self.all_offices = []
        self.fellows_not_allocated_office = []
        self.fellows_not_allocated_living_space = []
        self.staff_not_allocated = []
        self.all_living_spaces = []
        self.all_fellows = []
        self.all_staff = []

    def create_room(self, room_names, room_type):
        """Creates either an office or living space 
           depending on the room_type passed 
        """
        if not isinstance(room_names, list) or not isinstance(room_type, str):
            raise TypeError('Arguments should be a list and string')

        elif not room_names:
            raise ValueError('List of room names can not be empty')

        else:
            rooms = self.all_offices + self.all_living_spaces
            for room_name in room_names:
                for room in rooms:
                    if room_name == room.name:
                        return 'Room name already exists'

            if room_type == 'office':
                for room_name in room_names:
                    office = Office(room_name)
                    self.all_offices.append(office)

            elif room_type == 'living_space':
                for room_name in room_names:
                    living_space = LivingSpace(room_name)
                    self.all_living_spaces.append(living_space)
            else:
                return ('Invalid room type')

    def add_fellow(self, name, WANTS_ACCOMODATION='N'):
        """Adds fellow to an office and or living space"""

        fellow = Fellow(name)
        available_office = self.get_available_office()

        if available_office:
            self.add_person_to_room(fellow, available_office)
            fellow.office = available_office
        else:
            self.fellows_not_allocated_office.append(fellow)

        if (WANTS_ACCOMODATION == 'Y'):
            available_living_space = self.get_available_living_spaces()

            if available_living_space:
                self.add_person_to_room(fellow, available_living_space)
                fellow.living_place = available_living_space
            else:
                self.fellows_not_allocated_living_space.append(fellow)

        # Append fellow to list of fellows
        self.all_fellows.append(fellow)
        return fellow

    def add_staff(self, name):
        """ Add staff to an office"""

        staff = Staff(name)
        available_office = self.get_available_office()

        # If there is a free office
        if available_office:
            self.add_person_to_room(staff, available_office)
            staff.office = available_office
        else:
            self.staff_not_allocated.append(staff)
        self.all_staff.append(staff)
        return staff

    def get_available_office(self) -> Union[bool, Office]:
        """Check if offices still have available spaces
        """
        shuffle(self.all_offices)
        for office in self.all_offices:
            if office.contains_space():
                return office
        return False

    def add_person_to_room(self, person, room):
        room.occupants.append(person)
        room.spaces -= 1

    def get_available_living_spaces(self) -> Union[bool, Office]:
        """Check if living space still has available space"""
        shuffle(self.all_living_spaces)
        for living_spaces in self.all_living_spaces:
            if living_spaces.contains_space():
                return living_spaces
        return False

    def print_room(self, room_name):
        """Print names of people in room 
           on the screen 
        """
        if not isinstance(room_name, str):
            raise TypeError('Room name should be a string')

        elif not room_name:
            return ('Room name can not be empty')

        else:
            rooms = self.all_offices + self.all_living_spaces
            for room in rooms:
                if room.name == room_name:
                    print('-------------' + room_name + '-------------')
                    for person in room.occupants:
                        print(person.name)

    def print_allocations(self):
        """Print space allocations to screen"""
        text = self.allocations_text()
        print(text)

    def print_allocations_to_file(self, filename):
        """Print space allocations to file"""
        filename = '../files/' + filename
        file = open(filename, 'w')
        text = self.allocations_text()
        file.write(text)
        file.close()

    def allocations_text(self):
        rooms = self.all_offices + self.all_living_spaces
        text = ''
        for room in rooms:
            text += room.name.upper() + '\n'
            text += '---------------------------------------------\n'
            occupants_list = room.occupants
            for person in occupants_list:
                text += (person.name) + ', '
            text += '\n\n'
        return text

    def print_un_allocations(self):
        """Print spaces not allocated to screen"""
        text = self.un_allocations_text()
        print(text)

    def un_allocations_text(self):
        text = ''
        for fellow in self.fellows_not_allocated_office:
            text += fellow.name.upper() + ', Fellow Unallocated Office\n'

        for fellow in self.fellows_not_allocated_living_space:
            text += fellow.name.upper() + ', Fellow Unallocated living space\n'

        for fellow in self.staff_not_allocated:
            text += fellow.name.upper() + ', Staff Unallocated Office\n'

        return text

    def print_un_allocations_to_file(self, filename):
        """Print spaces not allocated to file"""
        filename = '../files/' + filename

        file = open(filename, 'w')
        text = self.un_allocations_text()
        file.write(text)
        file.close()

    def re_allocate_person(self, person_name, room_name):
        """Reallocates person from current room to new room"""
        room = self.get_room(room_name)
        if (room):
            person = self.get_person(person_name)
            if (person):
                if isinstance(room, Office):
                    self.re_allocate_to_office(person, room)
                elif isinstance(room, LivingSpace):
                    if isinstance(person, Fellow):
                        self.re_allocate_to_living_space(person, room)
                    else:
                        return 'Cant Re-allocate staff to a living room'
            else:
                return 'Person with name ' + person_name + ' does not exist'
        else:
            return 'Room with name ' + room_name + ' does not exist'

    def re_allocate_to_office(self, person, room):
        person.office.occupants.remove(person)
        person.office.spaces -= 1
        room.occupants.append(person)
        person.office = room

    def re_allocate_to_living_space(self, person, room):
        person.living_place.occupants.remove(person)
        person.living_place.spaces -= 1
        room.occupants.append(person)
        person.office = room

    def get_person(self, name):
        persons = self.all_fellows + self.all_staff
        for person in persons:
            if person.name == name:
                return person
        return False

    def get_room(self, room_name):
        rooms = self.all_offices + self.all_living_spaces
        for room in rooms:
            if room.name == room_name:
                return room
        return False

    def load_people(self, file_path):
        """Loads people from text file"""
        with open(file_path) as fp:
            for line in fp:
                words = line.split()
                name = words[0] + ' ' + words[1]
                if words[2] == 'FELLOW':
                    if words[3] == 'Y':
                        self.add_fellow(name, 'Y')
                    else:
                        self.add_fellow(name)
                elif words[2] == 'STAFF':
                    self.add_staff(name)

    def save_state(self, db=None):
        if db is None:
            engine = create_engine('sqlite:///..\modals\Dojo.db', echo=True)
        else:
            db = db + '.db'
            engine = create_engine('sqlite:///..\modals\\' + db, echo=True)

        # create a Session
        Session = sessionmaker(bind=engine)
        session = Session()

        # Save offices to db
        for office in self.all_offices:
            office_modal = OfficeModel(office.name, office.spaces)
            session.add(office_modal)

        # Save living spaces to db
        for living_space in self.all_living_spaces:
            living_space_modal = LivingSpaceModel(living_space.name, living_space.spaces)
            session.add(living_space_modal)

        # Save staff spaces to db
        for staff in self.all_staff:
            with session.no_autoflush:
                office = session.query(OfficeModel).filter_by(name=staff.office.name).first()
                office_id = office.office_id
                staff_modal = StaffModel(staff.name, office_id)
                session.add(staff_modal)

        # Save fellow to db
        for fellow in self.all_fellows:
            with session.no_autoflush:
                if fellow.office != None:
                    office = session.query(OfficeModel).filter_by(name=fellow.office.name).first()
                    office_id = office.office_id

                # check if fellow living space is None
                if fellow.living_space == None:
                    living_space_id = None
                    fellow_modal = FellowModel(fellow.name, office_id, living_space_id)
                    session.add(fellow_modal)

                else:
                    living_space = session.query(LivingSpaceModel).filter_by(name=fellow.living_space.name).first()
                    living_space_id = living_space.id
                    fellow_modal = FellowModel(fellow.name, office_id, living_space_id)
                    session.add(fellow_modal)
        # commit the record the database
        session.commit()

    def load_state(self, db=None):
        if db is None:
            engine = create_engine('sqlite:///..\modals\Dojo.db', echo=True)
        else:
            db = db + '.db'
            engine = create_engine('sqlite:///..\modals\\' + db, echo=True)

        # create a Session
        Session = sessionmaker(bind=engine)
        session = Session()

        # Loads offices from the databe
        for office in session.query(OfficeModel).order_by(OfficeModel.id):
            new_office = Office(office.name)
            new_office.spaces = office.spaces
            self.all_offices.append(new_office)

        # Loads living spaces from the database
        for living_space in session.query(LivingSpaceModel).order_by(LivingSpaceModel.id):
            new_living_space = LivingSpace(living_space.name)
            new_living_space.spaces = living_space.spaces
            self.all_living_spaces.append(new_living_space)

        # Loads staff from the database
        for staff in session.query(StaffModel).order_by(StaffModel.id):
            # Create new Staff Object from database details
            new_staff = Staff(staff.name)
            office_id = staff.office_id

            # Create new office using databsse office details
            office = session.query(OfficeModel).filter_by(id=office_id).first()
            office_name = office.name
            new_office = Office(office_name)

            # Append new office to list of office objects
            new_staff.office = new_office
            self.all_staff.append(new_staff)

        # Loads fellows from the database
        for fellow in session.query(FellowModel).order_by(FellowModel.id):
            # Create new fellow Object from database details
            new_fellow = Fellow(fellow.name)
            office_id = fellow.office_id
            living_space_id = fellow.living_space_id

            # Create new office using databsse office details
            office = session.query(OfficeModel).filter_by(id=office_id).first()
            office_name = office.name
            new_office = Office(office_name)

            # Create new living space using databsse office details
            living_space = session.query(LivingSpaceModel).filter_by(id=living_space_id).first()
            living_space_name = living_space.name
            new_living_space = LivingSpace(living_space_name)

            # Append new office to list of office objects
            new_fellow.office = new_office
            new_fellow.living_place = new_living_space
            self.all_fellows.append(new_fellow)

# dojo = Dojo()
# dojo.create_room(['blue', 'red', 'yellow'], 'office')
# dojo.create_room(['hotel'], 'living_space')
# print(dojo.all_offices)

# dojo.add_fellow('Patrick', 'Y')
# dojo.add_staff('Patrick')
# dojo.add_staff('Trey')
# dojo.add_staff('Dan')
# dojo.add_staff('Ian')
# dojo.add_staff('Ive')
# dojo.add_staff('Ivan')
# dojo.add_staff('Ivee')
# dojo.add_fellow('Jim', 'Y')
# dojo.add_fellow('Moses', 'Y')
# dojo.add_fellow('Becky', 'Y')
# dojo.add_fellow('Sebu')
# dojo.add_fellow('Fred', 'Y')
# dojo.add_fellow('Samuel', 'Y')
# dojo.add_fellow('Dona', 'Y')
# print(dojo.print_allocations())
# dojo.print_room('blue')
# dojo.print_allocations_to_file('hey.txt')
# dojo.print_un_allocations()
# dojo.print_un_allocations_to_file('unalloc')
# dojo.get_office('hi')
# dojo.re_allocate_person('Patrick', 'Yellow')
# dojo.save_state()
