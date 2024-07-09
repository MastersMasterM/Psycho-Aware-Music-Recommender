import pandas as pd
from scipy.spatial.distance import hamming
from sklearn.metrics import jaccard_score
import numpy as np

"""
# Sample data with real songs
data = {
    'Key Signatures': [['A major', 'C major'], ['B minor', 'E minor'], ['C major', 'G major'], ['D minor', 'F major'], ['E major', 'A minor']],
    'Tempo': ['Fast', 'Medium', 'Slow', 'Fast', 'Medium'],
    'Valence': ['High', 'Low', 'High', 'Low', 'High'],
    'Instrumentalness': ['Low', 'High', 'Low', 'High', 'Low'],
    'Recommended Songs': [
        ['Shape of You - Ed Sheeran', 'Blinding Lights - The Weeknd', 'Uptown Funk - Mark Ronson ft. Bruno Mars', 'Can’t Stop the Feeling! - Justin Timberlake', 'Happy - Pharrell Williams'],
        ['Lose Yourself to Dance - Daft Punk', 'Strobe - Deadmau5', 'Ghosts n Stuff - Deadmau5', 'Nero - Promises', 'Above & Beyond - Sun & Moon'],
        ['Someone Like You - Adele', 'Let Her Go - Passenger', 'All of Me - John Legend', 'Stay with Me - Sam Smith', 'Thinking Out Loud - Ed Sheeran'],
        ['Voodoo Child - Jimi Hendrix', 'Kashmir - Led Zeppelin', 'Black Sabbath - Black Sabbath', 'Highway to Hell - AC/DC', 'Iron Man - Black Sabbath'],
        ['Rolling in the Deep - Adele', 'Chandelier - Sia', 'Bad Romance - Lady Gaga', 'Firework - Katy Perry', 'Shake It Off - Taylor Swift']
    ]
}

# Create a DataFrame
df = pd.DataFrame(data)

df.to_csv('.\case_base.csv', index=False)
"""
# User profile (example)
user_profile = {
    'Key Signatures': ['C major', 'G major'],
    'Tempo': 'Slow',
    'Valence': 'High',
    'Instrumentalness': 'Low'
}

# Function to compute Jaccard distance for key signatures
def jaccard_distance(set1, set2):
    set1 = set(set1)
    set2 = set(set2)
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return 1 - intersection / union if union != 0 else 1

# Function to compute overall distance
def compute_distance(case, user_profile):
    distance = 0
    # Jaccard distance for Key Signatures
    distance += jaccard_distance(case['Key Signatures'], user_profile['Key Signatures'])
    # Hamming distance for categorical attributes
    categorical_attrs = ['Tempo', 'Valence', 'Instrumentalness']
    for attr in categorical_attrs:
        distance += hamming([case[attr]], [user_profile[attr]])
    return distance

def casebase(dir, user_profile):
    df = pd.read_csv(dir)
    print(user_profile)
    user_profile['Tempo'] = user_profile['Tempo'][0]
    user_profile['Valence'] = user_profile['Valence'][0]
    user_profile['Instrumentalness'] = user_profile['Instrumentalness'][0]
    # Compute distances and find the nearest case
    df['Distance'] = df.apply(lambda row: compute_distance(row, user_profile), axis=1)
    nearest_case = df.loc[df['Distance'].idxmin()]
    # Output the nearest case
    print("Nearest case to the user profile:")
    print(nearest_case['Recommended Songs'])
    return nearest_case['Recommended Songs']