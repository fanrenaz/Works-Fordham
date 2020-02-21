import json
import pandas as pd
import math
from sklearn import preprocessing
import os
from multiprocessing.dummy import Pool as ThreadPool
import warnings
warnings.filterwarnings('ignore')

def extract_node_text(i):
    try:
        i = i.get("edges")[0].get("node").get("text")
    except:
        pass
    return i

def tag_join(l):
    try:
        l = ",".join(l)
    except: pass
    return l

def json_to_df(file):
    with open(file, 'r') as f:
        js = json.load(f)
    df = pd.DataFrame(js["GraphImages"])
    df["dimensions"] = df["dimensions"].map(lambda line: str(line.get("height"))+"*"+str(line.get("width")))
    df["edge_liked_by"] = df["edge_liked_by"].map(lambda line: line.get("count"))
    df["edge_media_preview_like"] = df["edge_media_preview_like"].map(lambda line: line.get("count"))
    df["edge_media_to_caption"] = df["edge_media_to_caption"].map(extract_node_text)
    df["edge_media_to_comment"] = df["edge_media_to_comment"].map(lambda line: line.get("count"))
    df["owner"] = df["owner"].map(lambda line: line.get("id"))
    df["tags"] = df["tags"].map(tag_join)
    df["comments_disabled"] = df["comments_disabled"].map(lambda x: None if math.isnan(x) is True else x)
    df["video_view_count"] = df["video_view_count"].map(lambda x: x if type(x)==float else None)
    return df

def save_csv(df, to_path, focus_only=False):
    if focus_only == False:
        return df.to_csv(to_path,encoding="utf_8_sig",index=False)
    elif focus_only == True:
        df = df[["edge_liked_by","edge_media_to_comment","taken_at_timestamp"]]
        df["utcdate"] = pd.to_datetime(df["taken_at_timestamp"].values, utc=True,unit='s').to_period("D")
        x = df.set_index("utcdate").drop(columns="taken_at_timestamp").values #returns a numpy array
        min_max_scaler = preprocessing.MinMaxScaler()
        x_scaled = min_max_scaler.fit_transform(x)
        df[["nd_like","nd_comment"]] = pd.DataFrame(x_scaled)
        return df.to_csv(to_path,index=False)
    
def get_names(ls):#Please use your personal name list, this is only an example
    name_list = []
    for n in ls:
        name_list.append(n.split("/")[-2])
    return name_list

#focus_only
def process_js_csv(name):
    source = "./data/"+name+".json"
    dest = "./data/csv/"+name+"_focus"+".csv"
    try:
        save_csv(json_to_df(source),dest,focus_only=True)
    except:
        print("Failed in {}".format(name))

if __name__ == "__main__":
    ls = ['gs://fashionaiins/baggypants/']#use your own names list to deal with
    save_pool = ThreadPool()
    save_pool.map(process_js_csv, get_names(ls))
    save_pool.close()
    save_pool.join()
