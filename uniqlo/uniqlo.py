# -*- coding: utf-8 -*-
import requests
import json
import csv
import random
import re
import time

def parameters(shopname):
    global url,header
    url = 'https://{}.m.tmall.com'.format(shopname)
    #'''Set your headers here'''
    header = {
            'accept': '*/*',
            'accept-encoding': '*/*',
            'accept-language': '*/*',
            'cookie': '*/*',
            'referer': '*/*',
            "user-agent" : '*/*'
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

if __name__ == '__main__':
    parameters("uniqlo")
    create_csv("uniqlo.csv")
    main("uniqlo.csv")
