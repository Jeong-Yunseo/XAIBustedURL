"""
Load domain lists from CSV files
"""
import pandas as pd

FILE_PATH = ["dataset/alexa_top_1M.csv", "dataset/majestic_million.csv"]

def load_final_list():
    df1 = pd.read_csv(FILE_PATH[0], header=None)
    list1 = df1[1].to_list()

    df2 = pd.read_csv(FILE_PATH[1], header=None)
    list2 = df2[2].to_list()[1:]

    final_list = list(set(list1 + list2))
    return final_list
