##########################################################
"""
app.py

Main script for the Concert Data Dashboard Streamlit application.
Integrates Spotify and Ticketmaster APIs to display concert data 
for the user's top Spotify artists. 

Features:
- Filters for artist, date range, city, and country.
- Interactive data table and CSV downloads.

Run this script to launch the dashboard.
"""
##########################################################

import streamlit as st
import pandas as pd
import asyncio
from fetch_spotify_data import get_top_artists
from fetch_concert_data import get_ticketmaster_events
from datetime import datetime, date

##########################################################

async def search_concerts_for_top_artists():
    spotify_df = get_top_artists()
    artist_names = spotify_df['name'].tolist()
    all_concerts_df = await get_ticketmaster_events(artist_names)

    combined_data = []
    for _, artist_row in spotify_df.iterrows():
        artist_name = artist_row['name']
        artist_concerts = all_concerts_df[all_concerts_df['Artist'].str.contains(artist_name, case=False, na=False)]
        for _, concert_row in artist_concerts.iterrows():
            combined_data.append({
                'Artist': artist_name,
                'Concert Date': concert_row['Date'],
                'Venue': concert_row['Venue'],
                'City': concert_row['City'],
                'Country': concert_row['Country'],
            })
    combined_df = pd.DataFrame(combined_data)
    combined_df['Concert Date'] = pd.to_datetime(combined_df['Concert Date'], errors='coerce')
    return combined_df

# Fetch Spotify and Ticketmaster data and store it in session state
if 'combined_df' not in st.session_state:
    with st.spinner("Fetching data..."):
        st.session_state.combined_df = asyncio.run(search_concerts_for_top_artists())

# Verify the DataFrame columns
# st.write("Combined Data Columns:", st.session_state.combined_df.columns)

# Remove duplicate events
st.session_state.combined_df = st.session_state.combined_df.drop_duplicates(subset=['Artist', 'Concert Date', 'Venue'])

st.title('Concert Data Dashboard')

st.sidebar.header('Filters')

# Set the default date range to show all upcoming concerts
today = date.today()
max_date = st.session_state.combined_df['Concert Date'].max().date() if not st.session_state.combined_df.empty else today
date_range = st.sidebar.date_input("Select date range", [today, max_date], min_value=today, key='date_range')

if len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date = end_date = date_range[0]

# Artist dropdown
artist_names = st.session_state.combined_df['Artist'].unique().tolist()
selected_artist = st.sidebar.selectbox('Search Artist', options=[""] + artist_names, index=0, key='artist_search')

# Country dropdown
country_names = st.session_state.combined_df['Country'].unique().tolist()
selected_country = st.sidebar.selectbox('Filter by Country', options=[""] + country_names, index=0, key='country_filter')

# Filter DataFrame based on the selected criteria
filtered_df = st.session_state.combined_df

if selected_artist:
    filtered_df = filtered_df[filtered_df['Artist'] == selected_artist]

if selected_country:
    filtered_df = filtered_df[filtered_df['Country'] == selected_country]

# Display the filtered DataFrame
st.dataframe(filtered_df)

# Filter the DataFrame based on the selected date range
st.write(filtered_df)

st.download_button(
    label="Download data as CSV",
    data=filtered_df.to_csv(index=False).encode('utf-8'),
    file_name='filtered_concert_data.csv',
    mime='text/csv',
)

##########################################################