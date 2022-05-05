import pickle


def IATgeneration(file):
    # read_file = open("total_valid_packets.pkl", "rb")
    # file = pickle.load(read_file)
    # print("total length: ", len(file))

    """
    4. Stored in a dictionary. Key will be the MAC address.
    """

    IAT_list = dict()

    ########### for each devices ##########
    for item in file:

        # index1 = int(file[i][0])
        # index2 = int(file[i + 1][0])
        device = item
        packets = file[item]
        # print(device, "with", len(packets), "Arrival time.")

        init_time = 0.0
        ### for each packets ###
        for packet in packets:
            # protocol = packets[p][1]
            # if protocol == "icmp" or protocol == "icmpv6" or protocol == "ICMPV6" or protocol == "ICMP":
            #     type = int(packets[p][3])
            #     if type == 0 or type == 129:
            time2 = float(packet[2])
            time1 = float(init_time)
            interval = time2 - time1
            temp =[packet[0], packet[1], interval]
            IAT_list.setdefault(device, []).append(temp)
            init_time = packet[2]

        # if float(interval) <= 1.0:
        # MAC = file[i][2]

    ########################################
    print(IAT_list)
    return IAT_list
