from eda import  preprocess
import plotly.express as px
import streamlit as st
import pickle
import pandas as pd
import numpy as np

leet_dict = pickle.load(open('leet_dict.pkl','rb'))
df = pd.DataFrame(leet_dict)


df = preprocess.Preprocess_dataframe(df)
st.title("...Jai Shree Ram...")


#  Accepted analysis based on years
df_accepted = preprocess.accepted_questions(df)

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
    df_tags = preprocess.accepted_questions(df_tags)

    fig = px.bar(df_tags, x=df_tags['Date'], y=df_tags['Total'],color=df_tags['Month'])
    st.plotly_chart(fig)



# UI components cheat sheet

# x = st.slider('x')  # 👈 this is a widget
# st.write(x, 'squared is', x * x)
#
# st.text_input("Your name", key="name")
#
# # You can access the value at any point with:
# st.session_state.name
# if st.checkbox('Show dataframe'):
#     chart_data = pd.DataFrame(
#        np.random.randn(20, 3),
#        columns=['a', 'b', 'c'])
#
#     chart_data
#
#
# df = pd.DataFrame({
#     'first column': [1, 2, 3, 4],
#     'second column': [10, 20, 30, 40]
#     })
#
# option = st.selectbox(
#     'Which number do you like best?',
#      df['first column'])
#
# 'You selected: ', option
#
# # Add a selectbox to the sidebar:
# add_selectbox = st.sidebar.selectbox(
#     'How would you like to be contacted?',
#     ('Email', 'Home phone', 'Mobile phone')
# )
#
# # Add a slider to the sidebar:
# add_slider = st.sidebar.slider(
#     'Select a range of values',
#     0.0, 100.0, (25.0, 75.0)
# )
#
#
#
# left_column, right_column = st.columns(2)
# # You can use a column just like st.sidebar:
# left_column.button('Press me!')
#
# # Or even better, call Streamlit functions inside a "with" block:
# with right_column:
#     chosen = st.radio(
#         'Sorting hat',
#         ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"))
#     st.write(f"You are in {chosen} house!")

