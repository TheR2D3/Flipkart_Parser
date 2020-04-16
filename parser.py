#Import necessary functions

import numpy as np
import string
import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
from operator import add
from operator import iconcat
import functools

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

#Function to decode URLs
def getURLs(main_url):

    #Get the total pages of review
    response = requests.get(main_url, headers=headers)
    soup = BeautifulSoup(response.content, features="lxml")

    total_pages = soup.find_all("div", class_="_2zg3yZ _3KSYCY")[0]
    total_pages_count = total_pages.find_all("span")[0].get_text().split()[3]
    #Page nos have comma, so removing the comma
    total_pages_count = int(re.sub(",","",total_pages_count))
    
    #Generate pages having review URLs
    review_urls = []    
    for n in range(1,total_pages_count):
        review_urls.append(main_url+'&page='+str(n))
    return(review_urls)

#Function to get various objects
def get_objects(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, features="lxml")
    
    #Review text
    review = soup.find_all("div", class_="qwjRop")

    #Review Heading
    review_heading_obj = soup.find_all("p", class_="_2xg6Ul")

    #Star rating
    #star_count_obj=soup.find_all("div", class_="hGSR34 E_uFuv")
    star_count_obj = soup.find_all("div", class_="col _390CkK _1gY8H-")
    
    return(soup,review,review_heading_obj,star_count_obj)

#Function to get various ratings.
def get_ratings(star_count_obj):
    
    x=[]
    y=[]
    z=[]
    a=[]
    b=[]
    c=[]
    p=[]
    high_star_val=[]
    star_count_list=[]

    #Get the divs for each star as each star has a different class value.
    for temp in star_count_obj:
        two_star = temp.find_all("div",class_="hGSR34 _1x2VEC E_uFuv")
        one_star = temp.find_all("div",class_="hGSR34 _1nLEql E_uFuv")
        high_star = temp.find_all("div",class_="hGSR34 E_uFuv")

    #Logic to preserve the order of star ratings in a page.
    #Store the elements of each star value as a list. The list will have elements if respective star is present, else will be empty.    
        x.append(two_star)
        y.append(one_star)
        z.append(high_star)

    #If the list is empty, populate the position as 0, else populate with star value
    for temp in x:
        if temp:
            a.append(2)
        else:
            a.append(0)

    for temp in y:
        if temp:
            b.append(1)
        else:
            b.append(0)

    for temp in z:
        if temp:
            p.append(temp)
        else:
            p.append(0)

    #Since 3,4, and 5 stars have common class, we need to further drill down the star ratings from text.
    for temp in p:
        if temp:
            new_string = str(temp)
            high_star_val.append(int(new_string[28]))
        else:
            high_star_val.append(0)
    
    #Add all the list elements to get star ratings with order preserved.
    my_val = list(map(add,a, b))
    star_count_list = list(map(add,my_val,high_star_val))
    return(star_count_list)

#Populate the details in respective list
def populate_details(star_count_obj,soup,review_heading_obj,review):

    #Parse the required objects    
    review_heading_obj = soup.find_all("p", class_="_2xg6Ul")
    review = soup.find_all("div", class_="qwjRop")

    star_count_list = []
    review_heading_list = []
    review_list = []


    for words in review_heading_obj:
        review_heading_list.append(words.text)    

    for tag in review:
        review_list.append(tag.text)
    
    star_count_list = get_ratings(star_count_obj)

    return(star_count_list,review_heading_list,review_list)

def remove_nestings(a):
    return functools.reduce(iconcat, a, [])

def get_dataset_from_url(main_url):
    
    review_urls = getURLs(main_url)
    temp_review_urls = []

    #Restricting the scrapte to just 200 pages because Flipkart blocks the URL after multiple URL hits
    if (len(review_urls) < 150):
        temp_review_urls = review_urls
    else:
        temp_review_urls = review_urls[0:150]

    
    #Initialize all the lists
    data_set = pd.DataFrame()
    star_count_list_final = []
    review_heading_list_final = []
    review_list_final = []

    for temp in temp_review_urls:
        soup,review,review_heading_obj,star_count_obj = get_objects(temp)
        temp_star_count_list,temp_review_heading_list,temp_review_list = populate_details(star_count_obj,soup,review_heading_obj,review)

        star_count_list_final.append(temp_star_count_list)
        review_heading_list_final.append(temp_review_heading_list)
        review_list_final.append(temp_review_list)

    star_count_list_final = remove_nestings(star_count_list_final)
    review_heading_list_final = remove_nestings(review_heading_list_final)
    review_list_final = remove_nestings(review_list_final)

    data_set['Star_count'] = star_count_list_final
    data_set['Heading'] = review_heading_list_final
    data_set['Review'] = review_list_final

    data_set['Review'] = data_set['Review'].apply(lambda x: re.sub("READ MORE","",x))
    
    #data_set.to_csv('Outputs/Quiet_book.csv', index=False)
    return(data_set)

#main_url = 'https://www.flipkart.com/apple-ipad-7th-gen-32-gb-10-2-inch-wi-fi-only-gold/product-reviews/itmeb7a8cd2d3cf6?pid=TABFHF3A3GTFNHZH&lid=LSTTABFHF3A3GTFNHZH0VCIDD&marketplace=FLIPKART'
#new_data_set = get_dataset_from_url(main_url)

#print("Success!")
    

