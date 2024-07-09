import pandas as pd
from scipy.spatial.distance import hamming
import numpy as np

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

def casebase_retrive(dir, user_profile):
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

def casebase_retain(dir, user_profile, recommendations):
    df = pd.read_csv(dir)

    user_profile_tempo = user_profile.tempo[0]
    user_profile_valence = user_profile.valence[0]
    user_profile_instrumentalness = user_profile.instrumentalness[0]
    user_profile_key_signatures = user_profile.key_signatures

    # Extract only the titles from the recommendations
    recommendation_titles = [rec['title'] for rec in recommendations]

    # Create a new row with the user profile and recommendation titles
    new_row = {
        'Key Signatures': [user_profile_key_signatures],
        'Tempo': user_profile_tempo,
        'Valence': user_profile_valence,
        'Instrumentalness': user_profile_instrumentalness,
        'Recommended Songs': [recommendation_titles]
    }

    # Append the new row to the DataFrame
    df = pd.concat([df, pd.DataFrame(new_row)], ignore_index=True)
    # Save the updated DataFrame back to the CSV file
    df.to_csv(dir, index=False)
