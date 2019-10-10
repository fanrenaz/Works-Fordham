import pandas as pd
import requests

def download_img(img_url, file_name):
    resq = requests.get(img_url)
    with open(file_name, "wb") as f:
        f.write(resq.content)
        
def get_img(ori_file):
    df = pd.read_csv(ori_file,encoding="utf-8")
    for i in range(len(df)):
        file_name = "{}.jpg".format(i)
        img_url = df.loc[i, "图片链接"].split("\n")
        n = len(img_url)
        for x in range(n):
            url = img_url[x]
            file_name = "{}({}).jpg".format(i,x)
            try:
                download_img(url, file_name)
            except:
                url = "http:"+url
                download_img(url, file_name)
                #If only one picture per item is enough:
                #break

if __name__ == '__main__':
    get_img("XIAOCHONG items.csv")
    