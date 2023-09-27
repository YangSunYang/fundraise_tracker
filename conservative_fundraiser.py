#!/usr/bin/env python
# coding: utf-8


import pandas as pd
from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen
import time


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
    # Event title normally uses H3 tag
    title_h3 = event.find('h3')
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
df_history = pd.read_csv('https://yang-data-project.s3.amazonaws.com/conservative-events/conservative_events.csv')

# df_history = df_history.iloc[:,1:]


# In[56]:


df = pd.concat([df_history, df])


# In[57]:


df = df.drop_duplicates()


# In[58]:


df.to_csv('conservative_events.csv', index=False)


# In[ ]:


df_history = pd.read_csv('history.csv')

print("the csv file is exported successfully!")

