from classes.room import Room

class LivingSpace(Room):
    def __init__(self, name):
        super().__init__(name)
        self.name = name
        self.spaces = 4


    def contains_space(self):
        if self.spaces > 0:
            return True
