import emoji.unicode_codes
import pandas as pd
from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import emoji

extract = URLExtract()

#Fetches Normal stats
def fetchStats(selected_user,df):

    if(selected_user!= 'Overall'):
        df = df[df['User'] == selected_user]
    total_messages = df.shape[0]
    words = []
    for message in df['Message']:
        words.extend(message.split())
    mediaOmitted = df[df['Message'] == '<Media omitted>']
    links = []
    for message in df['Message']:
        links.extend(extract.find_urls(message))
    return total_messages,len(words),mediaOmitted.shape[0],len(links)

#Busy Users
def fetchBusy(df):
    df = df[df['User'] != 'Group Notification']
    count = df['User'].value_counts().head()
    newdf = pd.DataFrame((df['User'].value_counts()/df.shape[0])*100)
    return count,newdf

#User used Most word
def mostWords(df):
    df = df[df['User']!= 'Group Notification']
    users = df['User'].unique()
    total_words = []
    for user in users:
        newdf = df[df['User'] == user]
        words = []
        for message in newdf['Message']:
            words.extend(message.split(' '))
        total_words.append(len(words))
    worddf = pd.DataFrame({'Users':users,'No. of Words':total_words})
    worddf.sort_values(by='No. of Words', ascending=False, inplace=True)
    worddf.reset_index(drop=True, inplace=True)
    worddf.index += 1
    return worddf
    
#World CLoud
def createWordcloud(selected_user,df):
    if(selected_user!='Overall'):
        df = df[df['User']==selected_user]
    df = df[df['Message']!= '<Media omitted>']
    wc = WordCloud(width = 500, height = 500, min_font_size=10,background_color='white',max_words=75,colormap='plasma')
    df_wc = wc.generate(df['Message'].str.cat(sep = " "))
    return df_wc

#Frequency of words
def getCommonWords(selected_user,df):
    if(selected_user != 'Overall'):
        df = df[df['User'] == selected_user]

    df = df[(df['User'] != 'Group Notification') | (df['Message']!= '<media omitted>')]
    file = open(r'stop_hinglish.txt','r')
    stop_words = file.read().split('\n')

    words = []
    for message in df['Message']:
        for word in message.lower().split():
            # if(word not in stop_words):
            words.append(word)

    mostcommon = pd.DataFrame(Counter(words).most_common(20),columns = ['Word','Frequency'])
    return mostcommon
    
#Emojis analysis
def getEmojis(selected_user,df):
    
    if(selected_user != 'Overall'):
        df = df[df['User'] == selected_user]
    emojis = []
    for message in df['Message']:
        emojis.extend(c for c in message if c in emoji.EMOJI_DATA)
    emojidf = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emojidf

#Activity for every month
def getMonth(selected_user,df):
    if(selected_user != 'Overall'):
        df = df[df['User'] == selected_user]

    temp = df.groupby(['Year','Month','Month_name']).count()['Message'].reset_index()
    months = []
    for i in range(temp.shape[0]):
        months.append((temp['Month_name'][i]) + "-" + str(temp['Year'][i]))

    temp['Time'] = months
    return temp

#Activity of each day of the week
def getDayActivity(selected_user,df):
    if(selected_user !='Overall'):
        df = df[df['User'] == selected_user]
    return df['Day_name'].value_counts()

#Activity of each month
def getMonthActivity(selected_user,df):
    if(selected_user !='Overall'):
        df = df[df['User'] == selected_user]
    return df['Month_name'].value_counts()
