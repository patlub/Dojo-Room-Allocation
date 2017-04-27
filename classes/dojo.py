from classes.office import Office
from classes.living_space import LivingSpace
from classes.fellow import Fellow
from classes.staff import Staff
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modals.table_def import OfficeModel
from modals.table_def import LivingSpaceModel
from modals.table_def import StaffModel
from modals.table_def import FellowModel


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
        self.office_allocations = {}
        self.living_space_allocations = {}
        self.fellow_not_allocated_office = []
        self.fellow_not_allocated_living_space = []
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
            # First Check if office name or living_space name exists in list

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

    def add_fellow(self, name, WANTS_ACCOMODATION = 'N'):
        """Adds fellow to an office and or living space"""

        fellow = Fellow(name)
        available_office = self.get_available_office()

        # If there is a free office
        if available_office:
            # if key in dictionary, append to the list in dictionary
            # Otherwise create new key with list
            if available_office.name in self.office_allocations:
                fellows_list = self.office_allocations[available_office.name]
                fellows_list.append(fellow.name)
            else:
                self.office_allocations[available_office.name] = [fellow.name]

            available_office.spaces -= 1
            fellow.office = available_office

        else:
            self.fellow_not_allocated_office.append(fellow)

        if(WANTS_ACCOMODATION == 'Y'):
            fellow = Fellow(name)
            available_living_place = self.get_available_living_spaces()

            if available_living_place:
                # if key in dictionary, append to the list in dictionary
                # Otherwise create new key with list
                if available_living_place.name in self.living_space_allocations:
                    fellows_list = self.living_space_allocations[available_living_place.name]
                    fellows_list.append(fellow.name)

                else:
                    self.living_space_allocations[available_living_place.name] = [fellow.name]

                available_living_place.spaces -= 1
                # Assign office to fellow
                fellow.office = available_office

            else:
                self.fellow_not_allocated_living_space.append(fellow)

        # Append fellow to list of fellows
        self.all_fellows.append(fellow)
        return available_office

    def add_staff(self, name):
        """ Add staff to an office"""

        staff = Staff(name)
        available_office = self.get_available_office()

        if available_office:
            # if key in dictionary, append to the list in dictionary
            # Otherwise create new key with list
            if available_office.name in self.office_allocations:
                staff_list = self.office_allocations[available_office.name]
                staff_list.append(staff.name)

            else:
                self.office_allocations[available_office.name] = [staff.name]
            available_office.spaces -= 1
            # Assign office to staff
            staff.office = available_office

        else:
            self.staff_not_allocated.append(staff)

        self.all_staff.append(staff)
        return staff

    def get_available_office(self):
        """Check if offices still have available spaces"""

        for office in self.all_offices:
            if office.contains_space():
                return office
        return False

    def get_available_living_spaces(self):
        """Check if living space still has available space"""

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
            if room_name in self.office_allocations:
                for name in self.office_allocations[room_name]:
                    print(name)

            elif room_name in self.living_space_allocations:
                for name in self.office_allocations[room_name]:
                    print(name)

    def print_allocations(self):
        """Print space allocations to screen"""
        text = ''
        for room_name in self.office_allocations:
            text = text + (room_name.upper())
            text = text + ('---------------------------------------------')
            text = text + (", ".join(self.office_allocations[room_name]).upper())

        print(text)

    def print_allocations_to_file(self):
        """Print space allocations to file"""

        file = open('allocations.txt', 'w')
        for room_name in self.office_allocations:
            file.write('\n'+room_name.upper()+'\n')
            file.write('---------------------------------------------\n')
            file.write(", ".join(self.office_allocations[room_name]).upper()+'\n')
        file.close()

    def print_un_allocations(self):
        """Print spaces not allocated to screen"""

        for fellow in self.fellow_not_allocated_office:
            print(fellow.name.upper() + ', Fellow Unallocated Office')

        for fellow in self.fellow_not_allocated_living_space:
            print(fellow.name.upper() + ', Fellow Unallocated living space')

        for fellow in self.staff_not_allocated:
            print(fellow.name.upper() + ', Staff Unallocated Office')

    def print_un_allocations_to_file(self):
        """Print spaces not allocated to file"""

        file = open('unallocations.txt', 'w')
        for fellow in self.fellow_not_allocated_office:
            file.write(fellow.name.upper() + ', Fellow Unallocated Office\n')

        for fellow in self.fellow_not_allocated_living_space:
            file.write(fellow.name.upper() + ', Fellow Unallocated living space\n')

        for fellow in self.staff_not_allocated:
            file.write(fellow.name.upper() + ', Staff Unallocated Office\n')
        file.close()

    def get_office(self, name):
        """Get office when given person's name"""

        for alloc in self.office_allocations:
            for person_name in self.office_allocations[alloc]:
                if name == person_name:
                    return alloc
        return False

    def get_living_space(self, name):
        """Get office when given person's name"""

        for alloc in self.living_space_allocations:
            for person_name in self.living_space_allocations[alloc]:
                if name == person_name:
                    return alloc
        return False

    def is_fellow(self, name, room_name):
        """Check if person is fellow"""

        for fellow in self.all_fellows:
            if fellow.name == name:
                for office in self.all_offices:
                    if office.name == room_name:
                        fellow.office = office
                        fellow.office.spaces -= 1
                        return True
        return False

    def is_staff(self, name, room_name):
        """Check if person is staff"""

        for staff in self.all_staff:
            if staff.name == name:
                for office in self.all_offices:
                    if office.name == room_name:
                        staff.office = office
                        staff.office.spaces -= 1
                        return True
        return False

    def re_allocate_person(self, name, room_name):
        """Reallocates person from current room to new room"""

        room_office = self.get_office(name)
        room_living_space = self.get_living_space(name)

        if room_office:
            self.office_allocations[room_office].remove(name)
            # Increment space in room
            for office in self.all_offices:
                if office.name == room_office:
                    office.spaces += 1

            # Check if person is fellow or staff
            if not self.is_fellow(name, room_name):
                self.is_staff(name, room_name)

        elif room_living_space:
            self.living_space_allocations[room_living_space].remove(name)

            # Increment space in room
            for living_space in self.all_offices:
                if living_space.name == room_office:
                    living_space.spaces += 1

            # Check if person is fellow or staff
            self.is_fellow(name, room_name)
            # self.is_staff(name, room_name)

    def load_people(self, file_path):
        """Loads people from text file"""
        with open(file_path) as fp:
            for line in fp:
                words = line.split()
                name = words[0] +' '+ words[1]
                if words[2] == 'FELLOW':
                    if words[3] == 'Y':
                        self.add_fellow(name, 'Y')
                    else:
                        self.add_fellow(name)
                elif words[2] == 'STAFF':
                    self.add_staff(name)


    def save_state(self):
        engine = create_engine('sqlite:///..\modals\Dojo.db', echo=True)

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
                office = session.query(OfficeModel).filter_by(name = staff.office.name).first()
                office_id = office.office_id
                staff_modal = StaffModel(staff.name, office_id)
                session.add(staff_modal)

        # Save fellow to db
        for fellow in self.all_fellows:
            with session.no_autoflush:
                if fellow.office != None:
                    office = session.query(OfficeModel).filter_by(name = fellow.office.name).first()
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

    def load_state(self):
        engine = create_engine('sqlite:///..\modals\Dojo.db', echo=True)

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
            office = session.query(OfficeModel).filter_by(id = office_id).first()
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
            new_fellow.living_space = new_living_space
            self.all_fellows.append(new_fellow)


dojo = Dojo()
dojo.create_room(['blue', 'orange'], 'office')
dojo.create_room(['livingSpace1'], 'living_space')
# print(dojo.all_offices)

# dojo.add_fellow('Patrick','Y')
dojo.add_staff('Patrick')
dojo.add_staff('Trey')
dojo.add_staff('Dan')
# dojo.add_staff('Ian')
# dojo.add_staff('Ive')
# dojo.add_staff('Ivan')
# dojo.add_staff('Ivee')
dojo.add_fellow('Jim', 'Y')
dojo.add_fellow('Moses', 'Y')
dojo.add_fellow('Becky', 'Y')
dojo.add_fellow('Sebu')
dojo.add_fellow('Fred', 'Y')
dojo.add_fellow('Samuel', 'Y')
dojo.add_fellow('Dona', 'Y')
print(dojo.office_allocations)
print(dojo.living_space_allocations)
print(dojo.all_fellows)
dojo.print_room('blue')
dojo.print_allocations_to_file()
dojo.print_un_allocations_to_file()
dojo.get_office('hi')
dojo.re_allocate_person('Patrick', 'Yellow')
dojo.save_state()