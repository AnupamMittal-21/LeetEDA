from datetime import date
from datetime import datetime
import pandas as pd

def Date_Conversion(s1):
    if 'hours' in s1:
        return date.today()
    else:
        date_str_de_DE = s1
        datetime_object = datetime.strptime(date_str_de_DE, '%b %d, %Y')
        return datetime_object.date()

def Remove_K(s1):
    if 'K' in s1:
        return s1.replace('K','')
    if '%' in s1:
        return s1.replace('%','')
    else:
        a = float(s1)
    return str(a/1000)

def difficulty_encoding(s):
    if s == 'Hard':
        return 3
    elif s == 'Medium':
        return 2
    else:
        return 1

def Create_tags(column):
    tags_list = []
    for tag in column:
        a = tag.split('https://leetcode.com/tag/')
        tags_list.append(a[1].split('/')[0])
    return tags_list

def Preprocess_dataframe(df):
    df['DateOfSubmission'] = df['DateOfSubmission'].apply(Date_Conversion)
    df['Likes'] = df['Likes'].apply(Remove_K)
    df['Dislikes'] = df['Dislikes'].apply(Remove_K)
    df['Acceptance'] = df['Acceptance'].apply(Remove_K)
    df['Diff_encoded'] = df['Difficulty'].apply(difficulty_encoding)

    df['DateOfSubmission'] = pd.to_datetime(df['DateOfSubmission'])
    df['Likes'] = df['Likes'].astype('float64')
    df['Dislikes'] = df['Dislikes'].astype('float64')
    df['Acceptance'] = df['Acceptance'].astype('float64')
    df['ID'] = df['ID'].astype('int64')
    df['Tags'] = df['Tag_Link'].apply(Create_tags)
    return df

def get_topics(df):
    topics = []
    for topic_list in df['Tags']:
        for topic in topic_list:
            if topic not in topics:
                topics.append(topic)
    return topics

def get_years(df):
    start_date = df.iloc[-1]['DateOfSubmission']
    end_date = df.iloc[0]['DateOfSubmission']
    print(type(start_date))
    years = ['All Years']
    for i in range(start_date.year, end_date.year + 1):
        years.append(i)
    return years

def get_month_name(s):
    return s.month_name()

def get_year(s):
    return s.year

def get_week(s):
    return int(s.strftime("%U"))

def accepted_questions(df,status):
    a_df = df[df['Status'] == status]
    easy = []
    medium = []
    hard = []
    dos_ = a_df.groupby('DateOfSubmission')
    dates = []
    for x, y in dos_:
        dates.append(x)
        dos = dos_.get_group(x)
        try:
            eas = dos.groupby('Difficulty').get_group('Easy')['Status'].count()
        except:
            eas = 0
        try:
            med = dos.groupby('Difficulty').get_group('Medium')['Status'].count()
        except:
            med = 0
        try:
            har = dos.groupby('Difficulty').get_group('Hard')['Status'].count()
        except:
            har = 0
        easy.append(eas)
        medium.append(med)
        hard.append(har)

    dict = {'Date': dates, 'Easy': easy, 'Medium': medium, 'Hard': hard}
    df_accepted = pd.DataFrame(dict)
    df_accepted['Total'] = df_accepted['Easy'] + df_accepted['Medium'] + df_accepted['Hard']
    df_accepted['Month'] = df_accepted['Date'].apply(get_month_name)
    df_accepted['Year'] = df_accepted['Date'].apply(get_year)
    df_accepted['Month'] = df_accepted['Month'].astype(str)
    df_accepted['Month_Year'] = df_accepted['Month'].str.cat(df_accepted['Year'].astype(str), sep='-')
    df_accepted['Week'] = df_accepted['Date'].apply(get_week)
    df_accepted['Week_Year'] = df_accepted['Week'].astype(str) + '-' + df_accepted['Year'].astype(str)
    return df_accepted


month_dict = {
    'January': 1,
    'February': 2,
    'March': 3,
    'April': 4,
    'May': 5,
    'June': 6,
    'July': 7,
    'August': 8,
    'September': 9,
    'October': 10,
    'November': 11,
    'December': 12,
}

def to_month_number(s):
    return month_dict[s]

def get_status_types(df):
    status_types = df['Status'].unique()
    return status_types

def get_df_summary(df_status_acc):
    easy = []
    medium = []
    hard = []
    total = []
    month = []
    year = []
    month_year = []
    for u, v in df_status_acc.groupby('Month_Year'):
        mon = v['Month'].unique()[0]
        mon_year = v['Month_Year'].unique()[0]
        eas = v['Easy'].sum()
        med = v['Medium'].sum()
        har = v['Hard'].sum()
        tot = v['Total'].sum()
        yea = v['Year'].unique()[0]
        easy.append(eas)
        medium.append(med)
        hard.append(har)
        total.append(tot)
        month.append(mon)
        year.append(yea)
        month_year.append(mon_year)

    dict = {'Month': month, 'Year': year, 'Month_Year': month_year, 'Easy': easy, 'Medium': medium, 'Hard': hard,
            'Total': total}
    df_imp = pd.DataFrame(dict)
    df_imp['Month_no'] = df_imp['Month'].apply(to_month_number)
    df_imp.sort_values(by=['Year', 'Month_no'], inplace=True)
    return df_imp


def get_df_week_summary(df_status_acc):
    easy = []
    medium = []
    hard = []
    total = []
    month = []
    week_year = []
    year = []
    month_year = []
    week = []
    for u, v in df_status_acc.groupby('Week_Year'):
        mon = v['Month'].unique()[0]
        wee_year = v['Week_Year'].unique()[0]
        mon_year = v['Month_Year'].unique()[0]
        eas = v['Easy'].sum()
        med = v['Medium'].sum()
        har = v['Hard'].sum()
        tot = v['Total'].sum()
        yea = v['Year'].unique()[0]
        wee = v['Week'].unique()[0]
        easy.append(eas)
        medium.append(med)
        hard.append(har)
        total.append(tot)
        month.append(mon)
        year.append(yea)
        month_year.append(mon_year)
        week_year.append(wee_year)
        week.append(wee)

    dict = {'Month': month, 'Year': year, 'Month_Year': month_year, 'Week_Year': week_year, 'Week': week, 'Easy': easy,
            'Medium': medium, 'Hard': hard, 'Total': total}
    df_imp = pd.DataFrame(dict)
    df_imp['Month_no'] = df_imp['Month'].apply(to_month_number)
    df_imp.sort_values(by=['Year', 'Week'], inplace=True)
    return df_imp