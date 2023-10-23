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
    df['Month'] = df['DateOfSubmission'].apply(get_month_name)
    df['Year'] = df['DateOfSubmission'].apply(get_year)
    df['QName'] = df['Name'].apply(name)
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

def get_per_date(df):
    tag_list = get_topics(df)
    cols = ['Status', 'DateOfSubmission', 'Difficulty', 'Tags', 'Month', 'Year']
    plot_df = df[cols]
    date_df = plot_df.groupby('DateOfSubmission')
    ans = []
    x_ = []
    for i, j in date_df:
        print(j)
        x_.append(i)
        dict = {}
        for i in tag_list:
            dict[i] = 0
        for x in j['Tags']:
            for k in x:
                dict[k] = dict[k] + 1
        ans.append(dict)

    for_each = []
    for topic in tag_list:
        tp = []
        for day, y in enumerate(x_):
            tp.append(ans[day][topic])
        for_each.append(tp)
    return x_,for_each


def get_name(s):
    t2 = s.split('https://leetcode.com/problems/')[1]
    t = t2.split('/')[0]
    return t

def name(s):
    s = s.lower()
    s = s.replace(' ','-')
    return s
def get_dp_df(df):
    dp_df = pd.read_csv('dp_leet.csv')
    dp_df['QName'] = dp_df['Question'].apply(get_name)
    a = dp_df['Category'].value_counts()

    not_done = dp_df[~dp_df['QName'].isin(df['QName'])]
    done = dp_df[dp_df['QName'].isin(df['QName'])]
    b = done['Category'].value_counts()

    dfn = pd.concat([a, b], axis=1)
    dfn = dfn.reset_index()
    # Display the resulting DataFrame
    dfn.columns = ['Category', 'All', 'Done']
    dfn['Done'] = dfn['Done'].fillna(0).astype(int)
    dfn['Percent'] = (dfn['Done'] / dfn['All']) * 100
    dfn_least_done = dfn.sort_values(by='Percent')
    least = dfn_least_done.head(5)['Category']
    # Means ye to bhut hi kam kar rakhe h
    dfn_most_done = dfn.sort_values(by='Percent', ascending=False)
    Threshold = 30.0
    dfn_most_done = dfn_most_done[dfn_most_done['Percent'] < Threshold]
    most = dfn_most_done.head()['Category']
    # Most means you have done it but not up to the mark (< than threshold value)
    least_to_do = not_done[not_done['Category'].isin(list(least))]
    most_to_do = not_done[not_done['Category'].isin(list(most))]

    least_df = pd.DataFrame()
    least_df = least_to_do[least_to_do['Category'] == 'a']
    for i in list(least):
        #     i = 'Math'
        cat = not_done[not_done['Category'] == i]
        #     Apply prob of getting accepted
        #  Question is how to pick the question from large data set, one way is to give control to user, ask him to chooose random, sort by easy. medium hard, by prob of getting accepted
        # like this , this is a lot to do work
        # let me take case of random until i came up with accepting probabiltiy.
        new_ = cat.sample(3)
        least_df = pd.concat([least_df, new_], axis=0)
        print(cat.shape)

    threshold_percent = 30
    most_df = pd.DataFrame()
    most_df = most_to_do[most_to_do['Category'] == 'a']
    for i in list(most):
        #     i = 'Math'
        cat = not_done[not_done['Category'] == i]
        #     Apply prob of getting accepted
        #  Question is how to pick the question from large data set, one way is to give control to user, ask him to chooose random, sort by easy. medium hard, by prob of getting accepted
        # like this , this is a lot to do work
        # let me take case of random until i came up with accepting probabiltiy.
        new_ = cat.sample(3)
        most_df = pd.concat([most_df, new_], axis=0)

    return least_df, most_df


