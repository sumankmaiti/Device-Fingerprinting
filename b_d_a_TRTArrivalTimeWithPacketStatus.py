"""
this will extract the arrival times and make a list of times and store in a dictionary with MAC id
"""
dev_arrival = dict()


def findArrival(file):
    for item in file:
        dev = str(item)
        traffic = file[item]
        temp = dict()
        for items in traffic:
            traf = items[1]
            # source = str(items[3])
            # destination = str(items[4])
            # if item == source:
            #     packet_status = 'out'
            # elif item == destination:
            #     packet_status = 'in'
            # else:
            #     packet_status = 'unknown'
            temp.setdefault(traf, []).append(items[2])

        dev_arrival.setdefault(dev, []).append(temp)
    print(dev_arrival)
    return dev_arrival


#############################################
# import pickle
# read_file = open("seperated_devices.pkl", "rb")
# list = pickle.load(read_file)
# # print(list)
# arrival = findArrival(list)
# print(arrival)
# print("devices", len(arrival))
# for i in arrival:
#     print(i, len(arrival[i]), "values")