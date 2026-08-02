from pathlib import Path
import random
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity

# Load dataset using an absolute path
BASE_DIR = Path(__file__).resolve().parent
data = pd.read_csv(BASE_DIR / "SpotifyFeatures.csv")

# Select only numeric features
numeric_features = data.select_dtypes(include=["number"])

# Scale features
scaler = StandardScaler()
scaled_data = scaler.fit_transform(numeric_features)


def recommend(song_name, top_n=5):
    song_name = song_name.lower()
    track_names = data["track_name"].str.lower()

    # Find matching songs
    matches = data[track_names.str.contains(song_name, na=False)]

    if not matches.empty:
        idx = matches.index[0]

        similarity_scores = cosine_similarity(
            [scaled_data[idx]], scaled_data
        )[0]

        similar_indices = similarity_scores.argsort()[-top_n - 1:-1][::-1]

        return data.iloc[similar_indices]["track_name"].tolist()

    # Return random songs if no match is found
    return data["track_name"].sample(top_n).tolist()


if __name__ == "__main__":
    print(recommend("Shape of You"))
