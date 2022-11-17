#def proccess(data):
import re
import pandas as pd


def preprocess(data):
    pattern = "\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s"
    messages = re.split(pattern, data)[1:]
    date_time = re.findall(pattern, data)


    df = pd.DataFrame({'DATE': date_time, 'MESSAGES': messages})
    df['DATE'] = pd.to_datetime(df.DATE,format='%m/%d/%y, %H:%M - ')

    users = []
    user_mesages = []

    for mess in df["MESSAGES"]:
        entry = re.split(':\s', mess)
        if entry[1:] == []:
            users.append("group_notification")
            user_mesages.append(mess)

        else:
            users.append(entry[0])
            user_mesages.append(entry[1])

    df['User'] = users
    df['User_messages'] = user_mesages

    df['Year'] = df["DATE"].dt.year
    df["month_num"] = df["DATE"].dt.month
    df['Month'] = df["DATE"].dt.month_name()
    df['Day'] = df["DATE"].dt.day
    df["Day name"] = df["DATE"].dt.day_name()
    df['Hour'] = df["DATE"].dt.hour
    df["minutes"] = df["DATE"].dt.minute

    f = df[(df["User_messages"].str.find("<Media omitted>")) == 0]
    x = list(f.index)

    for i in x:
        df.iloc[i, 3] = "<Media omitted>\n"

    period = []
    for hour in df[['Day name', 'Hour']]['Hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df