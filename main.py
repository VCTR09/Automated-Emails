import yagmail
import os
import pandas
from news import NewsFeed
import datetime
import time


def send_email():
    contents, receiver_email, sender, subject = make_email()
    email = yagmail.SMTP(user=sender, password=os.getenv("GMAIL_PSWD"))
    email.send(to=receiver_email,
               subject=subject,
               contents=contents)
    print("Email Sent!")


def make_email():
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    news_feed = NewsFeed(interest=row['interest'],
                         from_date=yesterday,
                         to_date=today,
                         language='en')
    sender = os.getenv('GMAIL')
    receiver_email = row['email']
    subject = f"Your {row['interest']} news for today!"
    contents = [f"""
        Hi {row['name']},
        
        See what's on about {row['interest']} today.
        
        {news_feed.get()}
        Have a good day!
        """
                ]
    return contents, receiver_email, sender, subject


while True:
    if datetime.datetime.now().hour == 8 and datetime.datetime.now().minute == 45:
        df = pandas.read_csv('people.csv')

        for index, row in df.iterrows():
            send_email()

    time.sleep(60)