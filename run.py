from eda import preprocess
import plotly.express as px
import streamlit as st
import pickle
import pandas as pd
import plotly.graph_objects as go
import numpy as np
st.set_page_config (layout="wide")
leet_dict = pickle.load(open('leet_dict.pkl','rb'))
df = pd.DataFrame(leet_dict)

st.write(df.head(8))
df = preprocess.Preprocess_dataframe(df)


st.title("LeetCode Analysis")

#  Accepted analysis based on years
df_accepted = preprocess.accepted_questions(df,'Accepted')

tup_dt = preprocess.get_years(df)
choice1 = st.selectbox(
    'choose year to see analysis of particular year',
    tup_dt
)

if choice1=='All Years':
    fig = px.bar(df_accepted, x=df_accepted.Date, y=df_accepted.Total, hover_data=['Easy', 'Medium', 'Hard'],color=df_accepted.Month)
    st.plotly_chart(fig)
else:
    new_df = df_accepted[df_accepted['Year']==choice1]
    fig = px.bar(new_df, x=new_df.Date, y=new_df.Total, hover_data=['Easy', 'Medium', 'Hard'],color=new_df.Month)
    st.plotly_chart(fig)

years = preprocess.get_years(df)



#  Difficulty wise
diff_list = ['All Difficulty','Easy','Medium','Hard']
choice1 = st.selectbox(
    'choose difficulty to see analysis',
    diff_list
)
if choice1=='All Difficulty':
    fig = px.bar(df_accepted, x=df_accepted.Date, y=df_accepted.Total, hover_data=['Easy', 'Medium', 'Hard'],color=df_accepted.Month)
    st.plotly_chart(fig)
else:
    # new_df = df_accepted[df_accepted['Year']==choice1]
    fig = px.bar(df_accepted, x=df_accepted['Date'], y=df_accepted[choice1],color=df_accepted['Month'])
    st.plotly_chart(fig)

# Tags fuctionality

tag_list = preprocess.get_topics(df)

selected_tags = st.multiselect(
    "Select three known variables:",
    tag_list,
    max_selections=5,
)
req_tags = selected_tags


def fun(tag_list):
    for tag in tag_list:
        if tag in req_tags:
            return True
    return False

if len(selected_tags)==0:
    st.write("Choose Tags")
else:
    df_tags = df[df["Tags"].apply(fun)]
    df_tags = preprocess.accepted_questions(df_tags,'Accepted')

    fig = px.bar(df_tags, x=df_tags['Date'], y=df_tags['Total'],color=df_tags['Month'])
    st.plotly_chart(fig)



# Improvement Rate
tup_dt = preprocess.get_years(df)
choice2 = st.selectbox(
    'choose year',
    tup_dt
)

status_types = preprocess.get_status_types(df)

fig = go.Figure()

if choice2=='All Years':
    for status in status_types:
        df_status_acc = preprocess.accepted_questions(df, status)
        df_imp_acc = preprocess.get_df_summary(df_status_acc)
        fig.add_trace(go.Scatter(x=df_imp_acc.Month_Year, y=df_imp_acc.Total, mode='lines', name=status))
    fig.update_layout(title='Improvement Rate',
                      xaxis_title='Timeline', yaxis_title='Status Count')
    st.plotly_chart(fig)
else:
    new_df_2 = df[df['Year']==choice2]
    for status in status_types:
        df_status_acc = preprocess.accepted_questions(new_df_2, status)
        df_imp_acc = preprocess.get_df_summary(df_status_acc)
        fig.add_trace(go.Scatter(x=df_imp_acc.Month_Year, y=df_imp_acc.Total, mode='lines', name=status))
    fig.update_layout(title='Improvement Rate',
                      xaxis_title='Timeline', yaxis_title='Status Count')
    st.plotly_chart(fig)





### Improvement rate per week

tup_dt = preprocess.get_years(df)
choice2 = st.selectbox(
    'choose a year',
    tup_dt
)

status_types = preprocess.get_status_types(df)

fig = go.Figure()

if choice2=='All Years':
    for status in status_types:
        df_status_acc = preprocess.accepted_questions(df, status)
        df_imp_acc = preprocess.get_df_week_summary(df_status_acc)
        fig.add_trace(go.Scatter(x=df_imp_acc.Week_Year, y=df_imp_acc.Total, mode='lines', name=status))
    fig.update_layout(title='Improvement Rate',
                      xaxis_title='Timeline', yaxis_title='Status Count')
    st.plotly_chart(fig)
else:
    new_df_2 = df[df['Year']==choice2]
    for status in status_types:
        df_status_acc = preprocess.accepted_questions(new_df_2, status)
        df_imp_acc = preprocess.get_df_week_summary(df_status_acc)
        fig.add_trace(go.Scatter(x=df_imp_acc.Week_Year, y=df_imp_acc.Total, mode='lines', name=status))
    fig.update_layout(title='Improvement Rate',
                      xaxis_title='Timeline', yaxis_title='Status Count')
    st.plotly_chart(fig)

# Plot of monthwise status of questions.

name = "IDK"
tup_dt = preprocess.get_years(df)
choice3 = st.selectbox(
    'choose a year',
    (tup_dt), key=f"{name}",
)
if choice3=='All Years':
    fig = px.bar(df, x='Month', y='Diff_encoded', color='Status', title='Month-wise count of questions status.')
    st.plotly_chart(fig)
else :
    df_2023 = df[df['Year']==choice3]
    fig = px.bar(df_2023, x='Month', y='Diff_encoded', color='Status', title='Month-wise count of questions status.')
    st.plotly_chart(fig)



# HeatMap and other plot for each category representation.
x_,for_each = preprocess.get_per_date(df)
data = for_each

# Create the heatmap trace
heatmap_trace = go.Heatmap(z=data,x = x_, y = tag_list, colorscale='Viridis')

# Create a figure with the trace and layout
fig = go.Figure(data=[heatmap_trace])
st.plotly_chart(fig)


fig = go.Figure()
for i,j in enumerate(tag_list):
    a = [i] * len(x_)
    fig.add_trace(go.Scatter(
        x=x_,
        y=a,
        mode='markers',
        marker = {'size': [size * 2 for size in for_each[i]]},
        name = tag_list[i],
    ))
st.plotly_chart(fig)


least_df,most_df = preprocess.get_dp_df(df)

st.write("Model to show somw weak topic that you should focus on...")
st.write("These are topics in which you have less practice")
st.write(least_df)
st.write("These are topics in which you have good practice but need to do more")
st.write(most_df)