
'''''
here the traffics are devided into devices
find the actual source by checking type for ICMP and ports for TCP/UDP

ICMP: if the type of the packet is request then destination will be the source
      if the type of the packet is reply then the source is the actual source

TCP/UDP: which port number is grater that will be the actual source i.e device
'''
dev_list = dict()

def separate(file):
    for item in file:
        protocol = item[1]
        sourceMAC = item[3]
        # for each packet store packets based on the device ip
        # sourceIP = item[4]
        # dev = [item[0], item[1], item[2], item[3]]
        # dev_list.setdefault(sourceIP, []).append(dev)
        # if packet is icmp
        if protocol == "ICMP" or protocol == "ICMPV6" or protocol == "icmp" or protocol == "icmpv6":
            type = int(item[4])
            # since packet after receiving do its processing then send another packet we need two of them
            # if type == 8 or type == 128:
            #     sourceMAC = item[4]
            if type == 0 or type == 129:

                dev = [item[0], item[1], item[2]]
                dev_list.setdefault(sourceMAC, []).append(dev)

        # for packets has port numbers
        if protocol == "UDP" or protocol == "udp" or protocol == "TCP" or protocol == "tcp":
            src_port = item[4]
            dst_port = item[5]

            if src_port > dst_port:

                dev = [item[0], item[1], item[2]]
                dev_list.setdefault(sourceMAC, []).append(dev)
    print(dev_list)
    return dev_list

##################################################
import pickle
# read_file = open("total_valid_packets.pkl", "rb")
# list = pickle.load(read_file)
# x = separate(list)
# print(x)
# print("devices", len(x))
# for i in x:
#     print(i, len(x[i]), "values")
#
# file = open("seperated_devices.pkl", "wb")
# pickle.dump(x, file)
# file.close()