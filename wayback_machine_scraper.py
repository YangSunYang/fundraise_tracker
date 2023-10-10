#!/usr/bin/env python
# coding: utf-8

# In[220]:


import pandas as pd
from bs4 import BeautifulSoup
import requests
import json
from urllib.request import urlopen
import time


# In[221]:


# Use the wayback machine API to get all the historic snapshots
api_url = 'http://web.archive.org/cdx/search/cdx?url=https://www.conservative.ca/events/&output=json'
response = urlopen(api_url)
data_json = json.loads(response.read())


# In[222]:


# Only select the timestamps
snapshots = [i[1] for i in data_json[1:]]
# Select all 2023 snapshots
snapshots_2023 = [i for i in snapshots if i.startswith('2023')]
# Generate a list of url for scraping
urls = ['https://web.archive.org/web/' + str(i) + '/https://www.conservative.ca/events/' for i in snapshots_2023]


# In[284]:


page_link = []
event_name = []
event_content = []


# In[286]:


for url in urls:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    events = soup.find_all('div', class_='cell')
    for event in events:
        page_link.append(url)
        # Try to find the title in H3
        title_h3 = event.find('h3')
        # If the h3 didn't contain the title, try h2
        if not title_h3:
            title_h2 = event.find('h2')
            # If not the h2, try h1
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
        # append the event title
        event_name.append(title_text)
        
        text_list = event.find_all('p')
        content_string = ''
        for i in text_list:
            content_string += i.text.strip() + '; '
        # Append the event details
        event_content.append(content_string)

    print(url)
    time.sleep(2)
            


# In[287]:


df = pd.DataFrame({'link':page_link,'event_title':event_name, 'event_details':event_content})


# In[292]:


df = df[df['event_details'] != '; ']


# In[293]:


df.drop_duplicates()


# In[300]:


df['event_details'] = df['event_details'].replace(r'\n','; ', regex=True)


# In[302]:


df.to_csv('history.csv')


# In[303]:


df.shape


# In[ ]:





# In[261]:


page = requests.get('https://web.archive.org/web/20230731220540/https://www.conservative.ca/events/')
soup = BeautifulSoup(page.content, "html.parser")
events = soup.find_all('div', class_='cell')


# In[269]:


text_list = events[3].find_all('p')
text_list


# In[282]:


content=''
for i in text_list:
    print(i.text.strip())
    content += i.text.strip() + '; '


# In[283]:


content


# In[ ]:




