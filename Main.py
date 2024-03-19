

import datetime
import csv
from Package import Package
import Truck
import HashMap


# parse Distance CVS
with open("csv/distance.csv") as distanceFile:
    distanceCsv = csv.reader(distanceFile)
    distanceCsv = list(distanceCsv)


# calculate distance
def getDistance(x, y):
    dist = distanceCsv[x][y]
    if dist == '':
        dist = distanceCsv[y][x]
    return float(dist)


# parse package CVS
with open("csv/package.csv") as packageFile:
    packageCsv = csv.reader(packageFile)
    packageCsv = list(packageCsv)


# instantiate package objects, then insert into hashmap,
def extractPackageFields(file, hashMap):
    with open(file) as packageInformation:
        packageField = csv.reader(packageInformation)
        for p in packageField:
            packageId = int(p[0])
            packageAddress = p[1]
            packageCity = p[2]
            packageState = p[3]
            packageZipcode = p[4]
            packageDeadline = p[5]
            packageWeight = p[6]
            packageStatus = "Package waiting at hub"
            package = Package(packageId, packageDeadline, packageWeight, packageAddress, packageCity, packageState,
                              packageZipcode, packageStatus,None)
            hashMap.insert(packageId, package)


packageHashmap = HashMap.HashMap()

extractPackageFields("csv/package.csv", packageHashmap)

# parse address CVS
with open("csv/address.csv") as addressFile:
    addressCsv = csv.reader(addressFile)
    addressCsv = list(addressCsv)


# parse csv for address number
def getAddress(address):
    for data in addressCsv:
        if address in data[2]:
            return int(data[0])


# instantiate and manually load the  WGUPS delivery trucks.

firstTruck = Truck.Truck(18, [1, 13, 14, 15, 16, 20, 29, 30, 31, 34, 37, 40], None, 16, "4001 South 700 East",
                              datetime.timedelta(hours=8), 0.0,1)

# packages 3,18,36,38  must be on truck, delivery until EOD
secondTruck = Truck.Truck(18, [3, 12, 17, 18, 19, 21, 22, 23, 24, 26, 27, 35, 36, 38, 39], None, 16,
                               "4001 South 700 East",
                               datetime.timedelta(hours=10, minutes=20), 0.0,2)

# packages 6,9,25,28,32 were all delayed all will be handles in truck three
# method in package class to update address for package 9 after 10:20
thirdTruck = Truck.Truck(18, [2, 4, 5, 6, 7, 8, 9, 10, 11, 25, 28, 32, 33], None, 16, "4001 South 700 East",
                              datetime.timedelta(hours=9, minutes=9), 0.0,3)


def deliverPackage(truck):
    # nearest neighbor algorithm to deliver the packages.
    readyForDelivery = []
    for Id in truck.packages:
        package = packageHashmap.search(Id)
        package.truck = truck
        readyForDelivery.append(package)
    # reset on board to be re-sorted regarding the next nearest neighbor
    truck.packages.clear()

    # will run until there are no packages left in our readyForDeliveryList.
    while len(readyForDelivery) > 0:
        nxtAddress = 1000
        nxtPackage = None
        for package in readyForDelivery:
            if getDistance(getAddress(truck.address), getAddress(package.address)) <= nxtAddress:
                nxtAddress = getDistance(getAddress(truck.address), getAddress(package.address))
                nxtPackage = package
        # add package onto truck, remove after delivery then update truck miles, current location, and system time.
        truck.packages.append(nxtPackage.Id)
        readyForDelivery.remove(nxtPackage)
        truck.miles = truck.miles + nxtAddress
        truck.address = nxtPackage.address
        truck.time = truck.time + datetime.timedelta(hours=nxtAddress / 18)
        nxtPackage.deliveryTime = truck.time
        nxtPackage.departureTime = truck.departureTime


deliverPackage(firstTruck)
deliverPackage(secondTruck)
# third truck will leave after one and two are finished
thirdTruck.depart_time = min(firstTruck.time, secondTruck.time)
deliverPackage(thirdTruck)
totalMiles = firstTruck.miles + secondTruck.miles + thirdTruck.miles

# CLI User interface
print("\U0001f69A \U0001f69A WGUPS total truck distance driven:", totalMiles, "miles  \U0001f69A \U0001f69A")
print("Please type 'start' to begin, anything else will exit")
text = input()

if text == "start":

    # The user will be asked to enter a specific time for review
    print("In 'HH:MM:SS' please enter the time to review")
    reviewTime = input()
    (hour, minute, second) = reviewTime.split(":")
    time = datetime.timedelta(hours=int(hour), minutes=int(minute), seconds=int(second))
    # Print out all packages by default at chosen time
    for packageId in range(1, 41):
        package = packageHashmap.search(packageId)
        package.updateStatus(time)
        print(str(package))



    def packageEmoji():
        for i in range(9):
            print("\U0001F4E6", end=" ")


    # Give option to choose a specific package to review at given time
    while 2 > 1:
        packageEmoji()

        print("To view an individual package at time", time, "please enter the package number or type 'stop' to exit",
              end=" ")

        packageEmoji()
        print()
        packageNumber = input()

        if packageNumber == "stop":
            exit()
        package = packageHashmap.search(int(packageNumber))
        package.updateStatus(time)
        print(str(package))
