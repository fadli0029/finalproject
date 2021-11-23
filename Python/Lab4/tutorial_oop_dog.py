class Dog():
    name = ""
    age = 0
    __breed = None

    def __init__(self, dog_name, dog_age, dog_breed):
        self.name = dog_name
        self.age = dog_age
        self.__breed = dog_breed
    
    # Methods: 
    def speak(self, sound):
        print(self.name, "says", sound)

    def run(self, speed):
        print(self.name, "runs", speed, "mph")

    def description(self):
        print(self.name, "is a", self.age, "year old", self.__breed)

    def define_buddy(self, buddy):
        self.buddy = buddy
        buddy.buddy = self

scout = Dog("Scout", 2, "Belgian Malinois")
print(scout)
print(scout.name)
print(scout.age)
scout.speak("woof")
scout.description()

# Question 3: At the end of the Python file, add a second Dog object named skippy and make scout and skippy buddies. Then use scout to print out skippy’s description.
skippy = Dog("Skippy", 4, "BullDog")
scout.define_buddy(skippy)
skippy.description()
