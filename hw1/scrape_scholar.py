#!/usr/bin/env python
# coding: utf-8

# <h1 style="text-align:center;"> Fundamentos de Data Science </h1>
# <h4 style="text-align:center;">  Guilherme Araújo  e  Gabriel Novais </h4>
# <p  align="justify"> <b> Description </b> : Step 1 - Scraping .</p>   

# ### Importing Packages

# In[1]:


import pandas as pd
import numpy as np
import re
import time
import selenium
import splinter

from splinter import Browser
from bs4 import BeautifulSoup


# ### Function

# In[5]:


def scrape(x):
    browser = Browser(driver_name='chrome', headless=True)
    browser.visit('https://scholar.google.com.br/')
    browser.fill('q', x)
    browser.find_by_name('btnG').click()
    browser.click_link_by_partial_text(x)
    browser.click_link_by_partial_text(x)
    button = ['Artigos 1–100']
    while float(button[0][10:])%100==0:
        browser.find_by_id('gsc_bpf_more').click()
        time.sleep(3)
        soup = BeautifulSoup(browser.html,"html.parser")
        button = soup.findAll("span", {"id":"gsc_a_nn"})
        button = [re.findall(r'">(.+?)</span>', str(o))[0] for o in button]
        time.sleep(3)
    soup = BeautifulSoup(browser.html,"html.parser")
    tags1 = [a for a in soup.findAll("a", {"class":"gsc_a_at"})]
    tags2 = [div for div in soup.findAll("div", {"class":"gs_gray"})][::2]
    article = [re.findall(r'">(.+?)</a>', str(o))[0] for o in tags1]
    author = [re.findall(r'">(.+?)</div>', str(o))[0] for o in tags2]
    author = [a.split(", ") for a in author]
    t = ['title']*len(author)
    a = ['authors']*len(author)
    papers = []
    for t1, v1,a1,va1 in zip(t,article,a,author):
        mydict = {}
        mydict[t1] = v1
        mydict[a1] = va1
        aux = mydict
        papers.append(aux)

    if len(article)==0 or len(author)==0:
        print("ERROR: Author doesn't have any Paper or Paper doesn't have any Author")
    else:    
        return papers
    browser.quit()


# In[7]:


#Converting
#get_ipython().system('jupyter nbconvert --to script scholar.ipynb')




