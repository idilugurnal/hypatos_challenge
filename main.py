import pandas as pd
import Levenshtein as ls

MAXD = 3
MAXV = 2

def calculate_distance(str1, str2):
    if str1 == "" or str2 == "": return 1000
    return ls.distance(str(str1), str(str2))

def convert_to_int(value):
    if value == "": return value
    return(int(float(value)))

def check_match(sample, extraction, matched):

    length = len(extraction.index)
    counter = 0
    index = -1
    for i in range(0,length):
        if i not in matched:
            if sample.Description == extraction.iloc[i].Description\
                or (calculate_distance(sample["Description"], extraction.iloc[i]["Description"]) < MAXD
                    and (calculate_distance(convert_to_int(sample["Unit price"]), convert_to_int(extraction.iloc[i]["Unit price"])) < MAXV
                         or calculate_distance(convert_to_int(sample["Total price"]), convert_to_int(extraction.iloc[i]["Total price"])) < MAXV)):

                counter += 1
                index = i
                if counter > 1:
                    index = -2
    return index

def generate_matches(gt, extraction):
    matched = set()
    pairs = []
    length_gt = len(gt.index)
    for i in range (0,length_gt):
        m = check_match(gt.iloc[i], extraction, matched)
        if m > -1:
            matched.add(m)
        pairs.append((i,m))

    return pairs




def read_csv(filename):
    df = pd.read_csv(filename, usecols=["File_name", "Description", "Quantity", "Unit price", "Total price"], keep_default_na=False)
    return df


if __name__ == "__main__":

    extraction = read_csv("Extraction.csv")
    gt = read_csv("GT Ground Truth.csv")
    pairs = generate_matches(gt, extraction)
    print(pairs)
