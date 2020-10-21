# Hypatos Coding Challenge

## How to run the code:

### Packages to Install before Running:

- [pandas](https://pandas.pydata.org) -> pip install pandas
- [Levenshtein](https://pypi.org/project/python-Levenshtein/) -> pip install python-Levenshtein
- [argparse](https://docs.python.org/3/library/argparse.html) -> pip install argparse

**OR**

Run the following command when in the same directory with the code:

> pip install -r requirements.txt

### Run:

You should have python version 3.6+

> python main.py -gt *\<ground_truth_file_name\>* -e *\<extraction_file_name\>* -o *\<output_file_name\>*

You can see the inputs and their explanation by running:

> python main.py --help

All inputs have default values which are:

- extraction: Extraction.csv
- ground truth : GT Ground Truth.csv
- output: output.csv

The output will be created in the same directory as the code with the output name given. 


## Challenge Description

To summarize, the challenge asks us to compare the extraction file, which is generated by hypatos model that extracts data from documents,
with the ground truth and measure accuracy for the line items.

## Challenge Solution Steps

### 1. Match each line item in the ground truth file with an item in the extraction file 

For each line item in ground truth the following is checked:
The file name of line item in gt must be equal to the file name of the line item in extraction, if this is satisfied,


    1. The description of the line item in gt is compared to the description of the line item in extraction, if they are equal a match occurs


    2. Else if the description of the line item in gt has a calculated distance that is less than MAXD with the description of the line item in extraction AND quantity, total price, unit price of ground truth line item all have a calculated distance that is less than MAXV compared to quantity, total price, unit price of extraction line item, a match occurs.

    
    3. Else a match does not occur.

If not match occurs -1 is returned.
If more than one match occurs -2 is returned.
If a single match occurs the line index of the extraction match is returned.

### 2. Compare matched items 

Levenshtein distance comparison is used for string items.
For numerical items, first the numerical value is converted to integer and then converted back to string. Finally, Levenshtein distance is used for comparison.

### 3. Evaluation

For quantity, unit price and total price, the values are converted to integer and then they are compared with Levenshtein distance. If the compared values are equal (distance = 0), the evaluation value is 0, else the value is 1 (distance > 0).

For Description, the following evaluation is used:
- Levenshtein distance between gt and extraction description item / length of gt description item