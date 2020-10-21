import unittest
from comparison_service import *
import os
import pandas as pd


class TestComparisonService(unittest.TestCase):

    def setUp(self):
        os.system("python3 comparison_service.py")
        self.extraction = pd.read_csv("Extraction.csv", usecols=["File_name", "Description", "Quantity", "Unit price", "Total price"], keep_default_na=False)
        self.gt = pd.read_csv("GT Ground Truth.csv", usecols=["File_name", "Description", "Quantity", "Unit price", "Total price"], keep_default_na=False)
    
    def test_calculate_distance(self):
        self.assertEqual(calculate_distance("50" , "51") , 1)
        self.assertEqual(calculate_distance("basic service" , "basicservic") , 2)
    
    def test_convert_to_int(self):
        self.assertEqual(convert_to_int("50.01") , 50)
        self.assertEqual(convert_to_int("") , "")
    
    def test_check_match(self):
        self.assertEqual(check_match(self.gt.iloc[0] , self.extraction) , 0)
        self.assertEqual(check_match(self.gt.iloc[2] , self.extraction) , -2)
    
    def test_generate_matches(self):
        result = [(0,0), (1,1), (2,-2), (3,4), (4,5)]
        self.assertEqual(generate_matches(self.gt, self.extraction), result)
    
    def test_description_evaluation(self):
        self.assertAlmostEqual(description_evaluation(self.gt.iloc[0].Description, self.extraction.iloc[0].Description) , 0.06)

    def test_numerical_evaluation(self):
        self.assertEqual(numerical_evaluation(20 , 21), 1)
        self.assertEqual(numerical_evaluation(20.2 , 20), 0)
        self.assertEqual(numerical_evaluation(20.8 , 21), 1)




if __name__ == '__main__': 
    unittest.main() 