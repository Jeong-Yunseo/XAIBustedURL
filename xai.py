import numpy as np
import pandas as pd
from lime.lime_text import LimeTextExplainer
import random

# load BustedURL model
from src.ensemble_model import EnsembleModel

MODEL_PATH = "models/ensemble_model.pkl"
model = EnsembleModel()
model.load_model(MODEL_PATH)

class_names = ["benign", "malicious"]

# LIME: prediction wrapper function
def predict_proba(texts):
    """
    input: several text list
    return: 2D probability value
    """

    preds = []
    for t in texts:
        feats = model.extract_features([t])
        p = model.classify_proba(feats)[0]
        preds.append(p)

    return np.array(preds)

# initiate LIME Explainer
explainer = LimeTextExplainer(
    class_names=["benign", "malicious"],
    split_expression=r"(?<=/)|(?<=\.)|(?<=-)|(?<=\?)|(?<=\=)|(?<=:)",
    bow=True
)

# Explanation function
def explain_url(url):
    """
    input URL -> print explanation based on LIME
              -> show important substrings
    """

    print(f'\n[+] URL: {url}')
    print('[+] Generating explanation...')

    exp = explainer.explain_instance(
            url,
            predict_proba,
            num_features=6,
            top_labels=1
        )

    # print text
    print('\n=== LIME Explanation (Top Features) ===')
    label_to_use = exp.available_labels()[0]
    for feature, weight in exp.as_list(label=label_to_use):
        print(f'{feature:30s}: {weight:.4f}')

    try:
        return exp.show_in_notebook(text=True)
    except:
        return exp.save_to_file("lime_explanation.html")

# urls from csv
FILE_PATH = "dataset/urldata.csv"

def get_urls():
    df = pd.read_csv(FILE_PATH, header=None)
    df = df.dropna().reset_index(drop=True)
    df = df.drop(df.columns[0], axis=1)
    df = df.drop(df.columns[1], axis=1)
    df.columns = ['url', 'label']
    url_list = df['url'].to_list()
    random.shuffle(url_list)

    return url_list

# RUN
if __name__=="__main__":
    url_list = get_urls()
    for url in url_list:
        explain_url(url)
