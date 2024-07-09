from django.shortcuts import render, redirect
from .models import User, Question, Answer, UserProgress
from .services.Forward_Chaining import ExpertSystem
from django.views.decorators.csrf import csrf_exempt
from .services.dataf import casebase


def home(request):
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        user = User.objects.create(user_name=user_name)
        #request.session['user_id'] = user.uid  # Save the user_id in the session
        return redirect('questionnaire', user_id=user.uid)  # Redirect to questionnaire
    return render(request, 'inferenceengine/home.html')

@csrf_exempt  # Consider using CSRF protection for POST requests
def questionnaire(request, user_id):
    user = User.objects.get(uid=user_id)
    user_name = user.user_name

    if request.method == 'POST':
        user_progress, created = UserProgress.objects.get_or_create(user=user)
        question_id = request.POST.get('question_id')
        answer_text = request.POST.get('answer')

        if 'responses' not in request.session:
            request.session['responses'] = {}

        request.session['responses'][question_id] = answer_text
        request.session.modified = True

        user_progress.current_question += 1
        user_progress.save()

        current_question_index = user_progress.current_question
        questions = list(Question.objects.all())  # Convert to list for index access
        if current_question_index < len(questions):
            question = questions[current_question_index]
        else:
            responses = []
            for question_id, answer_text in request.session['responses'].items():
                question = Question.objects.get(id=question_id)

                if question.choices:
                    response_text = answer_text
                    response_score = None
                else:
                    try:
                        response_score = int(answer_text)
                    except ValueError:
                        response_score = None
                    response_text = None

                Answer.objects.create(user=user, question=question, answer_text=answer_text)
                responses.append({
                    'mood': question.mood,
                    'submood': question.submood,
                    'trait': question.trait,
                    'facet': question.facet,
                    'response': response_score,
                    'response_choices': response_text
                })
            
            del request.session['responses']
            user = User.objects.get(uid=user_id)
            evaluate_mood(user, responses)
            evaluate_personality(user, responses)
            save_contextual_factors(user, responses)
            expert_sys(user)
            
            return redirect('results', user_id=user.uid)

    else:
        user_progress, created = UserProgress.objects.get_or_create(user=user)
        current_question_index = user_progress.current_question
        questions = list(Question.objects.all())  # Convert to list for index access
        if current_question_index < len(questions):
            question = questions[current_question_index]
        else:
            return redirect('results', user_id=user.uid)

    return render(request, 'inferenceengine/questionnaire.html', {'question': question, 'user_name': user_name})

def results(request, user_id):
    user = User.objects.get(uid=user_id)
    recommendations = {
        'Key Signatures': user.key_signatures,
        'Tempo': user.tempo,
        'Valence': user.valence,
        'Instrumentalness': user.instrumentalness
    }
    list_case_base = casebase('./inferenceengine/services/case_base.csv', recommendations)
    print(f"*********** \n {list_case_base}")
    return render(request, 'inferenceengine/results.html', {'user': user, 'recommendations': recommendations, 'case_base':eval(list_case_base)})

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

def expert_sys(user):
    es = ExpertSystem('inferenceengine/services/rules.json')
    es.facts['Task'] = 'Make recommendation'
    es.facts["User's Mood"] = user.user_mood
    es.facts['Submood'] = user.user_mood
    es.facts["User's Personality Trait"] = user.user_personality

    es.facts["Personality"] = {user.user_personality : string_to_dict(user.user_personality_degree)}

    es.facts["Activity"] = user.user_activity
    es.facts["Location"] = user.user_location
    es.facts["Time of Day"] = user.user_timeofday
    es.facts["Social Context"] = user.user_social_context
    es.forward_chain()

    print("****************************")
    print("Recommended Query Parameters are as follows:")
    print(f"Key Signutures: {es.facts['Key']}")
    print(f"Tempo: {es.facts['Tempo']}")
    print(f"Valence: {es.facts['Valence']}")
    print(f"Instrumentalness: {es.facts['Instrumentalness']}")

    # Save recommendations to the User model
    user.key_signatures = es.facts.get('Key', [])
    user.tempo = es.facts.get('Tempo', [])
    user.valence = es.facts.get('Valence', [])
    user.instrumentalness = es.facts.get('Instrumentalness', [])
    user.save()

def string_to_dict(input_str):
    # Split the string by commas to get each key-value pair
    pairs = input_str.split(', ')
    
    # Initialize an empty dictionary
    result_dict = {}
    
    # Loop through each pair
    for pair in pairs:
        # Split the pair by the colon to get the key and value
        key, value = pair.split(': ')
        # Add the key-value pair to the dictionary
        result_dict[key] = value
    
    return result_dict