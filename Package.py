import datetime
import Truck

class Package:
    def __init__(self, Id, deadLine, weight, address, city, state, zipCode, status,truck):

        self.Id = Id
        self.deadLine = deadLine
        self.departureTime = None
        self.deliveryTime = None
        self.weight = weight
        self.address = address
        self.city = city
        self.state = state
        self.zipCode = zipCode
        self.status = status
        self.truck = truck

    def updateStatus(self, time):
        if self.departureTime > time:
            self.status = "Package is on the way!"
        elif self.deliveryTime < time:
            self.status = "Package delivered"
        else:
            self.status = "Package ready at hub"

        # update package 9 address after 10:20
        if self.Id == 9:
            if time > datetime.timedelta(hours=10, minutes=20):
                self.address = "410 S State St"
                self.zipCode = "84111"

    def __str__(self):
        return f"ID:{self.Id}, DeadLine:{self.deadLine}, Weight: {self.weight}, Address:{self.address}, City:{self.city}, State:{self.state}, ZipCode:{self.zipCode}, Delivery Time:{self.deliveryTime},Status:{self.status}, Truck Number:{self.truck.getID()}"
