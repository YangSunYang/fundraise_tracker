#!/usr/bin/env python
# coding: utf-8


import pandas as pd
from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen
import time
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


# In[48]:


url = 'https://www.conservative.ca/events/'
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")


# In[49]:


events = soup.find_all('div', class_='cell')
events = events[:-1]


# In[50]:


event_name = []
event_content = []

for event in events:
    title_h3 = event.find('h3')
    if not title_h3:
        title_h2 = event.find('h2')
        if not title_h2:
            title_h1 = event.find('h1')
            if title_h1:
                title_text = title_h1.text.strip()
            else:
                title_text = 'Title not found'
                
        else:
            title_text = title_h2.text.strip()
    else:
        title_text = title_h3.text.strip()
    
    event_name.append(title_text)

    # Locate p tags which store event details, such as time and location   
    text_list = event.find_all('p')
    content_string = ''
    for i in text_list:
        content_string += i.text.strip() + '; '
        # Append the event details
    event_content.append(content_string)


# In[51]:


df = pd.DataFrame({'event_title':event_name, 'event_details': event_content})


# In[52]:


df['Date'] = df['event_details'].str.extract(r'Date:(.*?);')


# In[53]:


df['Location'] = df['event_details'].str.extract(r'Location:(.*?);')


# In[55]:
df_history = pd.read_csv('https://yang-data-project.s3.amazonaws.com/conservative-events/data/conservative_events.csv')



# In[56]:


df = pd.concat([df_history, df])


# In[57]:


df = df.drop_duplicates()


# In[58]:


df.to_csv('data/conservative_events.csv', index=False)



print("the csv file is exported successfully!")

