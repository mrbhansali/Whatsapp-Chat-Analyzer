import re
import pandas as pd
import datetime

def getDateFormate(string):
    for i in string:
        date = i.split(',')[0]
        d = int(re.findall(r'(\d{1,2})\/\d{1,2}',date)[0])
        if(d>12):
            return 1
    return 0

def getTimeDate(string,formt):
    string = string.split(',')
    date = string[0]
    time = string[1]
    time = time.split('-')[0].strip()
    if(formt):
        date = datetime.datetime.strptime(date,"%d/%m/%y").strftime("%m/%d/%y")
    if(len(time)>5):
        time = datetime.datetime.strptime(time,"%I:%M %p").strftime('%H:%M')
    return date+" "+time

def preprocess(file):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}(?:\s[aApP][mM])?\s-\s'
    messages = re.split(pattern,file)[1:]
    dates = re.findall(pattern, file)
    df = pd.DataFrame({'user_messages': messages,'message_dates':dates })
    formt = getDateFormate(df['message_dates'])
    df['message_dates'] = df['message_dates'].apply(
        lambda text: getTimeDate(text,formt)
    )
    df.rename(columns={'message_dates':'dates'})

    #Extracting user and message
    user = []
    messages = []
    for message in df['user_messages']:
        entry = re.split(r'([\w\W]+?):\s',message)
        if entry[1:]:
            user.append(entry[1])
            messages.append(entry[2])
        else:
            messages.append(entry[0])
            user.append('Group Notification')
    df['user'] = user
    df['message'] = messages
    df['message'] = df['message'].apply(lambda text: text.split('\n')[0])
    df.drop(['user_messages'],axis =1,inplace=True)
    df.rename(columns= {'message':'Message','message_dates':'Date','user':'User'},inplace=True)

    #Extracting from date
    df['Only_date'] = pd.to_datetime(df['Date']).dt.date
    df['Year'] = pd.to_datetime(df['Date']).dt.year
    df['Month'] = pd.to_datetime(df['Date']).dt.month
    df['Month_name'] = pd.to_datetime(df['Date']).dt.month_name()
    df['Day'] = pd.to_datetime(df['Date']).dt.day
    df['Day_name'] = pd.to_datetime(df['Date']).dt.day_name()
    df['Hour'] = pd.to_datetime(df['Date']).dt.hour
    df['Minute'] = pd.to_datetime(df['Date']).dt.minute
    df['Month_name'] = df['Month_name'].astype(str)



    return df
