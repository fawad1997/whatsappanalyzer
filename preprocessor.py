import pandas as pd
import re


def preprocess(data):
    date_type = 12
    pattern = "\d{1,2}\/\d{1,2}\/\d{2},\s\d{1,2}:\d{2}\s\w{2}\s\-\s"
    messages = re.split(pattern, data)[1:]
    if messages == []:
        date_type = 24
        pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
        messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    df = pd.DataFrame({'user_message': messages, 'date': dates})
    df = df[2:]
    df['date'] = df['date'].str.rstrip('- ')
    if date_type == 12:
        df['date'] = pd.to_datetime(df['date'], format='%m/%d/%y, %I:%M %p')
    else:
        df['date'] = pd.to_datetime(df['date'], format='%m/%d/%y, %H:%M')
    # df = df[~df['user_message'].str.contains('<Media omitted>', case=False)]
    df['user_message'] = df['user_message'].str.rstrip('\n')
    df[['username', 'message']] = df['user_message'].str.split(': ', n=1, expand=True)
    df.drop('user_message', axis=1, inplace=True)
    mask = ~df['username'].isin(['Disappearing messages now support keeping messages in the chat. Tap to learn more.',
                                 "The message timer was updated. New messages will disappear from this chat 90 days after they're sent, except when kept. Tap to change."]) & ~ \
           df['username'].str.contains('call', case=False)& ~ \
           df['username'].str.contains('number', case=False)& ~ \
           df['username'].str.contains('added', case=False)
    df = df[mask]
    df = df[df['message'].str.contains('[a-zA-Z]')]
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['month_num'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['only_date'] = df['date'].dt.date
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour))
        else:
            period.append(str(hour) + "-" + str(hour + 1))
    df['period'] = period
    df.drop('date',axis=1,inplace=True)
    return df
