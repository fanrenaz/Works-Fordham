# -*- coding: utf-8 -*-
import requests
import json
import csv
import random
import re
import time
import urllib3
urllib3.disable_warnings()

def parameters(shopname):
    global url,header
    url = 'https://{}.m.tmall.com'.format(shopname)
    #'''Set your headers here'''
    header = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-us',
            'cookie': 'isg=BKKiGC6yCxXb8xeKYVsKEfbb-SwE86YNYJPsKOw7zpXAv0I51IP2HSg56yXmtB6l; _m_h5_tk=ef2dac56c3c3aa77a99945fa9ef38aac_1575514383191; _m_h5_tk_enc=b0cecd131168d93d14f237ae64ccd74d; _tb_token_=3e5b7e386335; cookie2=136f9022f492aee75e4ac382de4a4115; enc=X1e%2FTa6fXwEp8nx1ipRgLjp3Usw8jd%2F02URjS%2F8e0NsQsbWLKR7HAfVh26NFcyDUoLOaMm080v2ZTQmO9HHE8Q%3D%3D; hng=US%7Czh-CN%7CUSD%7C840; lgc=tb3759555_99; t=b3f472f034ecad985f6f12467e2d3bda; tracknick=tb3759555_99; uc3=id2=UoH%2B4N91JCmkPA%3D%3D&vt3=F8dByua%2BelJpqrx8JXA%3D&lg2=WqG3DMC9VAQiUQ%3D%3D&nk2=F5RGMcgaRhmUEHEz; uc4=nk4=0%40FY4NBLDSAOUBfM8ugnEq%2FH7np6TM78w%3D&id4=0%40UOnhBNzvyt9FV0Dnkk515WxXCFPg; cna=8msyFs+85WICAWwdmaO+OJBj',
            'referer': 'https://uniqlo.m.tmall.com/shop/shop_auction_search.htm?spm=a2141.7631565.0.0.5af8683ajNUqSY&suid=196993935&sort=default',
            "user-agent" : 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/78.0.3904.84 Mobile/15E148 Safari/604.1'
            } 

def create_csv(filename):
    title = ['item_id','price','quantity','sold','title','totalSoldQuantity','url','img','titleUnderIconList']
    with open(filename, "w", encoding="utf-8-sig", newline="") as f:
        csv_f = csv.writer(f)
        csv_f.writerow(title)

def get_pages():
    global totalpage
    num = random.randint(70647199,87739530)
    endurl = '/shop/shop_auction_search.do?sort=s&p=1&page_size=12&from=h5&ajson=1&_tm_source=tmallsearch&callback=jsonp_{}'
    url1 = url + endurl.format(num)
    html = requests.get(url1,headers=header,verify=False).text
    infos = re.findall('\(({.*})\)|$',html)[0]
    infos = json.loads(infos)
    totalpage = int(infos.get('total_page'))

def get_products(page,filename):
    num = random.randint(70647199,87739530)
    endurl = '/shop/shop_auction_search.do?sort=s&p={}&page_size=12&from=h5&ajson=1&_tm_source=tmallsearch&callback=jsonp_{}'
    url2 = url + endurl.format(page,num)
    html = requests.get(url2, headers=header,verify=False).text
    infos = re.findall('\(({.*})\)|$', html)[0]
    infos = json.loads(infos)
    products = infos.get('items')
    title = ['item_id', 'price', 'quantity', 'sold', 'title', 'totalSoldQuantity', 'url', 'img','titleUnderIconList']
    with open(filename, 'a', encoding="utf-8-sig", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=title)
        writer.writerows(products)

def main(filename):
    get_pages()
    for i in range(1,totalpage+1):
        get_products(i,filename)
        print('There are {} pages totally，now the {} page is extracting'.format(totalpage,i))
        time.sleep(5+random.random())
        if i in range(1,90,5):
            time.sleep(5+random.random())

if __name__ == '__main__':
    parameters("uniqlo")
    create_csv("uniqlo_20191229_3am.csv")
    main("uniqlo_20191229_3am.csv")
