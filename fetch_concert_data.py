##########################################################
"""
fetch_concert_data.py

Handles Ticketmaster API integration to fetch concert events for 
specified artists. This includes artist lookups, event retrieval, 
and data formatting into a pandas DataFrame.

Functions:
- fetch_artist_id: Retrieves the Ticketmaster ID for a given artist.
- fetch_event: Retrieves event details for a specified artist.
- get_ticketmaster_events: Fetches concert data for a list of artists.

Dependencies:
- Aiohttp for asynchronous requests.
- Tqdm for progress bars.
"""
##########################################################

# importing packages

import aiohttp
import asyncio
import pandas as pd
from tqdm import tqdm
import os
from dotenv import load_dotenv
load_dotenv()

######################################################

TICKETMASTER_API_KEY = os.getenv('TICKETMASTER_API_KEY')

async def fetch_artist_id(session, artist_name):
    url = f"https://app.ticketmaster.com/discovery/v2/attractions.json?apikey={TICKETMASTER_API_KEY}&keyword={artist_name}"
    async with session.get(url) as response:
        data = await response.json()
        print(f"API Response for {artist_name}: {data}")  # This will show what the API actually returns
        if response.status == 429:
            print(f"Rate limit exceeded for {artist_name}. Waiting...")
            await asyncio.sleep(30)
            return await fetch_artist_id(session, artist_name)
        elif data.get("_embedded"):
            for attraction in data["_embedded"]["attractions"]:
                if attraction["name"].lower() == artist_name.lower():
                    return attraction["id"]
        else:
            print(f"No artist ID found for {artist_name}, Response: {data}")
            return None

async def fetch_event(session, artist_id, artist_name):
    url = f"https://app.ticketmaster.com/discovery/v2/events.json?apikey={TICKETMASTER_API_KEY}&attractionId={artist_id}"
    async with session.get(url) as response:
        if response.status == 429:
            print(f"Rate limit exceeded for artist: {artist_name}. Waiting for 2 seconds...")
            await asyncio.sleep(2)
            return await fetch_event(session, artist_id, artist_name)
        data = await response.json()
        if not data.get("_embedded"):
            print(f"No events found for artist: {artist_name}")
            return []
        events = data["_embedded"]["events"]
        event_list = []
        for event in events:
            try:
                event_list.append({
                    "Artist": artist_name,
                    "Date": event["dates"]["start"]["localDate"],
                    "Venue": event["_embedded"]["venues"][0]["name"],
                    "City": event["_embedded"]["venues"][0]["city"]["name"],
                    "Country": event["_embedded"]["venues"][0]["country"]["name"],
                })
            except KeyError:
                continue
        return event_list

async def get_ticketmaster_events(artist_names):
    async with aiohttp.ClientSession() as session:
        all_events = []
        for artist_name in tqdm(artist_names, desc="Fetching concert data"):
            artist_id = await fetch_artist_id(session, artist_name)
            if artist_id:
                result = await fetch_event(session, artist_id, artist_name)
                if result:
                    all_events.extend(result)
            await asyncio.sleep(1)
            
        if all_events:
            events_df = pd.DataFrame(all_events, columns=['Artist', 'Date', 'Venue', 'City', 'Country'])

            os.makedirs('data', exist_ok=True)  # Ensure the 'data/' folder exists
            events_df.to_csv('data/concerts.csv', index=False)
        else:
            events_df = pd.DataFrame()

        return events_df

def main():
    artist_names = ['Taylor Swift', 'Sabrina Carpenter', 'Clairo']
    events_df = asyncio.run(get_ticketmaster_events(artist_names))
    print(events_df)

if __name__ == "__main__":
    main()

############################################################