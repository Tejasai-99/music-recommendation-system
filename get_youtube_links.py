import pandas as pd
from googleapiclient.discovery import build

API_KEY = "AIzaSyCosrBwt6wVXAHj5SDEShQARlRnQ6vA3OU"
youtube = build("youtube", "v3", developerKey=API_KEY)

df = pd.read_csv("SpotifyFeatures.csv")

possible_names = ["title", "song", "track_name", "name"]
song_column = None
for col in df.columns:
    if col.lower() in possible_names:
        song_column = col
        break
if song_column is None:
    song_column = df.columns[0]

print(f"🎵 Using column: {song_column}")

urls = []
for title in df[song_column]:
    try:
        request = youtube.search().list(
            q=title,
            part="snippet",
            type="video",
            maxResults=1
        )
        response = request.execute()

        if response.get("items") and "videoId" in response["items"][0]["id"]:
            video_id = response["items"][0]["id"]["videoId"]
            urls.append(f"https://www.youtube.com/watch?v={video_id}")
        else:
            urls.append(None)

    except Exception as e:
        print(f"⚠️ Error for '{title}': {e}")
        urls.append(None)

df["song_url"] = urls
df.to_csv("songs_with_urls.csv", index=False)
print("✅ Done! Links saved to songs_with_urls.csv")
