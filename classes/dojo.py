from classes.office import Office
from classes.living_space import LivingSpace
from classes.fellow import Fellow
from classes.staff import Staff

class Dojo:
    def __init__(self):
        self.all_offices = []
        self.office_allocations = {}
        self.living_space_allocations = {}
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
        fellow = Fellow(name, WANTS_ACCOMODATION, None)
        available_office = self.get_available_office()
        if available_office:
            if available_office.name in self.office_allocations:
                fellows_list = self.office_allocations[available_office.name]
                fellows_list.append(fellow.name)
            else:
                self.office_allocations[available_office.name] = [fellow.name]
            available_office.spaces -= 1
            print(available_office.spaces)

        if(WANTS_ACCOMODATION == 'Y'):
            fellow = Fellow(name, WANTS_ACCOMODATION, None)
            available_living_place = self.get_available_living_spaces()
            if available_living_place:
                if available_living_place.name in self.living_space_allocations:
                    fellows_list = self.living_space_allocations[available_living_place.name]
                    fellows_list.append(fellow.name)
                else:
                    self.living_space_allocations[available_living_place.name] = [fellow.name]
                available_living_place.spaces -= 1

        self.all_fellows.append(fellow.name)

    def add_staff(self, name):
        staff = Staff(name)
        available_office = self.get_available_office()
        if not available_office:
            staff = available_office.add_person(staff)
            self.all_fellows.append(staff.name)

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

# dojo = Dojo()
# dojo.create_room(['blue', 'orange'], 'office')
# dojo.create_room(['livingSpace1'], 'living_space')
# print(dojo.all_offices)
#
# dojo.add_fellow('Patrick','Y')
# dojo.add_fellow('Jim', 'Y')
# dojo.add_fellow('Moses', 'Y')
# dojo.add_fellow('Becky', 'Y')
# dojo.add_fellow('Sebu', 'Y')
# dojo.add_fellow('Fred', 'Y')
# print(dojo.office_allocations)
# print(dojo.living_space_allocations)
# print(dojo.all_fellows)
