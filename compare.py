import pandas as pd

import smtplib
import ssl
from email.message import EmailMessage

# Import two datasets
df_history = pd.read_csv('https://yang-data-project.s3.amazonaws.com/conservative-events/data/conservative_events.csv')
df_current = pd.read_csv('data/conservative_events.csv')

# Compare the datasets
if df_current.equals(df_history):
    message = 'There is no event update today.'
else:
    message = 'There are event updates today.'

# Sending message via email
email_sender = 'yang.sun.globeandmail@gmail.com'
email_password = 'dcgmvclcqwhffblk'
email_receiver = ['yang.sun.globeandmail@gmail.com', 'ysun@globeandmail.com']

subject = 'Conservative party events update'
body = message

em = EmailMessage()
em['From'] = email_sender
em['To'] = email_receiver
em['Subject'] = subject
em.set_content(body)

context = ssl.create_default_context()

with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
    smtp.login(email_sender, email_password)
    smtp.sendmail(email_sender, email_receiver, em.as_string())
