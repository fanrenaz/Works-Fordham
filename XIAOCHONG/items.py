import requests
from lxml import etree
import re
import json
import csv
import urllib3
import random
import time
urllib3.disable_warnings()

#This method was banned
'''def get_detail(url, price, comment, sell, name):
    id_=url.split('?')[1]
    headers = {
        'Host': 'item.taobao.com',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36',
        'accept-encoding': 'gzip, deflate, br',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Connection': 'keep-alive',
        'accept-language': 'zh,zh-CN;q=0.9,en;q=0.8',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'Referer': 'https://item.taobao.com/item.htm?',
        'upgrade-insecure-requests': '1',
        'path': '/item.htm?{}'.format(id_)
    }
    resp = requests.get(url, headers=headers, verify=False)
    # Re for images
    imgs = re.findall('auctionImages.+?(\[.+?\])', resp.text, re.S)[0]
    imgs = json.loads(imgs)
    # Xpath for details
    selector = etree.HTML(resp.text)
    detail = dict()

    detail["图片链接"] = "\n".join(imgs)
    detail["链接"] = url
    detail["评论数"] = comment
    detail["价格"] = price
    detail["销量"] = sell
    detail["标题"] = name

    for li in selector.xpath('//ul[@class="attributes-list"]/li'):
        if "年份" in li.xpath('string(.)').split(": ")[0]:
            key = '上市年份/季节'
        else:
            key = li.xpath('string(.)').split(": ")[0]
        detail[key] = li.xpath('string(.)').split(": ")[1]

    return detail'''


def download(url):
    global cookies
    headers = {
        'accept': 'text/javascript, application/javascript, application/ecmascript, '
                  'application/x-ecmascript, */*; q=0.01',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh,zh-CN;q=0.9,en;q=0.8',
        'cache-control': 'no-cache',
        'cookie': cookies,
        'pragma': 'no-cache',
        'referer': 'https://tone-elegancy.taobao.com/search.htm?_ksTS=1573362355814_209&callback=jsonp210&mid=w-21033524803-0&wid=21033524803&path=%2Fsearch.htm&search=y&orderType=hotsell_desc&pageNo=1',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }
    resp = requests.get(url, headers=headers, verify=False)
    if "asynSearch.htm/_____tmd_____/punish" in resp.text:
        cookies = input("出现验证码， 在浏览器查询复制Cookies\n")
        return download(url)
    else:
        return resp


def get_items():
    #loops only 18 times because the shop has 18 pages of items
    for page in range(1, 28):
        print("正在获取 第 {} 页".format(page))
        url = "https://tone-elegancy.taobao.com/i/asynSearch.htm?_ksTS=1573363505921_227&callback=jsonp228&" \
              "mid=w-21033524803-0&wid=21033524803&path=/search.htm&" \
              "search=y&orderType=hotsell_desc&pageNo={}".format(page)
        resp = download(url)
        text = resp.text.replace('\\"', '"')
        selector = etree.HTML(text)

        for item in selector.xpath('//dl[starts-with(@class,"item ")]'):
            t=item.xpath('string(.//a[@class="item-name J_TGoldData"])').strip()
            yield ["https:" + item.xpath('.//a[@class="J_TGoldData"]')[0].attrib["href"],
                   item.xpath('string(.//span[@class="c-price"])'),
                   item.xpath('string(.//span[@class="sale-num"])'),
                   item.xpath('string(.//h4//span)'),
                   item.xpath('string(.//a[@class="item-name J_TGoldData"])').strip(),
                   "https:"+item.xpath('.//img[@alt="{}"]'.format(t))[0].attrib["src"]]


def create_csv():
    with open(file_name, "w", encoding="utf-8-sig", newline="") as f:
        csv_f = csv.writer(f)
        csv_f.writerow(head)


def save_data(data):
    with open(file_name, "a", encoding="utf-8-sig", newline="") as f:
        csv_f = csv.writer(f)
        csv_f.writerow([data.get(key) for key in head])


def main():
    create_csv()
    for item_url, price, sell, comment, name, img_url in get_items():
        # print(item_url, price, sell, comment, name)
        #data = get_detail(item_url, price, comment, sell, name)
        detail = dict()
        detail["item_url"] = item_url
        detail["title"] = name
        detail["img_url"] = img_url
        detail["price"] = price
        detail["sell"] = sell
        detail["comment"] = comment
        #print(data)
        save_data(detail)


if __name__ == '__main__':
    #The following cookies should be collected manually
    cookies = "t=62c827ae4a0d7e4d3b1471162a6ed67b; cna=tJtLFsdv0BoCAWwdmaPgpfgS; lgc=tb3759555_99; tracknick=tb3759555_99; tg=0; _m_h5_tk=cdfe06f8181fc833a483ed21a06b1889_1573368141911; _m_h5_tk_enc=b38455db2e2bdd4e087a4f8e475e987a; _fbp=fb.1.1573360582222.1983353015; hng=CN%7Czh-CN%7CCNY%7C156; thw=cn; uc3=nk2=F5RGMcgaRhmUEHEz&lg2=V32FPkk%2Fw0dUvg%3D%3D&vt3=F8dByua%2BelR%2BVwM5W%2B4%3D&id2=UoH%2B4N91JCmkPA%3D%3D; uc4=id4=0%40UOnhBNzvyt9FV0Dnkk515WxV%2FPmy&nk4=0%40FY4NBLDSAOUBfM8ugnEq%2FH7np6bLjh4%3D; _cc_=WqG3DMC9EA%3D%3D; enc=6Lxi3eHI5wfPzuATFNksbgQG%2Bq%2BG7LYg3wBoWo9zyzHpzSMRepODM99Jg514BWW3zbWoBNCtipHwlhM8ycRpwA%3D%3D; mt=ci=1_1; pnm_cku822=121%23phnlkp4aPcMlVlaAEFhPllXYec%2FfKujVlGuLxb%2FIoO7pKIsru9D5lwLYAcFfKujVlmgY%2BzpIDMlSA3rJEzegbIRNLaffDuQllGgYxzC5KMlVA3rnEkDIll9YOcFfKujVlmuY%2BzpIDM9lA3JnEGD5xfNSctmylmYgebP6MqSJan40COe2CpxSp2ibk65T8uBhbgi0CeHXFt8bbZi0JjdeN4jVCZe4GG%2FmbgiekHIaFtFbbZsbnjxSpXb0k65T8uBhbZs0CeHXF9WbCZsbnMxyp2D0CZeTEuYGM11zFNqzQ17lC6W3nnC9Jw9l4IYDt5Wche%2FlPzO8%2BRwxFRzqADGsx%2B9Tohz7TVw2JvAzYggQNvJm%2B9gzY4icPOe046fBj1WGyJxXkWR%2BUmKFgyEGkErZgP9Q6OB9j2BqyJ%2FVPT9EpVWc8SbUc6j6phtpe3xQfnm%2FvePn4L5yDX8TVIYSg0M%2BXzau22N1cJiuHmqEmqp1WZ2JDQcQztQ%2Fjz3jtkOTd%2Fj%2FDGrBpVbH3hqPycSXRBt%3D; l=dBa_oTOnqZgmtviABOCwourza77OSIRAguPzaNbMi_5N16L1X1QOkC_wtFp6VxWfG9YB47_ypVw9-etkiMBaxzv-eZDnKxDc.; isg=BLOzZyuo6pOC7qZK-9rlfR4tQrfd6EeqOY8wyGVQD1IJZNMG7bjX-hHyHsQvRJ-i"
    file_name = "xiaochong_20191229_3am.csv"
    # csv column names
    '''head = ['链接', '标题', '评论数', '价格', '销量', '图片链接', '品牌', '适用年龄', '尺码', '面料', '图案', '风格',
            '通勤', '领子', '衣门襟', '颜色分类', '袖型', '组合形式', '货号', '成分含量', '上市年份/季节',
            '袖长', '款式', '厚薄', '衣长', '服装版型']'''
    head = ['item_url','title','img_url','price','sell','comment']
    main()

