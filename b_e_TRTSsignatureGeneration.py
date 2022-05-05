import pandas as pd
import pickle
import csv

'''''
1. Each signature will be created using 2500 IAT values.
2. Bin size will be 300. 2500 values will be distrebuted and fallen into approapiate bin.
3. Counting the values fallen in each bin will crate the signature.
4. Signature size will be 300
5. Stored in a dictionary. Key will be MAC address.
'''''

###### define a function ##############
def sign_generation(IAT_list, chunk_size):
    # convert the input dataframe to a list(a row of the dataframe is a single element in the list
    # a row contains n element so, 1 item in the list contain n element
    # List = dataset.values.tolist()


    total_signature = dict()  # to hold the signatures of each device as a list
    deviceMAC = str()

    ###### convert the values to float ##########
    # take a row ,convert the elements to float, sort the row, devide it into 300 bins, count the frequency in each bin, add the frequency in the total_signature list then goto next row
    for item in IAT_list:  # 1 item in the list = n elements
        deviceMAC = item
        IAT = IAT_list[item]

        converted = []  # to hold n elements
        for values in range(len(IAT)):
            x = float(IAT[values])  # converting to float
            converted.append(x)  # appending the floating values

        limit = 0
        # create chunk of 1000
        while limit < len(converted):
            chunk = converted[limit:limit + int(chunk_size)]
            limit = limit + int(chunk_size)

            ######## create bins ################
            if len(chunk) == chunk_size:
                chunk.sort()  # sort the list of converted values of a row to find min and max value in the row
                min = chunk[0]
                max = chunk[len(chunk) - 1]
                # max = 5.0
                bin = (max - min) / 300  # bin size for the row

                ########## counting the number of values that fall in a bin(frequency count) ############
                signature = []  # to hold the frequency count of a row(signature)

                while min < max:  # to traverse from 1st element to last element
                    upper = (min + bin)  # upper limit of the bin lower is min
                    count = 0  # initialize the count to 0

                    # for the last round to check overcome the extra 1 loop(for 600 bin some row became 601)
                    if len(signature) == 299:
                        upper = max

                    ########## comparing an element if it falls in a bin #############
                    for i in range(len(chunk)):  # for a bin check all values in the row
                        comp = chunk[i]  # taking an element from the row

                        # if the element falls in the bin then increase the count by 1
                        if min <= comp <= upper:
                            count += 1
                    signature.append(count)  # apend the count in the signature list of a row
                    min = upper  # update the min to next bin
                total_signature.setdefault(deviceMAC, []).append(signature)

          # after generation of signature of a row append it in the main list
    # print("the signature set", total_signature)  # length of the total signature

    ######## converting the signature list to data frame ###############
    # device_SIGNATURE = DataFrame(total_signature)
    # ******************************************
    # device_SIGNATURE = device_SIGNATURE.fillna(0)  # normalize the columns to 301 values in each row
    # *****************************************
    print(total_signature)
    return total_signature  # returning the signature dataframe



########################################
# DeviceList = []
# SignatureList = []
# # count = 0


############################################
#     # count += 1
    # DeviceList.append(str(count))
    # SignatureList.append(signatures[items])
# df.to_csv('signature_with_ID.csv')

# sig_file = open('signatures.csv', 'w+', newline='')
# dev_file = open('device.csv', 'w+', newline='')
# # writing the data into the file
# with sig_file:
#     write = csv.writer(sig_file)
#     write.writerows(SignatureList)
#
# with dev_file:
#     write = csv.writer(dev_file)
#     write.writerows(DeviceList)

# **************************************************
