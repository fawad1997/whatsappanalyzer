from urlextract import URLExtract
from wordcloud import WordCloud
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from collections import Counter
import pandas as pd
import emoji

def fetch_stats(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['username'] == selected_user]
    # 1. Number of Messages
    num_messages = df.shape[0]
    # 2. Number of Words 4. Links Shared
    words = []
    links = []
    extractor = URLExtract()
    for message in df['message']:
        words.extend(message.split())
        links.extend(extractor.find_urls(message))
    # 3. Number of Media
    num_media_messages = df[df['message'] == '<Media omitted>'].shape[0]
    num_link_shared = df
    return num_messages,len(words),num_media_messages,len(links)

def fetch_most_busy_users(df):
    active_users = df['username'].value_counts().head()
    df = round(df['username'].value_counts()/df.shape[0]*100,2).reset_index().rename(columns={'count':'percentage share','username':'Name'})
    return active_users,df

def create_wordcloud(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['username'] == selected_user]
    df = df[~df['message'].str.contains('<Media omitted>', case=False)]
    df = df[~df['message'].apply(contains_url)]
    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    df_wc = wc.generate(df['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['username'] == selected_user]
    df = df[df['message'] != '<Media omitted>']
    stop_words = set(stopwords.words('english'))
    df['message'] = df['message'].apply(
        lambda x: ' '.join([word for word in x.split() if word.lower() not in stop_words]))
    words = []
    for message in df['message']:
        words.extend(message.split())
    most_common_df = pd.DataFrame(Counter(words).most_common(20)).rename(columns={0: 'words', 1: 'frequency'})
    return most_common_df

def most_common_emoji(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['username'] == selected_user]
    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
    most_common_emoji = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return most_common_emoji

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['username'] == selected_user]
    timeline = df.groupby(['year','month_num','month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+"-"+str(timeline['year'][i]))
    timeline['time']= time
    return timeline

def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['username'] == selected_user]
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline

def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['username'] == selected_user]
    return df['day_name'].value_counts()

def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['username'] == selected_user]
    return df['month'].value_counts()

def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['username'] == selected_user]
    period_order = sorted(df['period'].unique())
    activity_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)[period_order]
    return activity_heatmap

def contains_url(text):
    extractor = URLExtract()
    urls = extractor.find_urls(text)
    return len(urls) > 0