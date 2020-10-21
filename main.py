import pandas as pd
import Levenshtein as ls
import sys
import argparse

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

def description_evaluation(description_gt, description_extraction):
    return float("{:.2f}".format(calculate_distance(description_gt, description_extraction)/len(description_gt)))

def numerical_evaluation(value_gt, value_extraction):
    """
    neden int çevirdiğini anlat. 60.01 olayını
    """
    if value_gt == "" or value_extraction == "": return ""
    return int(not(convert_to_int(value_gt) == convert_to_int(value_extraction)))

def create_output(extraction, gt, pairs):
        """

        """
        output = gt.copy()
        output.rename({"Description": "Description_GT","Quantity":"Quantity_GT", "Unit price":"Unit price_GT", "Total price":"Total price_GT" }, inplace=True, axis="columns")
        output.insert(loc=2, column="Description_Extraction", value="")
        output.insert(loc=4, column="Quantity_Extraction", value="")
        output.insert(loc=6, column="Unit_price_Extraction", value="")
        output.insert(loc=8, column="Total_price_Extraction", value="")

        output.insert(loc=3, column="Evaluation", value="", allow_duplicates=True)
        output.insert(loc=6, column="Evaluation", value="", allow_duplicates=True)
        output.insert(loc=9, column="Evaluation", value="", allow_duplicates=True)
        output.insert(loc=12, column="Evaluation", value="", allow_duplicates=True)
        
        for pair in pairs:
            if pair[1] >= 0:
                output.at[pair[0],"Description_Extraction"] = extraction["Description"][pair[1]]
                output.iat[pair[0],3] = description_evaluation(gt["Description"][pair[0]], extraction["Description"][pair[1]])
                output.at[pair[0],"Quantity_Extraction"] = extraction["Quantity"][pair[1]]
                output.iat[pair[0],6] = numerical_evaluation(gt["Quantity"][pair[0]], extraction["Quantity"][pair[1]])
                output.at[pair[0],"Unit_price_Extraction"] = extraction["Unit price"][pair[1]]
                output.iat[pair[0],9] = numerical_evaluation(gt["Unit price"][pair[0]], extraction["Unit price"][pair[1]])
                output.at[pair[0],"Total_price_Extraction"] = extraction["Total price"][pair[1]]
                output.iat[pair[0],12] = numerical_evaluation(gt["Total price"][pair[0]], extraction["Total price"][pair[1]])

        return output


if __name__ == "__main__":

    if len(sys.argv) < 3: raise Exception("Please check input format and try again.")

    extraction_file_name = sys.argv[1]
    gt_file_name = sys.argv[2]
    extraction = read_csv(extraction_file_name)
    gt = read_csv(gt_file_name)

    pairs = generate_matches(gt, extraction)
    print(pairs)

    output = create_output(extraction, gt, pairs)
    output.to_csv("output.csv", index=False ,float_format="{:.2f}")
