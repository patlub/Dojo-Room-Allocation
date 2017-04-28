"""
This example uses docopt with the built in cmd module to demonstrate an
interactive command application.
Usage:
    (dojo) create_room <room_type> <room_name>
    (dojo) add_person person_name (<FELLOW>|<STAFF>) [<wants_accommodation>]
    (dojo) print_room <room_name>
    (dojo) print_allocations [--o=filename]
    (dojo) print_unallocated [--o=filename]
    (dojo) reallocate_person <person_identifier> <new_room_name>
    (dojo) load_people
    (dojo) save_state [--db=sqlite_database]
    (dojo) load_state <sqlite_database>
    (dojo) (-i | --interactive)
    (dojo) (-h | --help)
Arguments:
    FELLOW|STAFF           Type of person to create/employ
    wants_accommodation    Specify if person(only fellow) wants living space
Options:
    -i, --interactive  Interactive Mode
    -h, --help  Show this screen and exit.
    --o=filename
    --db=sqlite_database
"""

from classes.dojo import Dojo
import sys
import cmd
from docopt import docopt, DocoptExit


def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """

    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.

            print('Invalid Command!')
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here.

            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn


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
            for room_name in room_names:
                for office in self.all_offices:
                    if room_name == office.name:
                        return 'Room name already exists'

            for room_name in room_names:
                for living_space in self.all_living_spaces:
                    if room_name == living_space.name:
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

        if (WANTS_ACCOMODATION == 'Y'):
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
        shuffle(self.all_offices)
        for office in self.all_offices:
            if office.contains_space():
                return office
        return False

    def get_available_living_spaces(self):
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
            print(room_name.upper())
            print('---------------------------------------------')
            print(", ".join(self.office_allocations[room_name]).upper())

        print(text)

    def print_allocations_to_file(self, filename):
        """Print space allocations to file"""
        filename = '../files/' + filename
        file = open(filename, 'w')
        for room_name in self.office_allocations:
            file.write('\n' + room_name.upper() + '\n')
            file.write('---------------------------------------------\n')
            file.write(", ".join(self.office_allocations[room_name]).upper() + '\n')
        file.close()

    def print_un_allocations(self):
        """Print spaces not allocated to screen"""

        for fellow in self.fellow_not_allocated_office:
            print(fellow.name.upper() + ', Fellow Unallocated Office')

        for fellow in self.fellow_not_allocated_living_space:
            print(fellow.name.upper() + ', Fellow Unallocated living space')

        for fellow in self.staff_not_allocated:
            print(fellow.name.upper() + ', Staff Unallocated Office')

    def print_un_allocations_to_file(self, filename):
        """Print spaces not allocated to file"""
        filename = '../files/' + filename

        file = open(filename, 'w')
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
                name = words[0] + ' ' + words[1]
                if words[2] == 'FELLOW':
                    if words[3] == 'Y':
                        self.add_fellow(name, 'Y')
                    else:
                        self.add_fellow(name)
                elif words[2] == 'STAFF':
                    self.add_staff(name)

    def save_state(self, db = None):
        if db is None:
            engine = create_engine('sqlite:///..\modals\Dojo.db', echo=True)
        else:
            db = db +'.db'
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

    def load_state(self, db = None):
        if db is None:
            engine = create_engine('sqlite:///..\modals\Dojo.db', echo=True)
        else:
            db = db +'.db'
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
            new_fellow.living_space = new_living_space
            self.all_fellows.append(new_fellow)





dojo = Dojo()
class TheDojo(cmd.Cmd):
    intro = 'Welcome to THE DOJO OFFICE ALLOCATION PROGRAM!' \
            + ' (type help for a list of commands.)'
    prompt = '(The Dojo) '

    file = None

    @docopt_cmd
    def do_create_room(self, arg):
        """Usage: create_room <room_type> <room_name>"""
        room_names = []
        room_names.append(arg['<room_name>'])
        print(room_names)
        room_type = arg['<room_type>']
        dojo.create_room(room_names, room_type)

    @docopt_cmd
    def do_add_person(self, arg):
        """Usage: add_person <person_name> (<FELLOW>|<STAFF>) [<wants_accommodation>]"""
        person_name = arg['<person_name>']
        accomodation = arg['<wants_accommodation>']

        if arg['<FELLOW>']:
            dojo.add_fellow(person_name, accomodation)
        else:
            dojo.add_staff(person_name)

    @docopt_cmd
    def do_print_room(self, arg):
        """Usage: print_room <room_name>"""
        room_name = arg['<room_name>']
        dojo.print_room(room_name)

    @docopt_cmd
    def do_print_allocations(self, arg):
        """Usage: print_allocations [--o=filename]"""
        if arg['--o'] is None:
            dojo.print_allocations()
        else:
            dojo.print_allocations_to_file(arg['--o'])

    @docopt_cmd
    def do_print_unallocated(self, arg):
        """Usage: print_unallocated [--o=filename]"""
        if arg['--o'] is None:
            dojo.print_un_allocations()
        else:
            dojo.print_un_allocations_to_file(arg['--o'])

    @docopt_cmd
    def do_reallocate_person(self, arg):
        """Usage: reallocate_person <person_identifier> <new_room_name>"""
        person_name = arg['<person_identifier>']
        room_name = arg['<new_room_name>']
        dojo.re_allocate_person(person_name, room_name)

    @docopt_cmd
    def do_load_people(self, arg):
        """Usage: load_people"""
        dojo.load_people()

    @docopt_cmd
    def do_save_state(self, arg):
        """Usage: save_state [--db=sqlite_database]"""
        if arg['--o'] is None:
            dojo.save_state()
        else:
            dojo.save_state(arg['--o'])

    @docopt_cmd
    def do_load_state(self, arg):
        """Usage: load_state [--db=sqlite_database]"""
        if arg['--o'] is None:
            dojo.load_state()
        else:
            dojo.load_state(arg['--o'])

    def do_quit(self, arg):
        """Quits out of Interactive Mode."""

        print('******Good Bye!******')
        exit()


opt = docopt(__doc__, sys.argv[1:])

if opt['--interactive']:
    TheDojo().cmdloop()
print(opt)

