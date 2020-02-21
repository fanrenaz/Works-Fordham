# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 23:22:30 2020

@author: Yifan Ren
"""

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
