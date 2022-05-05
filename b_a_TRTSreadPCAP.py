import pyshark
import pickle

########################################################################
#                             Read method                              #
########################################################################

def read_pyshark(path):

    print("Reading {}...".format(path))

    # global time, sourceMAC
    pcap_object = pyshark.FileCapture(path, use_json=True)

    # use this to extract time, source, destination, total number of packets.
    pcap_object_summary = pyshark.FileCapture(path, only_summaries=True)

    # to get the number of packets
    pcap_object_summary.load_packets()

    print("total ", len(pcap_object_summary), " packets. Reading packets please wait...")

    # Initialise result
    result = list()
    # count = 0

    # Loop over packets to extract values
    # while True:
    for i in range(len(pcap_object_summary)):
        try:
            # print(item)
            # packet = next(pcap)

            packet_layers = pcap_object[i]
            packet = pcap_object_summary[i]

            protocol = packet_layers.layers[2].layer_name
            sourceMAC = packet_layers.layers[0].src
            sourceIP = packet.source
            # destinationMAC = packet_layers.layers[0].dst
            index = packet.no

            time = packet.time
            # print(time)

            # d = [index, protocol, time, sourceMAC, sourceIP]
            # result.append(d)

            if protocol == "ICMP" or protocol == "ICMPV6" or protocol == "icmpv6" or protocol == "icmp":
                type = int(packet_layers.layers[2].type)
                d = [index, protocol, time, sourceMAC, type]
                result.append(d)

            if protocol == "UDP" or protocol == "udp" or protocol == "TCP" or protocol == "tcp":
                source_port = int(packet_layers.layers[2].srcport)
                destination_port = int(packet_layers.layers[2].dstport)
                d = [index, protocol, time, sourceMAC, source_port, destination_port]
                result.append(d)


        except Exception as ex:
            # print("packet ", i+1, "not extracted. protocol not supported")
            pass
        #     break


    # Close capture
    pcap_object.close()
    pcap_object_summary.close()
    print(result)
    return result

##################################################################
# for testing purpose
# X = read_pyshark('D:\IIT DELHI ALL\multiple device packets for outgoing packets\satanu 2 device meeting.pcapng')
#
# file = open("total_valid_packets.pkl", "wb")
# pickle.dump(X, file)
# file.close()
##################################################################
# list = []
# try:
#     read_file = open("total_valid_packets.pkl", "rb")
#     list = pickle.load(read_file)
# except:
#     pass
#
# finalList = list + total
# file = open("total_valid_packets.pkl", "wb")
# pickle.dump(finalList, file)
# file.close()
