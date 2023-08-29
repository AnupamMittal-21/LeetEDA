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

def extract_insights(df):
    submission_counts_per_day = df.groupby("DateOfSubmission")["Diff_encoded"].sum()
    submission_counts_per_day_status = df[df['Status']=='Accepted'].groupby("DateOfSubmission")['Diff_encoded'].sum()
    submission_difficulty_easy = df[df['Difficulty']=='Easy'].groupby("DateOfSubmission")['Diff_encoded'].sum()
    return submission_counts_per_day,submission_counts_per_day_status,submission_difficulty_easy

def get_month_name(s):
    return s.month_name()

def get_year(s):
    return s.year

def accepted_questions(df):
    a_df = df[df['Status'] == 'Accepted']
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
    return df_accepted

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
