from classes.office import Office
from classes.living_space import LivingSpace
from classes.fellow import Fellow
from classes.staff import Staff

class Dojo:
    def __init__(self):
        self.all_offices = []
        self.all_living_spaces = []
        self.all_fellows = []
        self.all_staff = []

    def create_room(self, room_names, room_type):
        if not isinstance(room_names, list) or not isinstance(room_type, str):
            raise TypeError('Arguments should be a list and string')
        elif not room_names:
            raise ValueError('List of room names can not be empty')
        else:
            # First Check if office name or living_space name exists in list


            if room_type == 'office':
                office = Office(room_names)
                self.all_offices.append(office)
            elif room_type == 'living_space':
                living_space = LivingSpace(room_names)
                self.all_living_spaces.append(living_space)
            else:
                return ('Invalid room type')

    def add_fellow(self, name, WANTS_ACCOMODATION = 'N'):
        fellow = Fellow(name, WANTS_ACCOMODATION)
        available_office = self.get_available_office()
        if not available_office:
            fellow = available_office.add_person(fellow)
            self.all_fellows.append(fellow)

        if(WANTS_ACCOMODATION == 'Y'):
            fellow = Fellow(name, WANTS_ACCOMODATION)
            available_living_place = self.get_available_living_spaces()
            if not available_living_place:
                fellow = available_living_place.add_person(fellow)
                self.all_fellows.append(fellow)

    def add_staff(self, name):
        staff = Staff(name)
        available_office = self.get_available_office()
        if not available_office:
            staff = available_office.add_person(staff)
            self.all_fellows.append(staff)

    def get_available_office(self):
        for office in self.all_offices:
            if office.contains_space:
                return office
        return False

    def get_available_living_spaces(self):
        for living_spaces in self.all_living_spaces:
            if living_spaces.contains_space:
                return living_spaces
        return False


