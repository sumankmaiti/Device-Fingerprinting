import pickle
import numpy
import b_a_TRTSreadPCAP
import b_b_TRTSseperation
import b_d_a_TRTArrivalTimeWithPacketStatus
import b_d_b_TRTSInterArrivalTimeGeneration
import b_e_TRTSsignatureGeneration
import b_f_TRgenerateCSVtraining
from pathlib import Path
from operator import add

feature_list = dict()

# autometiclly read the files from the folder
entries = Path(r'D:\fingerprinting final successfully run on iit delhi machine\packet_capture')
for entry in entries.iterdir():
 
    # ############################### Read packets #####################################################

    # *********************************************************************************************
    total = b_a_TRTSreadPCAP.read_pyshark(str(entry))
    # print('packet details:\n', total)
    print('length:', len(total))
    # *********************************************************************************************

    # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    # file = open("total_valid_packets.pkl", "wb")
    # pickle.dump(total, file)
    # file.close()
    # print("stored ", entry, " in total_valid_packets.pkl")
    # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

    # ########################## Separate Packets based on sources #####################################

    # *********************************************************************************************
    print("\nSeparating traffics for each device...\n")
    device_traffic = b_b_TRTSseperation.separate(total)
    # print("\ntotal ", len(device_traffic), "devices")
    for item in device_traffic:
        print(item, "with", len(device_traffic[item]), "traffic captured")
    # *********************************************************************************************

    # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    # file = open("separated_traffics_for_each_devices(sum2).pkl", "wb")
    # pickle.dump(device_traffic, file)
    # file.close()
    # print("stored ", entry, " in separated_traffics_for_each_devices.pkl ")
    # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx


    # ################################# inter arrival time  ########################################

    print("\nGenerating Inter Arrival Times from traffics for each device...\n")
    IAT_of_device = b_d_b_TRTSInterArrivalTimeGeneration.IATgeneration(device_traffic)
    # print("\nIAT of devices:\n", IAT_of_device)
    # print("\ntotal ", len(IAT_of_device), "devices")
    for item in IAT_of_device:
        print(item, "with", len(IAT_of_device[item]), "traffic captured")

    # ######################## separate IAT based on traffic type ###################################

    # *********************************************************************************************
    print("\nSeparating traffics based on traffic type for each device...\n")
    inter_arrival_times_with_traffic_type = b_d_a_TRTArrivalTimeWithPacketStatus.findArrival(IAT_of_device)
    # print("\n traffic devices:\n", inter_arrival_times_with_traffic_type)
    # print("\ntotal ", len(inter_arrival_times_with_traffic_type), "devices")
    # for item in inter_arrival_times_with_traffic_type:
    #     for it in inter_arrival_times_with_traffic_type[item]:
    #         print(it)
        # print(item, "with", len(inter_arrival_times_with_traffic_type[item]), "traffic captured")


    # ##################################### sign generation #####################################################

    # *********************************************************************************************
    print("\nGenerating Signature for each traffic type for each device...\n")
    sig_list = dict()
    for ip in inter_arrival_times_with_traffic_type:
        for all_traffic in inter_arrival_times_with_traffic_type[ip]:
            sig_device = b_e_TRTSsignatureGeneration.sign_generation(all_traffic, 2500)
            sig_list.setdefault(ip, []).append(sig_device)

    # for item in sig_list:
    #     for it in sig_list[item]:
    #         for i in it:
    #             print(it[i])
    # *********************************************************************************************


    # #################################### Save as CSV ##################################################

    # *********************************************************************************************
    # print("\nSaving Signature in signature.csv...\n")
    b_f_TRgenerateCSVtraining.generateCSV(sig_list, "demo.csv")
    # b_f_TRgenerateCSVtraining.generateCSV(sig_device, "traffic_only_features.csv")
    # *********************************************************************************************

    # ########################### clear all preserved values#################################################
    total.clear()
    device_traffic.clear()
    IAT_of_device.clear()
    inter_arrival_times_with_traffic_type.clear()
    sig_list.clear()
    # *********************************************************************************************

    print("\n\n")
