import requests
from lxml import etree
import re
import json
import csv
import urllib3
urllib3.disable_warnings()


def get_detail(url, price, comment, sell, name):
    headers = {
        'Host': 'item.taobao.com',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleW'
                      'ebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
        'accept-encoding': 'gzip, deflate, br',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0'
                  '.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Connection': 'keep-alive',
        'accept-language': 'zh,zh-CN;q=0.9,en;q=0.8',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'Referer': 'https://item.taobao.com/item.htm?',
        'upgrade-insecure-requests': '1'
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

    return detail


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
        'referer': 'https://tone-elegancy.taobao.com/search.htm?spm=a1z10.3-c-s.w4002-21033524803.27.'
                   '65ce37c5uGhdMU&_ksTS=1570139708311_205&callback=jsonp206&mid=w-21033524803-0&wid=210'
                   '33524803&path=%2Fsearch.htm&search=y&orderType=hotsell_desc&pageNo=3',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
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
    for page in range(1, 19):
        print("正在获取 第 {} 页".format(page))
        url = "https://tone-elegancy.taobao.com/i/asynSearch.htm?_ksTS=1570037877033_219&" \
              "mid=w-21033524803-0&wid=21033524803&path=/search.htm&" \
              "search=y&orderType=hotsell_desc&pageNo={}".format(page)
        resp = download(url)
        text = resp.text.replace('\\"', '"')
        selector = etree.HTML(text)

        for item in selector.xpath('//dl[starts-with(@class,"item ")]'):
            yield ["https:" + item.xpath('.//a[@class="J_TGoldData"]')[0].attrib["href"],
                   item.xpath('string(.//span[@class="c-price"])'),
                   item.xpath('string(.//span[@class="sale-num"])'),
                   item.xpath('string(.//h4//span)'),
                   item.xpath('string(.//a[@class="item-name J_TGoldData"])').strip()]


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
    for item_url, price, sell, comment, name in get_items():
        # print(item_url, price, sell, comment, name)
        data = get_detail(item_url, price, comment, sell, name)
        #print(data)
        save_data(data)


if __name__ == '__main__':
    #The following cookies should be collected manually
    cookies = ""
    file_name = "XIAOCHONG items.csv"
    # csv column names
    head = ['链接', '标题', '评论数', '价格', '销量', '图片链接', '品牌', '适用年龄', '尺码', '面料', '图案', '风格',
            '通勤', '领子', '衣门襟', '颜色分类', '袖型', '组合形式', '货号', '成分含量', '上市年份/季节',
            '袖长', '款式', '厚薄', '衣长', '服装版型']
    main()

