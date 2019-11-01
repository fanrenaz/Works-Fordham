# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 20:19:40 2019

@author: Yifan Ren
"""


import pandas as pd

import requests,re,json
import csv
def getHouseNumber(url):
    html = requests.get(url)
    data=html.text
    #构造正则，获取remarketing_ids
    urlbase=re.search('"remarketing_ids":\[(.*?)\],',data)
 
    #将其放入一个列表return回去主函数
    url=[]
    urlNumber=''
    for each in urlbase.group(1):
        if each==",":
            url.append(urlNumber)
            urlNumber=''
        else:
            urlNumber=urlNumber+each
 
    return url
 
 
def getHouseInformation(urlNumber):
    Url = 'https://zh.airbnb.com/api/v2/pdp_listing_details/' + str(urlNumber) + '?_format=for_rooms_show&adults=1&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&'
    html=requests.get(Url)
    data = json.loads(html.text)
    #房主
    House_owner=data['pdp_listing_detail']['user'].get('host_name')
    #价格
    price_url='https://zh.airbnb.com/api/v2/pdp_listing_booking_details?force_boost_unc_priority_message_type=&guests=1&listing_id='+ str(urlNumber) +'&show_smart_promotion=0&_format=for_web_dateless&_interaction_type=pageload&_intents=p3_book_it&_parent_request_uuid=4527592d-6c3c-4b64-9c40-b814fb4ca733&_p3_impression_id=p3_1547785606_MzQbhXiFnlGGppGx&number_of_adults=1&number_of_children=0&number_of_infants=0&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&currency=USD&locale=en'
    price_html = requests.get(price_url)
    price_data = json.loads(price_html.text)
    price=price_data['pdp_listing_booking_details'][0]['rate_with_service_fee'].get('amount_formatted')
    '''#房源介绍
    Introduction_housing=data['pdp_listing_detail']['sectioned_description'].get('description')'''
    #位置
    Position=data['pdp_listing_detail'].get('location_title')
    #房名
    HouseName=data['pdp_listing_detail'].get('name')
    # 评论
    '''Commen = ''
    for each in range(100):
        CommenUrl = 'https://zh.airbnb.com/api/v2/reviews?key=d306zoyjsyarp7ifhu67rjxn52tv0t20&currency=USD&locale=en&listing_id='+str(urlNumber)+'&role=guest&_format=for_p3&_limit=7&_offset=' + str(each * 7) + '&_order=language_country'
        CommenHtml=requests.get(CommenUrl)
        if CommenHtml.status_code==200:
            Commendata = json.loads(CommenHtml.text)
            for i in Commendata['reviews']:
                Commen = Commen + i.get('comments') + '\n'
        else:
            break'''
    ALL_Information=[]
    ALL_Information.append(HouseName)
    ALL_Information.append(House_owner)
    ALL_Information.append(price)
    #ALL_Information.append(Introduction_housing)
    ALL_Information.append(Position)
    #ALL_Information.append(Commen)
 
    return ALL_Information
 
 
def main(i):
    HouseNumberUrl="https://zh.airbnb.com/api/v2/explore_tabs?version=1.4.5&satori_version=1.1.3&_format=for_explore_search_web&experiences_per_grid=20&items_per_grid=18&guidebooks_per_grid=20&auto_ib=false&fetch_filters=true&has_zero_guest_treatment=true&is_guided_search=true&is_new_cards_experiment=true&luxury_pre_launch=true&query_understanding_enabled=false&show_groupings=true&supports_for_you_v3=true&timezone_offset=480&client_session_id=fb9116ef-5573-43c3-a864-68f9c4b04813&metadata_only=false&is_standard_search=true&refinement_paths%5B%5D=%2Fhomes&selected_tab_id=home_tab&adults=0&children=0&infants=0&toddlers=0&place_id=ChIJdd4hrwug2EcRmSrV3Vo6llI&allow_override%5B%5D=&s_tag=BoUbRf3d&section_offset=4&items_offset="+str(i)+"&screen_size=large&query=London%2C%20United%20Kingdom&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&currency=USD&locale=en"
    out = open('Stu_csv.csv', 'a', newline='', encoding='utf-8-sig')
    csv_write = csv.writer(out, dialect='excel')
    n=0
    for number in getHouseNumber(HouseNumberUrl):
        n+=1
        stu2=getHouseInformation(number)
        csv_write.writerow(stu2)
        #每爬取一个完整的房源信息，就输出一次write over
        print(n,"write over")
 
 
 
if __name__ == '__main__':
 
    stu1 = ['Title', 'Host', 'Price',  'Location']
    out = open('Stu_csv.csv', 'a', newline='', encoding='utf-8-sig')
    csv_write = csv.writer(out, dialect='excel')
    csv_write.writerow(stu1)
    for i in range(18):
        main(i)