def evaluate_mood(user, responses):
    mood_counts = {"Happy": 0, "Sad": 0, "Anxious": 0, "Calm": 0}
    submood_counts = {"Elated": 0, "Content": 0, "Melancholic": 0, "Depressed": 0, "Stressed": 0, "Worried": 0, "Relaxed": 0, "Peaceful": 0}
    mood_submood_map = {"Happy": ["Elated", "Content"], "Sad": ["Melancholic", "Depressed"], "Anxious": ["Stressed", "Worried"], "Calm":["Relaxed", "Peaceful"]}
    
    for r in responses:
        if r['mood']:
            mood_counts[r['mood']] += r['response']
        if r['submood']:
            submood_counts[r['submood']] += r['response']
    
    primary_mood = max(mood_counts, key=mood_counts.get)
    feasible_submood = mood_submood_map[primary_mood]
    sub = {x: submood_counts[x] for x in feasible_submood}
    primary_submood = max(sub, key=sub.get)
    
    user.user_mood = primary_mood
    user.user_submood = primary_submood
    user.save()

def evaluate_personality(user, responses):
    traits = {}
    for r in responses:
        if r['trait'] and r['facet']:
            trait = r['trait']
            facet = r['facet']
            if trait not in traits:
                traits[trait] = {}
            if facet not in traits[trait]:
                traits[trait][facet] = 0
            traits[trait][facet] += r['response']
    
    personality_profile = {}
    trait_score_max = 0
    dominant_trait = None

    for trait, facets in traits.items():
        personality_profile[trait] = {}
        t_score = 0
        for facet, score in facets.items():
            t_score += score
            if score >= 3:  # Example threshold for high
                personality_profile[trait][facet] = "High"
            else:
                personality_profile[trait][facet] = "Low"
        if t_score > trait_score_max:
            trait_score_max = t_score
            dominant_trait = trait

    user.user_personality = dominant_trait
    user.user_personality_degree = ', '.join([f"{facet}: {level}" for facet, level in personality_profile[dominant_trait].items()])
    user.save()

def save_contextual_factors(user, responses):
    # Initialize contextual factors
    activity = None
    location = None
    time_of_day = None
    social_context = None
    
    # Iterate over responses and map them to the appropriate user fields
    for response in responses:
        if response['trait'] == 'Activity':
            activity = response['response_choices']
        elif response['trait'] == 'Location':
            location = response['response_choices']
        elif response['trait'] == 'Time of Day':
            time_of_day = response['response_choices']
        elif response['trait'] == 'Social Context':
            social_context = response['response_choices']
    
    # Update the User model fields
    if activity:
        user.user_activity = activity
    if location:
        user.user_location = location
    if time_of_day:
        user.user_timeofday = time_of_day
    if social_context:
        user.user_social_context = social_context
    
    user.save()