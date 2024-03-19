class Truck:
    def __init__(self, speed, packages, load, capacity, address, departureTime, miles,ID):
        self.speed = speed
        self.packages = packages
        self.load = load
        self.capacity = capacity
        self.address = address
        self.departureTime = departureTime
        self.time = departureTime
        self.miles = miles
        self.ID = ID

    def getID(self):
        return self.ID

    def __str__(self):
        return f"Speed:{self.speed}, Packages:{self.packages}, Load: {self.load}, Capacity:{self.capacity}, Address:{self.address}, Departure Time:{self.departureTime}, Miles:{self.miles}, ID:{self.ID}"
