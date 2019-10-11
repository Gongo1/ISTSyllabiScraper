"""
Created on Mon Aug 19 22:56:38 2019
@Title:Syllabi Scrapper
@python 2.7 version 
@author: Austin
@client: Cramless
@purpose: web-scrape teaching.ist for syllabi of different courses
"""


#Libraries
from bs4 import BeautifulSoup as bsp
import requests
import pandas as pd
import names
import re
import urllib2
import os
import time
import unicodedata
start = time.time()



base_url = "https://teaching.ist.psu.edu/ist-courses"
output_directory = "data/"

#os.chdir("/Users/Austin/Desktop/cramless")

#----------------------------------------------------
''' Collect all course links from HTML using base_url '''
# connect to server, randomize user-agent tag to enable prolonged iterations
req = requests.get(base_url, headers=({'User-Agent' : names.get_full_name()}))
# get the html content from the webpage
r = req.content
# 'soup' it
soup = bsp(r, 'lxml')

#
course_silly = []
for tag in soup.findAll('a', href=True):
    course_silly.append(tag['href'])
    #print tag['href']
    

#Getting new links for each major 
class_url = [s for s in course_silly if 'https://teaching.ist.psu.edu/courses/' in s]

#takes every single link 
all_links = []
for link in class_url:
    page = urllib2.urlopen(link)
    soup = bsp(page, 'html.parser')
    for tag in soup.findAll('a', href=True):
        all_links.append(tag['href']) 
    #sylly_links.append(tag['href'])
    
    major = link.split("/")[-2:][0].upper()
    print "Getting data from {}".format(major)
    
#Takes only sylly links
get_silly= [s for s in all_links  if 'wp-content/uploads/sites' in s]
get_silly = set(get_silly)
#Append get_silly to base url

#Some of the links already contain the entire url so we want to extract those 
#Make sure to add theses to the list after the other urls are finalized
complete_links = [s for s in get_silly  if 'https://teaching.ist.psu.edu/wp-content/uploads/sites/' in s]

#Delete Complete links from get_silly
unfinished_links= [x for x in get_silly if x not in complete_links]

#IST210_Section002_Syllabus-FA18_withTopics.docx
#IST-402.3-FA17-Xu.docx

base_url = "https://teaching.ist.psu.edu"
sylly_list= []
for x in unfinished_links:
    l = base_url + x
    sylly_list.append(l)

#This contains all the links to scrape the syllabus with 
finalized_links = sylly_list + complete_links

#File naming convention 
clean_list = []
for i in finalized_links:
    clean_list.append(unicodedata.normalize('NFKD', i).encode('ascii','ignore'))


#Download pdfs to local machine 
for i in clean_list:
    r = requests.get(i)
    #print(i)
    #with open("document.pdf", 'wb') as f:
    with open(i[65:], 'wb') as f:
        f.write(r.content)
    

end = time.time()
print(end - start,"seconds")
    
