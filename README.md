# Concert Recommendation Project

## Overview
This project integrates Spotify's API to fetch the user's top artists and Ticketmaster's API to retrieve concert events for those artists. The data is then processed and displayed in a simple dashboard using Streamlit. The goal is to help users discover live events for their favorite artists based on their current Spotify listening preferences.

## Table of Contents
- [Data](#data)
- [Methods](#methods)
- [Results](#results)
- [Project Structure](#project-structure)
- [Notes](#notes)

### Data
The data for this project is fetched from two sources:
1. **Spotify API**: Retrieves the top artists of the user.
2. **Ticketmaster API**: Retrieves concert event data for those artists.

These datasets are then processed and used to create an interactive dashboard. **Please note that you must provide your own Spotify and Ticketmaster API keys in order to use this project, and it is currently not set up for public use.**

### Methods
1. **Spotify API**: The project uses the Spotify Web API to fetch the user's top artists based on their listening history.
2. **Ticketmaster API**: The project uses the Ticketmaster API to find concerts associated with those top artists.
3. **Streamlit**: The concert data is displayed in a user-friendly, interactive dashboard using Streamlit.
4. **Pandas**: Used for data manipulation and storage.

### Results
The app displays a list of concerts for the user's top artists. Users can filter the events by date range and specific artists. Additionally, users can download the filtered event data as a CSV. **Please note that this app is designed to access only your personal Spotify data.**

### Project Structure
```plaintext
Spotify_Ticketmaster_Project/
│
├── app.py                  # Main Streamlit app script
├── fetch_spotify_data.py   # Fetches data from the Spotify API
├── fetch_concert_data.py   # Fetches data from the Ticketmaster API
├── data/                   # Directory containing data files
│   ├── top_artists.csv     # Saved top artist data from Spotify
│   └── concerts.csv        # Saved concert data from Ticketmaster
├── requirements.txt        # Project dependencies
└── .env                    # File to store API credentials (not pushed to GitHub)
```

### Notes
- **Personal Use Only**: The current implementation of this project is intended for personal use. Please be aware of the privacy and legal implications involved in using Spotify and Ticketmaster's APIs.
- This project is **not** set up to allow others to use their own data for now.
- Further steps may be needed to ensure compliance with user rights and data privacy laws before sharing this with others.

---
**Author:** Mia Jaenike<br>
**Contact:** miaajaenike@gmail.com<br>
**Last Updated**: 2024-12-11
