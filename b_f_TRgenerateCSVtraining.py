import pandas as pd
import csv


# write into a csv file
def generateCSV(signatures, name_of_the_file):
    df = pd.DataFrame()
    for ip in signatures:
        for traffic in signatures[ip]:
            for sig in traffic:
                all_sign = traffic[sig]
                for sign in all_sign:
                    sign.append(sig)
                    sign.append(ip)
                    df = df.append(sign)
                with open(name_of_the_file, "a", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerows(all_sign)
    print("\nSignatures stored in ", name_of_the_file)
