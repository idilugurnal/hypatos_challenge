import pandas as pd
import Levenshtein as ls
import sys
import argparse

MAXD = 3
MAXV = 2

def calculate_distance(str1, str2):
    """
    Calculate the distance between two strings with Levenshtein mode.

    Args:
    str1: First item to be compared
    str2: Second item to be compared

    Returns:
    An integer distance value.
    """

    if str1 == "" or str2 == "": return 1000
    return ls.distance(str(str1), str(str2))

def convert_to_int(value):
    """
    Convert string to int

    Args:
    value: String representation of a float or int value

    Returns:
    Converted integer value
    """

    if value == "": return value
    return(int(float(value)))

def check_match(sample, extraction, matched):

    """
    Check the match of a single line from gt with lines in extraction

    Args:
    sample: Single Dataframe item to be matched
    extraction: Dataframe of extraction list
    matched: A list of already matched lines in extraction file

    Returns:
    Integer index that the sample is matched to.
    -1 represents no match to be found, -2 represents multiple matches to be found and other positive integers represent index of the single match found in extraction dataframe
    """

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
    """
    Generate a list of tuples matching ground truth line items with their extraction matches

    Args:
    gt: ground truth data frame
    extraction: extraction dataframe

    Returns:
    A list of tuples 
    Ex: [(0,0),(1,-1)] -> This means 0th line in gt is matched with 0th line in extraction and 1st line in gt has no match.
    """
    
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
    """
    Read csv and convert it to pandas dataframe

    Args:
    filename: Name of csv to be read

    Returns:
    Converted dataframe
    """

    df = pd.read_csv(filename, usecols=["File_name", "Description", "Quantity", "Unit price", "Total price"], keep_default_na=False)
    return df

def description_evaluation(description_gt, description_extraction):
    return float("{:.2f}".format(calculate_distance(description_gt, description_extraction)/len(description_gt)))

def numerical_evaluation(value_gt, value_extraction):
    """
    Evaluate the accuracy of numerical items such as quantity, unit price and total price
    Convert values to int first for accurate evaluation
    For example: 60.01 is converted to 60

    Args:
    value_gt: Numerical value from gt
    value_extraction: Numerical value from extraction

    Returns:
    Integer value (binary 0 or 1) representing 0 for success and 1 for failure to be written to csv
    """

    if value_gt == "" or value_extraction == "": return ""
    return int(not(convert_to_int(value_gt) == convert_to_int(value_extraction)))

def create_output(extraction, gt, pairs):

    """
    Create output csv file

    Args:
    extraction: extraction dataframe
    gt: ground truth dataframe
    pairs: list of tuples representing matched lines of gt to extraction

    Returns:
    Output dataframe
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

    parser = argparse.ArgumentParser(description='Accuracy measurement of line items ')
    parser.add_argument('-e', action="store_true", default="Extraction.csv", help="Extraction file name", required=False, dest="extraction")
    parser.add_argument('-gt', action="store_true", default="GT Ground Truth.csv", help="Ground Truth file name", required=False, dest="gt")
    parser.add_argument('-o', action="store_true", default="output.csv", help="Output file name", required=False, dest="output")

    args = parser.parse_args()

    extraction_file_name = args.extraction
    gt_file_name = args.gt
    extraction = read_csv(extraction_file_name)
    gt = read_csv(gt_file_name)

    pairs = generate_matches(gt, extraction)
    #print(pairs)

    output = create_output(extraction, gt, pairs)
    output.to_csv(args.output, index=False ,float_format="{:.2f}")
