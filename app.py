import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly_express as px
import seaborn as sns
import plotly.graph_objects as go
sns.set()
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(layout="wide")

header = st.container()
dataset = st.container()
Visualisation = st.container()
@st.cache_data
def get_data():
    df = pd.read_csv("netflix_titles.csv")
    return df
df = get_data()

# TODO : Header
with header:
    st.title("Welcome to ***Netflix Data Analysis*** Project.")
    st.image("netflix.jpg")

def attribute_information():
    st.subheader("Attribute Information")
    st.markdown("**Show_id** : unique id of each show")
    st.markdown("**Type**    : I create this featuree")
    st.markdown("**Title** : Name of the show")
    st.markdown("**Director**    : Name of the director(s) of the show")
    st.markdown('**Cast**: Name of actors and other cast of the show')
    st.markdown("**Country**: Name of countries the show is available to watch on Netflix")
    st.markdown("**Date_added**: Date when the show was added on Netflix")
    st.markdown("**Release_year**: Release year of the show")
    st.markdown("**Rating**: Show rating on netflix")
    st.markdown("**Duration**: Time duration of the show")
    st.markdown("**Listed_in**: Genre of the show")
    st.markdown("**Description**: Some text describing the show")

# TODO: About Dataset
with dataset:
    st.write("Dataset for this project is taken from [here](https://www.kaggle.com/datasets/shivamb/netflix-shows)")
    st.write(df.head(7))

# TODO: Data wrangling
df["date_added"] = pd.to_datetime(df['date_added'], errors='coerce')
df['added_year'] = df['date_added'].dt.year
df['added_day'] = df['date_added'].dt.day_name()
df['month'] = pd.DatetimeIndex(df['date_added']).month

df['added_year'].fillna(df['added_year'].mean(), inplace=True)
df["month"].fillna(df['month'].mean(), inplace=True)
df["added_year"] = df["added_year"].astype(int)
df["month"] = df["month"].astype(int)
df.fillna("Data Not Available", inplace=True)

# TODO: Visualisation
Q1,Q2 = st.columns(2)

with Q1:
    df1 = df.groupby(by='type').value_counts().reset_index()
    fig_by_type = px.pie(df,names=df['type'],title='<b>Movies & Tv shows </b>')
    fig_by_type.update_layout(title = {'x':0.5}, plot_bgcolor = "rgba(0,0,0,0)")
    st.plotly_chart(fig_by_type,use_container_width=True)
    st.subheader("There are more Movies than Tv shows in Netflix")


months_data = df[df['added_day'] != 'Data Not Available']
with Q2:
    df2 = months_data.groupby('added_day').size()
    # fig_by_month = px.pie(df, names=months_data.size(), title='<b>Movies & Tv shows </b>')
    fig_by_month = px.bar(months_data, x=months_data['added_day'], title='<b>Day wise release in netflix</b>')
    fig_by_month.update_layout(title={'x': 0.5}, xaxis=(dict(showgrid=False)), yaxis=(dict(showgrid=False)),
                                 plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_by_month, use_container_width=True)
    st.subheader("Most movies and shows in netflix are released on Friday")
st.divider()

country_data = df[df["country"] != "Data Not Available"].sort_values(by='country')
fig = plt.figure(figsize=(10,4))
sns.countplot(x="country", data=country_data, order=country_data["country"].value_counts().index[:10], hue="type",palette="YlGnBu_d").set(title='Top 10 countries of shows in netflix')
st.pyplot(fig)
st.subheader("Most Tv shows have been released in India, whilst most films have been released in the United States.")
st.divider()


# after 2016 is more tv shows or movies added in netflix?
fig2 = plt.figure(figsize=(15,7))
movie = df[df["type"] == "Movie"]
tv_shows = df[df["type"] == "TV Show"]
movie_added_total = movie["added_year"].value_counts()
tv_shows_added_total = tv_shows["added_year"].value_counts()
sns.lineplot(x=movie_added_total.index,y=movie_added_total.values, color="mediumseagreen", label="movie").set(title='Frequency of content added by Netflix (2008 - 2021)')
sns.lineplot(x=tv_shows_added_total.index,y=tv_shows_added_total.values, color="teal", label="Tv shows")
st.pyplot(fig2)
st.subheader("we can see the frequency of content added by Netflix from 2008 to 2021. The plot shows that there has been a steady increase "
             "in the number of titles added each year, with a notable jump in 2015. We can also see that the number of movies added has "
             "generally been higher than the number of TV shows added each year.")
st.divider()


# Top rating movies in the last century
fig3 = plt.figure(figsize=(15,7))
plt.title("Top 10 movies according to their rating")
movies_before_2000 = df[df["release_year"] < 2000]
sns.countplot(x="rating",data=movies_before_2000,order=movies_before_2000["rating"].value_counts().index[:10],hue="type",palette="YlGnBu_d").set(title="Top 10 movies according to their rating")
st.pyplot(fig3)
st.subheader("This chart displays the frequency of each distinct value in the 'rating' column, broken down by the type of "
             "content (a movie or TV show). We can observe from this plot how the ratings for films and TV series are distributed differently. "
             "We can see that TV episodes and films with the TV-14 rating tend to be more common.")
st.divider()


# Top 10 actors in netflix
tmp=pd.DataFrame()
tmp=df['cast'].str.split(',',expand=True).stack().to_frame()
tmp.columns=['actors']
actor_info=tmp.groupby(['actors']).size().reset_index(name='Total Shows')
actor_info = actor_info[actor_info['actors'] != 'Data Not Available']
actor_info = actor_info.sort_values(by='Total Shows', ascending=False)[:15]
fig4 = plt.figure(figsize=(15,7))
sns.barplot(y='actors', x='Total Shows', data=actor_info, palette="crest").set(title="Top Actors in netflix")
st.pyplot(fig4)
st.divider()


# columns
Q3,Q4 = st.columns(2, gap="medium")

with Q3:
    # Indian tv shows w.r.t. rating
    indian_shows = df[df.country == "India"]
    df1 = indian_shows.query("type == 'TV Show'")
    df1 = df1[["title", "rating"]]
    df1 = df1.groupby('rating')["title"].count().reset_index().sort_values('title', ascending = False)
    df1 = df1.rename(columns = {"title": "movies_count"})
    fig5 = px.bar(df1, x='rating', y='movies_count', color_discrete_sequence=['teal'],
           title='Tv shows in India w.r.t rating')
    fig5.update_layout()
    st.write(fig5)
    st.subheader("We can see that Indian Tv shows with TV-MA rating tend to be more common.")

with Q4:
    #Movies in India according to their rating
    df_2 = indian_shows.query("type == 'Movie'")
    df_2 = df_2[["title", "rating"]]
    df_2 = df_2.groupby(['rating'])["title"].count().reset_index().sort_values('title', ascending = False)
    df_2 = df_2.rename(columns = {"title": "movies_count"})
    fig6 = px.bar(df_2, x='rating', y='movies_count', color_discrete_sequence=px.colors.sequential.BuPu_r,
           title='Movies in India according to their rating ')
    fig6.update_layout()
    st.write(fig6)
    st.subheader("We can see that Indian Movies with TV-14 rating tend to be more common.")

st.divider()
# columns
Q5,Q6 = st.columns(2, gap="small")

with Q5:
    #Movies/TV Shows average release monthly trend
    df_4 = indian_shows.query("release_year >= 2007")
    df_4 = df_4[["type", "month", 'release_year', "show_id"]]
    df_4 = df_4.groupby(['release_year', 'month', 'type'])['show_id'].count().reset_index()
    df_4 = df_4.rename(columns={"show_id": "total_shows"})
    df_4 = df_4.groupby(['month', 'type'])['total_shows'].mean().reset_index()

    df_4_movie = df_4.query("type == 'Movie'")
    df_4_show = df_4.query("type == 'TV Show'")

    fig7 = go.Figure()
    fig7.add_trace(go.Scatter(
        x=df_4_movie['month'],
        y=df_4_movie['total_shows'],
        showlegend=True,
        text=df_4_movie['total_shows'],
        name='Movie',
        marker_color='Maroon'

    ))
    fig7.add_trace(go.Scatter(
        x=df_4_show['month'],
        y=df_4_show['total_shows'],
        showlegend=True,
        text=df_4_show['total_shows'],
        name='TV Show',
        marker_color='Grey'
    ))

    fig7.update_traces(mode='lines+markers')
    fig7.update_layout(title_text='Movies/TV Shows average release monthly trend')
    fig7['layout']['xaxis']['title'] = 'Month'
    fig7['layout']['yaxis']['title'] = 'No. of movies/Tv Shows'
    st.write(fig7)

with Q6:
    #
    def trend_yearwise(year):
        title = (f'Indian Movies/TV Show release Month Trend for year {year}')
        df_6 = indian_shows.query("release_year == @year")
        df_6 = df_6.groupby(["type", "month"])["show_id"].count().reset_index()
        df_6_movie = df_6.query("type == 'Movie'")
        df_6_show = df_6.query("type == 'TV Show'")

        fig8 = go.Figure()
        fig8.add_trace(go.Scatter(
            x=df_6_movie['month'],
            y=df_6_movie['show_id'],
            showlegend=True,
            text=df_6_movie['show_id'],
            name='Movie',
            marker_color='Maroon'

        ))
        fig8.add_trace(go.Scatter(
            x=df_6_show['month'],
            y=df_6_show['show_id'],
            showlegend=True,
            text=df_6_show['show_id'],
            name='TV Show',
            marker_color='Grey'
        ))

        fig8.update_traces(mode='lines+markers')
        fig8.update_layout(title_text=title)
        st.write(fig8)



    trend_yearwise(2020)

st.divider()
st.write("For github link: [click here](https://github.com/Anynomous25/Netflix_EDA_webapp)")