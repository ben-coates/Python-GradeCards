class Student:
    def __init__(self, name, id, gradelevel, date, term, gpa, units, classes):
        self.name = name
        self.id = id
        self.gradelevel = gradelevel
        self.date = date
        self.term = term
        self.gpa = gpa
        self.units = units
        self.classes = classes
        self.eligibility = self.getEligibility()
        self.effort = self.getEffort()
        self.coupons = self.getCoupons()
        self.gender = ""

    def addAttribute(self, key, value):
        self.__setattr__(key.replace(" ","").lower(), value)

    def getEligibility(self):
        failing = 0
        for c in self.classes:
            if "F" in c.get("lettergrade"):
                failing = failing + 1
        
        if (failing >=2 or self.gpa < 1):
            return "Ineligible"
        elif (failing == 1 or self.gpa < 2):
            return "Limited"
        elif (self.gpa >= 3.5):
            return "Honor Roll"
        else:
            return "Eligible"

    def getEffort(self):
        overallEffort = 0
        for cl in self.classes:
            overallEffort = overallEffort + cl.get('effort')

        return round(overallEffort / len(self.classes) * 10)

    def getCoupons(self):
        if self.effort > 17:
            return 5
        elif self.effort >= 12:
            return 4
        elif self.effort >= 9:
            return 3
        elif self.effort >= 5:
            return 2
        elif self.effort >= 0:
            return 1
        else:
            return 0

    def printStudent(self):
        print("Name:", self.name)
        print("ID:", self.id)
        print("Grade Level:", self.gradelevel)
        print("Date:", self.date)
        print("Term:", self.term)
        print("GPA:", self.gpa)
        print("Units:", self.units)
        print("Status:", self.eligibility)
        print("Effort:", self.effort)
        self.printClasses()
        print("\n")

    def printClasses(self):
        print(  ('Class Name').ljust(30),
                ('Credits').ljust(10),
                ('Grade').ljust(11),
                ('Effort').ljust(6)
        )
        print("= = = = = = = = = = = = = = = = = = = = = = = = = = = = = ")
        for i in self.classes:
            print(  i.get('classname').ljust(30),
                    i.get('credits').ljust(10),
                    i.get('lettergrade').ljust(3),
                    i.get('percentage').ljust(7),
                    str(i.get('effort')).ljust(6)
            )