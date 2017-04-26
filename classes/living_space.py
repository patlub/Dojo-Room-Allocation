from classes.room import Room

class LivingSpace(Room):
    spaces = 4
    def __init__(self, name):
        super().__init__(name)
        self.name = name


    def contains_space(self):
        if self.spaces > 0:
            return True
