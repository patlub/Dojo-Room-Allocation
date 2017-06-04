class Room:
    def __init__(self, name):
        self.name = name

class Person:
    def __init__(self, name, office):
        self.name = name
        self.office = office

class Office(Room):
    def __init__(self, name):
        super().__init__(name)
        self.name = name
        self.spaces = 6
        self.occupants = []

    def contains_space(self):
        return self.spaces > 0

class LivingSpace(Room):
    def __init__(self, name):
        super().__init__(name)
        self.name = name
        self.spaces = 4
        self.occupants = []

    def contains_space(self):
        return self.spaces > 0


class Fellow(Person):
    def __init__(self, name):
        super().__init__(name, None)
        self.name = name
        self.office = None
        self.living_place = None

class Staff(Person):
    def __init__(self, name):
        super().__init__(name, None)
        self.name = name
        self.office = None
