import sys
from tkinter import *
import random

import urllib.request
import json

WIDTH = 200
HEIGHT = 200

X = 0
Y = 1

LATITUDE_INDEX = 4
LONGITUDE_INDEX = 5


class Net:
    def __init__(self, name):
        self.name = name
        self.computer_dict = {}

    # this function can add both router into neighbor list
    def updateConnection(self, first_computer, second_computer):
        if second_computer not in self.computer_dict[first_computer]:
            self.computer_dict[first_computer].add(second_computer)
        if first_computer not in self.computer_dict[second_computer]:
            self.computer_dict[second_computer].add(first_computer)
            



def getAddressFromLine(line):
    if ("RemoteAddress" in line) or ("SourceAddress" in line) or ("TraceRoute" in line):
        temp_list = line.split(" ")
        return temp_list[len(temp_list) - 1]
    else:
        temp_list = line.split(" ")
        return temp_list[len(temp_list) - 1]


def createRandomPoint(point_dict):
    while True:
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)

        if [x, y] in point_dict.values():
            continue
        else:
            return [x, y]


def getIPLocation(computer_name):
    string_list = computer_name.split("\n")
    web_string = "https://geolocation-db.com/jsonp/" + string_list[0]
    with urllib.request.urlopen(web_string) as url:
        data = url.read().decode()
        data = data.split("(")[1].strip(")")

        temp_list = data.split(",")
        print("latitude " + (temp_list[4].split(":"))[1] + "longitude " + (temp_list[5].split(":"))[1])
        if (temp_list[4].split(":"))[1] == '"Not found"':
            return [0, 0]
        else:
            latitude = float((temp_list[4].split(":"))[1])
            longitude = float((temp_list[5].split(":"))[1])
        
        # return [latitude, longitude]
    x = 0
    y = 0
    if latitude > 0:
        y = 100 - abs(latitude)
    else:
        y = 100 + abs(latitude)

    if longitude > 0:
        x = 100 + abs(longitude)
    else:
        x = 100 - abs(longitude)
    return [int(x), int(y)]



if __name__ == "__main__":
# creat dictionary network
    network = Net(name = "network", )
    routeset = {}
    file_traceroute = open(sys.argv[1], 'r')
    
#    for i in range(0, 5):
#        if "ComputerName" in file_traceroute.readline():
#            print("nono\n")
#        else:
#            print(file_traceroute.readline())
#
#    while True:
    for i in range(0, 3):
        line = file_traceroute.readline()
        while line == "\n":
            line = file_traceroute.readline()

        if not line:
            break
        # elif line == "\n":
        #     continue
        # elif "ComputerName" in line:
        else:
            # read RemoteAddress
            line = file_traceroute.readline()
            computer_name = getAddressFromLine(line)
            routeset[computer_name] = list()

            if computer_name not in network.computer_dict:
                network.computer_dict[computer_name] = set()

        print(computer_name)
        print("1\n")

        line = file_traceroute.readline()
        line = file_traceroute.readline()
        source_name = getAddressFromLine(line)

        if source_name not in network.computer_dict:
            network.computer_dict[source_name] = set()

        # print(network.computer_dict)
        # print("2\n")

        file_traceroute.readline()
        file_traceroute.readline()
        line = file_traceroute.readline()
        route_name = getAddressFromLine(line)

        if route_name not in network.computer_dict:
            network.computer_dict[route_name] = set()
            network.updateConnection(source_name, route_name)

        # print(network.computer_dict)
        # print("3\n")

        routeset[computer_name].append(source_name)
        routeset[computer_name].append(route_name)

        line = file_traceroute.readline()

        previous_router = route_name

        # for j in range(0, 5):
        while True:
            if not line:
                break
            elif line == "\n":
                break
            else:
                new_router = getAddressFromLine(line)
                if new_router == "0.0.0.0\n":
                    line = file_traceroute.readline()
                    continue

                routeset[computer_name].append(new_router)

                if new_router in network.computer_dict:
                    network.updateConnection(previous_router, new_router)
                else:
                    network.computer_dict[new_router] = set()
                    network.updateConnection(previous_router, new_router)

                previous_router = new_router
                line = file_traceroute.readline()

        # print(routeset[computer_name])
        # print("4\n")

        for key in network.computer_dict:
            print("key")
            print(key)
            print(network.computer_dict[key])
        print("4\n")
        print(routeset[computer_name])
        # end of reading file
    
    # draw picture of net
    my_window = Tk()
    my_canvas = Canvas(my_window, width = WIDTH, height = HEIGHT, background = 'white')
    my_canvas.grid(row = 0, column = 0)

    # create point for each computer
    point_dict = dict()
    for each_computer in network.computer_dict:
        point_dict[each_computer] = getIPLocation(each_computer)
        if (point_dict[each_computer][0] == 0) and (point_dict[each_computer][1] == 0):
            continue
        else:
            my_canvas.create_oval(point_dict[each_computer][X], point_dict[each_computer][Y], point_dict[each_computer][X], point_dict[each_computer][Y], fill = "black")

    # draw line based on route
    for each_computer in network.computer_dict:
        if (point_dict[each_computer][0] == 0) and (point_dict[each_computer][1] == 0):
            continue
        else:
            for each_neighbor in network.computer_dict[each_computer]:
                if (point_dict[each_neighbor][0] == 0) and (point_dict[each_neighbor][1] == 0):
                    continue
                else:
                    my_canvas.create_line(point_dict[each_computer][X], point_dict[each_computer][Y], point_dict[each_neighbor][X], point_dict[each_neighbor][Y], fill = "blue")


    my_window.mainloop()
    



        
               
            

