from classes.person import Person

class Fellow(Person):
    def __init__(self, name, WANTS_ACCOMODATION, office):
        super().__init__(name, office)
        self.office = None
        self.name = name
        self.wants_accomodation = WANTS_ACCOMODATION
        self.living_space = None


