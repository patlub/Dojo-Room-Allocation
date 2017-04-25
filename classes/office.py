from classes.room import Room

class Office(Room):

    def __init__(self, name):
        super().__init__(name)
        self.name = name
        self.spaces = 6

    def contains_space(self):
        return self.spaces != 0

    def add_person(self, person):
        person.Office = self
        self.spaces -= 1

