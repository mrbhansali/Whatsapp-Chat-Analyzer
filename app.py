import streamlit as st
import preprocess
import stats
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')


st.sidebar.title("Whatsapp chat analyze")
upload_file = st.sidebar.file_uploader('Choose a file')


if upload_file is not None:
    bytes_data = upload_file.getvalue()

    #byte code to text format
    data = bytes_data.decode("utf-8")

    #sending file to preporcess
    df = preprocess.preprocess(data)

    #Selectbox
    users = df['User'].unique().tolist()
    # users.remove('Group Notification')
    users.sort()
    users.insert(0,'Overall')
    selected_user = st.sidebar.selectbox(
        "Show analysis with respect to", users
    )
    st.title(f"Whatsapp Chat analysis with respect to: {selected_user}")
    #Analysis with respect to the selection
    if st.sidebar.button("Show analysis") :
        total_messages,words,mediaOmitted,links = stats.fetchStats(selected_user,df)
        col1, col2 ,col3, col4 = st.columns(4)

        with col1:
            st.header("Total Meassages")
            st.title(total_messages)
        with col2:
            st.header("Total words")
            st.title(words)
        with col3:
            st.header("Total media sent")
            st.title(mediaOmitted)
        with col4:
            st.header("Total links")
            st.title(links)

        #Most busy users
        if(selected_user == 'Overall'):
            st.title('Most Busy Users')
            busycount,newdf = stats.fetchBusy(df)
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)
            with col1:
                ax.bar(busycount.index,busycount.values,color = 'red')
                plt.xticks(rotation = 45)
                st.pyplot(fig)
            with col2:
                st.dataframe(newdf.rename(columns={'count':'percentage'}))


        #User which used most words
        if(selected_user == 'Overall'):
            st.title('User used most words')
            col1, col2 = st.columns(2)
            worddf = stats.mostWords(df)
            with col2:
                fig,ax = plt.subplots()
                ax.bar(worddf.loc[:8,'Users'],worddf.loc[:8,'No. of Words'],color = 'brown')
                plt.xticks(rotation = 'vertical')
                plt.xlabel('User Name')
                st.pyplot(fig)
            with col1:
                worddf['Percentage'] = worddf['No. of Words']/sum(worddf['No. of Words']) *100
                st.dataframe(worddf)
        
        #WORD CLOUD
        st.title("Word Cloud")
        df_img = stats.createWordcloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_img)
        st.pyplot(fig)

        #Most common words in the chat

        most_common_df = stats.getCommonWords(selected_user,df)
        fig,ax = plt.subplots()
        ax.barh(most_common_df['Word'].tolist(),most_common_df['Frequency'].tolist(),color = 'orange')
        ax.invert_yaxis()
        st.title("Most Common Words")
        st.pyplot(fig)


        #Emoji analysis
        emojidf = stats.getEmojis(selected_user,df)
        
        st.title("Analysis of emojis used")
        emojidf['Percentage'] = emojidf[1]/emojidf[1].sum() * 100
        emojidf.rename(columns={0:'Emoji',1:'Count'},inplace=True)
        emojidf = emojidf.reindex([i for i in range(1,len(emojidf)+1)])
        st.dataframe(emojidf)

        #Analysis wrt month
        st.title("Messages per Month")
        monthdf = stats.getMonth(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(monthdf['Time'],monthdf['Message'],color = 'blue')
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)

        #Activity Maps
        col1, col2 = st.columns(2)
        with col1:
            daydf = stats.getDayActivity(selected_user,df)
            st.title("Days activity")
            custom_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            daydf = daydf.reindex(custom_order)
            fig,ax = plt.subplots()
            ax.bar(daydf.index,daydf.values,color = 'red' )
            plt.xticks(rotation = 45)
            st.pyplot(fig)
        with col2:
            st.title('Month Activity')
            monthdf = stats.getMonthActivity(selected_user,df)
            custom_month_order = ['January', 'February', 'March', 'April','May', 'June', 'July', 'August','September','October', 'November', 'December']
            monthdf = monthdf.reindex(custom_month_order)
            fig,ax = plt.subplots()
            ax.bar(monthdf.index,monthdf.values,color = 'yellow' )
            plt.xticks(rotation = 45)
            st.pyplot(fig)
