"""
Load malicious URL list
"""
import pandas as pd

FILE_PATH = ["dataset/phishtank.csv", "dataset/url_haus.txt"]

def load_malicious_urls():
    # phishtank.csv
    df1 = pd.read_csv(FILE_PATH[0], header=None)
    list1 = df1[1].to_list()[1:]

    # url_haus.txt
    df2 = pd.read_csv(FILE_PATH[1], header=None)
    list2 = df2[2].to_list()

    final_list = list(set(list1 + list2))
    return final_list
