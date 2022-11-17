# to organise the code properly
from collections import Counter
from urlextract import URLExtract
from wordcloud import  WordCloud
import  pandas as pd
import emoji
#import matplotlib.pyplot as plt

def fetch_stats(selected_user,df):
    if selected_user!="Overall":
        df = df[df["User"]==selected_user]
    #fetching num messages
    num_messages = df.shape[0]

    # feching no. of words
    words = []
    for message in df["User_messages"]:
        words.extend(message.split())

    # feteching total number of midea
    num_media_message = df[df['User_messages']=="<Media omitted>\n"].shape[0]

    # fetching number of link shared
    extractor = URLExtract()
    links = []
    for message in df["User_messages"]:
        links.extend(extractor.find_urls(message))


    return num_messages, words , num_media_message , links


def fecth_most_busy_users(df):
    x = df.User.value_counts().head()
    df = round((df.User.value_counts()/df.shape[0])*100,2).reset_index().rename(columns= {'index':'Name','User':'Percent'})
    return  x,df

# Wordcloud
def create_wordcld(selected_user,df):
    if selected_user!="Overall":
        df = df[df["User"]==selected_user]

    wc = WordCloud(width=500,height=500,min_font_size=10,background_color="black")
    df_wc = wc.generate(df["User_messages"].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user,df):
    if selected_user!="Overall":
        df = df[df["User"]==selected_user]

    nndf = df[df['User'] != 'group_notification']
    nndf = nndf[nndf["User_messages"]!="<Media omitted>\n"]

    f = open("hinglish_stopwords.txt", 'r')
    stop_words = f.read()

    words = []
    for mess in nndf["User_messages"]:
        for word in mess.lower().split():
            if word not in stop_words:
                if (word != "(file") & (word != "attached)") & (word != ","):
                    words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return  most_common_df

def emoji_helper(selected_user,df):
    if selected_user!="Overall":
        df = df[df["User"]==selected_user]

    emojis = []
    for mm in df["User_messages"]:
        emojis.extend([c for c in mm if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return  emoji_df

def monthly_timeline(selected_user,df):
    if selected_user!="Overall":
        df = df[df["User"]==selected_user]

    timeline = df.groupby(["Year", "month_num", "Month"]).count()["User_messages"].reset_index()
    tim = []
    for i in range(timeline.shape[0]):
        tim.append(timeline['Month'][i] + "-" + str(timeline["Year"][i]))

    timeline['time'] = tim

    return timeline

def daily_timeline(selected_user,df):
    if selected_user!="Overall":
        df = df[df["User"]==selected_user]


    df["only_date"]=df["DATE"].dt.date

    daily_timeline = df.groupby("only_date").count()["User_messages"].reset_index()

    return daily_timeline

def activity_map_for_everyday(selected_user,df):
    if selected_user!="Overall":
        df = df[df["User"]==selected_user]

    return  df["Day name"].value_counts()

def activity_map_for_month(selected_user,df):
    if selected_user!="Overall":
        df = df[df["User"]==selected_user]

    return df["Month"].value_counts()

def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='Day name', columns='period', values='User_messages', aggfunc='count').fillna(0)

    return user_heatmap



