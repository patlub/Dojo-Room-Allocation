from classes.room import Office, LivingSpace, Fellow, Staff
from modals.table_def import OfficeModel, FellowModel, StaffModel, LivingSpaceModel
from modals.table_def import engine
from random import shuffle
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Union


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
                if not rooms:
                    self.create_an_office_or_a_living_space(room_type, room_name)
                    rooms = self.all_offices + self.all_living_spaces

                else:
                    if (self.is_room_exists(room_name)):
                        print('Room with name ' + room_name + ' Already exists')
                    else:
                        self.create_an_office_or_a_living_space(room_type, room_name)

    def is_room_exists(self, room_name):
        """
        Check if room with name, room_name already exists
        :param room_name: 
        :return boolean: 
        """
        rooms = self.all_offices + self.all_living_spaces
        for room in rooms:
            if room_name == room.name:
                return True
        return False

    def create_an_office_or_a_living_space(self, room_type, room_name):
        """
        Creates a room of type room_type with a specified name room_name
        :param room_type: 
        :param room_name: 
        :return: 
        """
        if room_type == 'office':
            office = Office(room_name)
            self.all_offices.append(office)
            print('-------------Office ' + room_name + ''
                                                       ' has been created----------------')

        elif room_type == 'living_space':
            living_space = LivingSpace(room_name)
            self.all_living_spaces.append(living_space)
            print('-------------Living space ' + room_name + ''
                                                             ' has been created----------------')

        else:
            print('Invalid room type')

    def add_fellow(self, name, WANTS_ACCOMODATION='N'):
        """
        Adds fellow to an office and or living space
        :param name: 
        :param WANTS_ACCOMODATION: 
        :return: 
        """

        fellow = Fellow(name)
        available_office = self.get_available_office()

        if available_office:
            self.add_person_to_room(fellow, available_office)
            fellow.office = available_office
            print('----------------Fellow ' + name + ' '
                                                     'has been added to office ' + available_office.name)
        else:
            self.fellows_not_allocated_office.append(fellow)
            print('----------------Fellow ' + name + ''
                                                     ' is currently unallocated office')

        if (WANTS_ACCOMODATION == 'Y'):
            available_living_space = self.get_available_living_spaces()

            if available_living_space:
                self.add_person_to_room(fellow, available_living_space)
                fellow.living_place = available_living_space
                print(
                    '----------------Fellow ' + name + ' '
                                                       'has been added to Living space '
                    + available_living_space.name)

            else:
                self.fellows_not_allocated_living_space.append(fellow)
                print('----------------Fellow ' + name + ''
                                                         ' is currently unallocated Living space')

        # Append fellow to list of fellows
        self.all_fellows.append(fellow)
        return fellow

    def add_staff(self, name):
        """
        Add staff to an office
        :param name: 
        :return: 
        """

        staff = Staff(name)
        available_office = self.get_available_office()

        # If there is a free office
        if available_office:
            self.add_person_to_room(staff, available_office)
            staff.office = available_office
            print('----------------Staff ' + name + ' '
                                                    'has been added to office ' + available_office.name)
        else:
            self.staff_not_allocated.append(staff)
            print('----------------Staff ' + name + ' '
                                                    'is currently unallocated due to unavailable Living space')

        self.all_staff.append(staff)
        return staff

    def get_available_office(self) -> Union[bool, Office]:
        """
        Check if offices still have available spaces
        :return: 
        """
        shuffle(self.all_offices)
        for office in self.all_offices:
            if office.contains_space():
                return office
        return False

    def add_person_to_room(self, person, room):
        """
        Adds a person to a room
        :param person: 
        :param room: 
        :return: 
        """
        room.occupants.append(person)
        room.spaces -= 1

    def get_available_living_spaces(self) -> Union[bool, LivingSpace]:
        """
        Check if living space still has available space
        :return: 
        """
        shuffle(self.all_living_spaces)
        for living_space in self.all_living_spaces:
            if living_space.contains_space():
                return living_space
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
                    if not room.occupants:
                        print('Room is currently empty')
                        return None
                    else:
                        for person in room.occupants:
                            print(person.name)
                        return None
            print('Room ' + room_name + ' does not exist')

    def print_allocations(self):
        """Print space allocations to screen"""
        text = self.allocations_text()
        if not text:
            print('No persons are currently allocated rooms')
        else:
            print(text)

    def print_allocations_to_file(self, filename):
        """Print space allocations to file"""
        filename = '../files/' + filename
        file = open(filename, 'w')
        text = self.allocations_text()
        file.write(text)
        file.close()

    def allocations_text(self):
        """
        generates text of all room allocations
        :return: 
        """
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
        if not text:
            print('No persons are currently not allocated rooms')
        else:
            print(text)

    def un_allocations_text(self):
        """
        geaerates text of people not allocated room space
        :return: 
        """
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
        """
        Reallocates person from current room to new room
        :param person_name: 
        :param room_name: 
        :return: 
        """
        room = self.get_room(room_name)
        if (room):
            person = self.get_person(person_name)

            if (person):
                if isinstance(room, Office):
                    if person.office == room:
                        return person_name + ' is already in room ' + room_name
                    self.re_allocate_to_office(person, room)
                    return person_name + ' has been reallocated to Office ' + room_name

                elif isinstance(room, LivingSpace):
                    if isinstance(person, Fellow):
                        if person.living_place == room:
                            return person_name + ' is already in room ' + room_name
                        self.re_allocate_to_living_space(person, room)
                        return person_name + ' has been reallocated to Living Space ' + room_name

                    else:
                        return 'Cant Re-allocate staff to a living room'
            else:
                return 'Person with name ' + person_name + ' does not exist'
        else:
            return 'Room with name ' + room_name + ' does not exist'

    def re_allocate_to_office(self, person, room):
        """
        Re-allocates a person to an office
        :param person: 
        :param room: 
        :return: 
        """

        persons_not_allocated = self.fellows_not_allocated_office + self.staff_not_allocated
        if person not in persons_not_allocated:
            person.office.occupants.remove(person)
            person.office.spaces -= 1
        else:
            if isinstance(person, Fellow):
                self.fellows_not_allocated_office.remove(person)
            else:
                self.staff_not_allocated.remove(person)

        room.occupants.append(person)
        person.office = room

    def re_allocate_to_living_space(self, person, room):
        """
        Re-allocates a person to a living space
        :param person: 
        :param room: 
        :return: 
        """
        if person not in self.fellows_not_allocated_living_space:
            person.living_place.occupants.remove(person)
            person.living_place.spaces -= 1
        else:
            self.fellows_not_allocated_living_space.remove(person)

        room.occupants.append(person)
        person.office = room

    def get_person(self, name):
        """
        Gets a person when passed a person's name
        :param name: 
        :return: 
        """
        persons = self.all_fellows + self.all_staff
        for person in persons:
            if person.name == name:
                return person
        return False

    def get_room(self, room_name):
        """
        Gets a room when passed a room name
        :param room_name: 
        :return: 
        """
        rooms = self.all_offices + self.all_living_spaces
        for room in rooms:
            if room.name == room_name:
                return room
        return False

    def load_people(self, file_path):
        """Loads people from text file"""
        try:
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
        except:
            print('File not Found')

    def save_state(self, db=None):
        # if db is not None:
        #     db = db + '.db'
        #     engine = create_engine('sqlite:///..\modals\\' + db, echo=True)

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
                    if office:
                        office_id = office.office_id

                # check if fellow living space is None
                if fellow.living_place == None:
                    living_space_id = None
                    fellow_modal = FellowModel(fellow.name, office_id, living_space_id)
                    session.add(fellow_modal)

                else:
                    living_space = session.query(LivingSpaceModel).filter_by(name=fellow.living_place.name).first()
                    if living_space:
                        living_space_id = living_space.id
                        fellow_modal = FellowModel(fellow.name, office_id, living_space_id)
                        session.add(fellow_modal)
        # commit the record the database
        session.commit()

    def load_state(self, db=None):
        # if db is None:
        #     engine = create_engine('sqlite:///..\modals\Dojo.db', echo=True)
        # else:
        #     db = db + '.db'
        #     engine = create_engine('sqlite:///..\modals\\' + db, echo=True)

        # create a Session
        Session = sessionmaker(bind=engine)
        session = Session()

        # Loads offices from the databe
        for office in session.query(OfficeModel).order_by(OfficeModel.office_id):
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
# dojo.create_room(['blue', 'blue', 'blue', 'red'], 'office')
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
