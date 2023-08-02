# from flask import Flask
# app = Flask(__name__)

# @app.route('/')
# def hello_world():  # put application's code here
#     return 'Hello World!'
#
#
# if __name__ == '__main__':
#     app.run()

import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analysis")
st.sidebar.text("""Only Chats exported without media 
can be uploaded here""")

uploaded_file = st.sidebar.file_uploader("Choose a file", type=None, accept_multiple_files=False)
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)
    # st.dataframe(df)


    user_list = sorted(df['username'].unique().tolist())
    user_list.insert(0,'Overall')
    selected_user = st.sidebar.selectbox("Show analysis wrt",user_list)

    # Monthly Timeline
    st.title("Monthly Timeline")
    timeline = helper.monthly_timeline(selected_user,df)
    fig,ax = plt.subplots()
    ax.plot(timeline['time'],timeline['message'],color='green')
    plt.xticks(rotation='vertical')
    st.pyplot(fig)

    # st.text("Analysis on Gupuuu's Conversation")

    # Daily Timeline
    st.title("Daily Timeline")
    daily_timeline = helper.daily_timeline(selected_user,df)
    fig,ax = plt.subplots()
    ax.plot(daily_timeline['only_date'],daily_timeline['message'],color='green')
    plt.xticks(rotation='vertical')
    st.pyplot(fig)

    # Activity Map
    st.title("Activity Map!")
    col1, col2 = st.columns(2)
    with col1:
        st.header("Most Busy Day")
        busy_day = helper.week_activity_map(selected_user,df)
        fig,ax = plt.subplots()
        ax.bar(busy_day.index,busy_day.values)
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
    with col2:
        st.header("Most Busy Month")
        busy_month = helper.month_activity_map(selected_user,df)
        fig,ax = plt.subplots()
        ax.bar(busy_month.index,busy_month.values, color='orange')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

    # Heatmap
    st.title("Weekly Activity Map")
    heatmap = helper.activity_heatmap(selected_user, df)
    plt.figure(figsize=(20, 6))
    fig, ax = plt.subplots()
    ax = sns.heatmap(heatmap)
    st.pyplot(fig)

    st.markdown("""---""")

    if st.sidebar.button("Show Analysis"):
        num_messages, words, num_media_messages,links = helper.fetch_stats(selected_user,df)
        col1,col2,col3,col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links Shared")
            st.title(links)
        st.markdown("""---""")
        # Finding Busiest users in Group
        if selected_user == 'Overall':
            st.title("Most Active Users")
            active_users,new_df = helper.fetch_most_busy_users(df)
            col1,col2 = st.columns(2)
            with col1:
                fig, ax = plt.subplots()
                ax.bar(active_users.index, active_users.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # Word Cloud
        st.title("Common Used Words!")
        df_wc = helper.create_wordcloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # Most Common Words
        most_common_df = helper.most_common_words(selected_user,df)
        # st.dataframe(most_common_df)
        fig,ax = plt.subplots()
        ax.barh(most_common_df['words'],most_common_df['frequency'])
        plt.xticks(rotation='vertical')
        st.title('Top 20 Words!')
        st.pyplot(fig)

        # Most Common Emojis
        st.title("Emoji Analysis")
        col1, col2 = st.columns(2)
        most_common_emoji = helper.most_common_emoji(selected_user,df)
        with col1:
            st.dataframe(most_common_emoji)
        with col2:
            fig,ax=plt.subplots()
            ax.pie(most_common_emoji[1].head(8),labels=most_common_emoji[0].head(8),autopct="%0.2f")
            st.pyplot(fig)