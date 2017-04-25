from classes.office import Office
from classes.living_space import LivingSpace

class Dojo:
    def __init__(self):
        self.all_offices = []
        self.all_living_spaces = []

    def create_room(self, room_names, room_type):
        if not isinstance(room_names, list) or not isinstance(room_type, str):
            raise TypeError('Arguments should be a list and string')
        elif not room_names:
            raise ValueError('List of room names can not be empty')
        else:
            if room_type == 'office':
                office = Office(room_names)
                self.all_offices.append(office)
            else:
                living_space = LivingSpace(room_names)
                self.all_living_spaces.append(living_space)

    def add_fellow(self, name):
