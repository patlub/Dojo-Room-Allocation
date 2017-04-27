from classes.person import Person

class Staff(Person):
    def __init__(self, name):
        super().__init__(name, None)
        self.name = name
        self.office = None


