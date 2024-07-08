from django.shortcuts import render, redirect
from .models import User, Question, Answer


def questionnaire(request):
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        user = User.objects.create(user_name=user_name)
        responses = []

        for key, answer_text in request.POST.items():
            if key.startswith('question_'):
                question_id = int(key.split('_')[1])
                question = Question.objects.get(id=question_id)

                if question.choices:
                    # For multiple-choice questions
                    response_text = answer_text
                    response_score = None
                else:
                    # For numeric questions
                    try:
                        response_score = int(answer_text)
                    except ValueError:
                        response_score = None  # Ignore invalid numeric responses
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
        
        evaluate_mood(user, responses)
        evaluate_personality(user, responses)
        
        return redirect('results', user_id=user.uid)
    else:
        questions = Question.objects.all()
        return render(request, 'inferenceengine/questionnaire.html', {'questions': questions})


def results(request, user_id):
    user = User.objects.get(uid=user_id)
    answers = Answer.objects.filter(user=user)
    return render(request, 'inferenceengine/results.html', {'user': user, 'answers': answers})

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
