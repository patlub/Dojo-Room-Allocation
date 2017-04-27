from classes.person import Person

class Fellow(Person):
    def __init__(self, name):
        super().__init__(name, None)
        self.office = None
        self.name = name
        self.living_space = None


