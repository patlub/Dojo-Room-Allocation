from classes.room import Room

class Office(Room):
    def __init__(self, name):
        super().__init__(name)
        self.spaces = 6
        self.name = name

    def contains_space(self):
        if self.spaces > 0:
            return True


