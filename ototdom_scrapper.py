# -*- coding: utf-8 -*-
# importing libriries
import requests
from bs4 import BeautifulSoup
import json
import math
import re
import pandas as pd

#%% defining functions
# defining function that generate all pages with offers
def loop_sales_pages(sales_rent):
    if not(sales_rent in ['wynajem', 'sprzedaz']):
        print('Wrong listing type')
        exit()
    otodom_main_link = "https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/cala-polska?limit=100&page={}".format(sales_rent)
    otodom_request = requests.get(otodom_main_link)
    soup_read = BeautifulSoup(otodom_request.text,'html.parser')
    offer_count_element = soup_read.select('html body div#__next div.css-13o7eu2.ee6kzq25 main.css-lmlup0.e1d07yf20 div.css-10esakf.ee6kzq27 div.css-172356e.ee6kzq22 div.css-ej90lz.eeki05l7 div.css-di5c3h.eeki05l4 div.css-u8mcic.e1ia8j2v6 strong.css-35ezg3.e1ia8j2v5 span.css-klxieh.e1ia8j2v3')
    sales_offer_count = offer_count_element[0].text.strip()
    page_count = math.ceil(int(sales_offer_count)/100)
    offer_pages = []
    for i in range(1,page_count+1, 1):
        otodom_link = "https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/cala-polska?limit=100&page={}".format(i)
        offer_pages.append(otodom_link)
    return offer_pages

# defining function that extract all offer links 

def get_offer_links(pages_list):
    offers_links_list = []
    for link in pages_list:
        request_item = requests.get(link)
        soup_item = BeautifulSoup(request_item.content, 'html.parser')
        for i in soup_item.find_all("li"):
            next_element = i.next_element
            if next_element.has_attr("data-cy") and next_element.get("data-cy") == 'listing-item-link':
                offers_links_list.append(next_element.get('href'))
    return offers_links_list

# defining function that go through all offer URL and return dictionary with offer details
def offer_details_read (offer_url_list):
    Offer_details_dic = {'Area':[], 'Build_year':[], 'Building_floors_num':[], 'Building_material':[], 
           'Building_ownership':[], 'Building_type':[], 'City':[], 'Country':[], 'Extras_types':[], 
          'Floor_no':[], 'Heating':[], 'MarketType':[], 'Media_types':[], 'OfferType':[], 'Price_per_m':[], 
           'ProperType':[], 'Rooms_num':[], 'Subregion':[], 'env':[], 'Offer_id':[], 'Offer_url':[]}
    
    
    for url in offer_url_list:
        url_full = r'https://www.otodom.pl' + url
        request_result = requests.get(url_full)
        if request_result.status_code == '200':
            continue
        offer_soup = BeautifulSoup(request_result.content, 'html.parser')
        offer_html = str(offer_soup.find_all("script",  type="application/json"))
        re_pattern = """target":{(.*)topInformation"""
        if type(re.search(re_pattern,offer_html)) != re.Match:
            continue
        offer_details = re.search(re_pattern,offer_html).group()[10:]
        details_edited = offer_details.replace(',',', ').replace('''"''','')
        
        area_re = re.compile(r'Area:\[?(\d*.\d*)')
        Offer_details_dic['Area'].append(area_re.search(details_edited))

        Build_year_re = re.compile(r'Build_year:\[?(\d*),')
        Offer_details_dic['Build_year'].append(Build_year_re.search(details_edited))

        Building_floors_num_re = re.compile(r'Building_floors_num:\[?(\d*)')
        Offer_details_dic['Building_floors_num'].append(Building_floors_num_re.search(details_edited))

        Building_material_re = re.compile(r'Building_material:\[?(\w*)\]?')
        Offer_details_dic['Building_material'].append(Building_material_re.search(details_edited))                

        Building_ownership_re = re.compile(r'Building_ownership:\[?(\w*)\]?')
        Offer_details_dic['Building_ownership'].append(Building_ownership_re.search(details_edited))

        Building_type_re = re.compile(r'Building_type:\[?(\w*)\]?')
        Offer_details_dic['Building_type'].append(Building_type_re.search(details_edited))

        City_re = re.compile(r'City:\[?(\w*)\]?')
        Offer_details_dic['City'].append(City_re.search(details_edited))

        Country_re = re.compile(r'Country:\[?(\w*)\]?')
        Offer_details_dic['Country'].append(Country_re.search(details_edited))

        Extras_types_re = re.compile(r'(?<=Extras_types:\[)(.*?)(?=\])')
        Offer_details_dic['Extras_types'].append(Extras_types_re.search(details_edited))

        Floor_no_re = re.compile(r'Floor_no:\[?(\w*)\]?')
        Offer_details_dic['Floor_no'].append(Floor_no_re.search(details_edited))

        Heating_re = re.compile(r'Heating:\[?(\w*)\]?')
        Offer_details_dic['Heating'].append(Heating_re.search(details_edited))

        id_re = re.compile(r' Id:\[?(\d*)]?')
        Offer_details_dic['Offer_id'].append(id_re.search(details_edited))

        MarketType_re = re.compile(r' MarketType:\[?(\w*)\]?')
        Offer_details_dic['MarketType'].append(MarketType_re.search(details_edited))

        Media_types_re = re.compile(r'(?<=Media_types:\[)(.*?)(?=\])')
        Offer_details_dic['Media_types'].append(Media_types_re.search(details_edited))

        OfferType_re = re.compile(r'OfferType:\[?(\w*)\]?')
        Offer_details_dic['OfferType'].append(OfferType_re.search(details_edited))

        Price_per_m_re = re.compile(r'Price_per_m:\[?(\d*)\]?')
        Offer_details_dic['Price_per_m'].append(Price_per_m_re.search(details_edited))

        ProperType_re = re.compile(r'ProperType:\[?(\d*)\]?')
        Offer_details_dic['ProperType'].append(ProperType_re.search(details_edited))

        Rooms_num_re = re.compile(r'Rooms_num:\[?(\d*)\]?')
        Offer_details_dic['Rooms_num'].append(Rooms_num_re.search(details_edited))

        Subregion_re = re.compile(r'Subregion:\[?(\w*-?\w+)\]??')
        Offer_details_dic['Subregion'].append(Subregion_re.search(details_edited))

        env_re = re.compile(r'env:\[?(\w*)\]?')
        Offer_details_dic['env'].append(env_re.search(details_edited))
        
        Offer_details_dic['Offer_url'].append(url)
        
    for key in Offer_details_dic.keys():
        key_values = []
        for value in Offer_details_dic.get(key):
            if type(value) == re.Match:
                key_values.append(value.group(1))
            elif type(value) == str:
                key_values.append(value)
            else:
                key_values.append('NA')
        Offer_details_dic[key] = key_values
    Offer_details_df = pd.DataFrame(Offer_details_dic)
    return Offer_details_df

# get all offer links
# %% get all pages
rent_offer_pages = loop_sales_pages('wynajem')
sales_offer_pages = loop_sales_pages('sprzedaz')

# %% get offer url
sales_offer_url_links = get_offer_links(sales_offer_pages)
rent_offer_url_links = get_offer_links(rent_offer_pages)
sales_offer_url_links = list(set(sales_offer_url_links))
rent_offer_url_links = list(set(rent_offer_url_links))

# %% get offer details pandas data frame
#looping through offers and extracting data to dataframe

sales_offer_df = offer_details_read(sales_offer_url_links)
rent_offer_df = offer_details_read(rent_offer_url_links)


# %% save dataframce locally

from datetime import date
sales_offer_df.to_json(r'C:\Users\Piniusz\Documents\Projekty\otodom webscrapping\data\rent_offers_18092021.json')
rent_offer_df.to_json(r'C:\Users\Piniusz\Documents\Projekty\otodom webscrapping\data\rent_offers_{}.json')













