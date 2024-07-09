import json
import requests

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from .models import User, Question, Answer, UserProgress
from .services.Forward_Chaining import ExpertSystem

from .services.casebase_engine import casebase_retrive, casebase_retain
from .services.Evaluation_User import evaluate_mood, evaluate_personality, save_contextual_factors

    
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
    list_case_base = casebase_retrive('./inferenceengine/services/case_base.csv', recommendations)
    mood = user.user_mood
    youtube_response = requests.get(f'http://127.0.0.1:8000/fetch-youtube-recommendations/{mood}/').json()
    youtube_recommendations = youtube_response.get('recommendations', [])
    
    casebase_retain('./inferenceengine/services/case_base.csv', user, youtube_recommendations)
    
    return render(request, 'inferenceengine/results.html', {
        'user': user,
        'recommendations': recommendations,
        'case_base': eval(list_case_base),
        'youtube_recommendations': youtube_recommendations
    })


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

def fetch_youtube_recommendations(request, mood):
    api_key = 'AIzaSyAj2QLlcj_8e6q_GXBSMthLGOTd_xMhGjg'
    query = f'mood {mood} official music'
    url = f'https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&type=video&key={api_key}&maxResults=5'
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        recommendations = [
            {
                'title': item['snippet']['title'],
                'link': f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                'image_url': item['snippet']['thumbnails']['high']['url']
            }
            for item in data['items']
        ]
        return JsonResponse({'status': 'success', 'recommendations': recommendations, 'data': data})
    else:
        return JsonResponse({'status': 'error', 'message': 'Failed to fetch YouTube recommendations'}, status=500)