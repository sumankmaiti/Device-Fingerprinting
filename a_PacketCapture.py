import pyshark
from pathlib import Path

# choice = input("capture for training or testing: (1==training, 2==testing): ")

# if choice == "1":
file_name = "rsp"
print("capturing... please wait")
for i in range(1000):
    capture = pyshark.LiveCapture(interface='wlp3s0', output_file="/home/ubuntu/Desktop/data_capture/" + file_name + str(i) + ".pcapng")
    capture.sniff(packet_count=11000)
    print(file_name + str(i) + ".pcapng stored ", capture)

# elif choice == "2":
#     file_name = input("enter file name to store: ")
#     print("capturing... please wait")
#     capture = pyshark.LiveCapture(interface='hotspot', output_file="D:/IIT DELHI ALL/PACKET CAPTURE/" + file_name + ".pcapng")
#     capture.sniff(packet_count=11000)
#     print(file_name + ".pcapng stored ", capture)

# else:
#     print("invalid choice")
"""
#*************** Rename multiple files ***********************
count = 1
entries = Path('D:\IIT DELHI ALL\PACKET CAPTURE\suman pc')
for entry in entries.iterdir():
    if entry.is_file():
        old_name = entry.stem
        old_extension = entry.suffix
        directory = entry.parent
        new_name = "LenovoSuman" + str(count) + old_extension
        entry.rename(Path(directory, new_name))
        count += 1
"""