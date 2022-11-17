import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import proccessor,Helper


st.sidebar.title("Whatsapp Chat Analyzer")

# for uploading file
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    #to read file as bytes
    bytes_data = uploaded_file.getvalue()
    # till now the file is a stream we have to convert it into string
    data = bytes_data.decode("utf-8")
    #st.text(data)
    df = proccessor.preprocess(data)

    #st.dataframe(df)

    #fetch unique Users
    user_list = df["User"].unique().tolist()
    user_list.remove("group_notification")
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Show Analysis with accordance to",user_list)

    if st.sidebar.button("Show Analysis"):

        num_messages,words , num_media_message,links = Helper.fetch_stats(selected_user,df)
        st.title("Top Statistics")
        col1 , col2 , col3 ,col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(len(words))

        with col3:
            st.header("Media Shared")
            st.title(num_media_message)

        with col4:
            st.header("Links Shared")
            st.title(len(links))

        # Monthly timeline
        st.title("Monthly Timeline")
        ffg,aax = plt.subplots()
        timelin = Helper.monthly_timeline(selected_user,df)
        aax.plot(timelin["time"],timelin["User_messages"],color= "green")
        plt.xticks(rotation='vertical')
        st.pyplot(ffg)

        # daily Timeline
        st.title("Daily Timeline")
        daily_timeline = Helper.daily_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(daily_timeline["only_date"],daily_timeline["User_messages"])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # activity map of everyday
        st.title("Activity Map")
        col1,col2 = st.columns(2)
        with col1:
            st.header("Most Busy Day")
            busy_day = Helper.activity_map_for_everyday(selected_user,df)
            fig, ax = plt.subplots()
            ax.plot(busy_day.index,busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.header("Most Busy Month")
            busy_month = Helper.activity_map_for_month(selected_user,df)
            fig, ax = plt.subplots()
            ax.plot(busy_month.index, busy_month.values,color="orange")
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap = Helper.activity_heatmap(selected_user,df)
        fig , axxx= plt.subplots()
        axxx = sns.heatmap(user_heatmap)
        st.pyplot(fig)




        # finding the active or busy users in grp (Group Level)
        if selected_user=="Overall":
            st.title("Most Active Users")

            x , ndf= Helper.fecth_most_busy_users(df)
            fig, ax = plt.subplots()

            coll1 , coll2 = st.columns(2)

            with coll1:
                ax.bar(x.index, x.values,color = "red")
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)

            with coll2:
                st.dataframe(ndf)

        #Wordcloud
        st.title('Wordcloud')
        df_wc = Helper.create_wordcld(selected_user,df)
        figg , axs = plt.subplots()
        axs.imshow(df_wc)
        st.pyplot(figg)

        #Most common words
        st.title("Most Common Words")
        most_common_df = Helper.most_common_words(selected_user,df)
        fi ,a = plt.subplots()
        a.barh(most_common_df[0],most_common_df[1]) # for horizontal bar plot
        plt.xticks(rotation='vertical')
        st.pyplot(fi)

        # Emoji analysis
        st.title("Emojis Used")
        emoji_df = Helper.emoji_helper(selected_user,df)

        cl1,cl2 = st.columns(2)

        with cl2:
            st.dataframe(emoji_df)

        with cl1:
            fff, aa = plt.subplots()
            aa.pie(emoji_df[1].head(),labels = emoji_df[0].head(),autopct = "%0.2f")
            st.pyplot(fff)


