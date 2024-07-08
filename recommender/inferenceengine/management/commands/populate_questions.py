from django.core.management.base import BaseCommand
from inferenceengine.models import Question

class Command(BaseCommand):
    help = 'Populate the Question table with predefined questions'

    def handle(self, *args, **kwargs):
        questions = [
            {"text": "I feel elated and high-energy.", "mood": "Happy", "submood": "Elated"},
            {"text": "I feel content and positive.", "mood": "Happy", "submood": "Content"},
            {"text": "I feel melancholic and reflective.", "mood": "Sad", "submood": "Melancholic"},
            {"text": "I feel depressed and low.", "mood": "Sad", "submood": "Depressed"},
            {"text": "I feel stressed and anxious.", "mood": "Anxious", "submood": "Stressed"},
            {"text": "I feel worried and uneasy.", "mood": "Anxious", "submood": "Worried"},
            {"text": "I feel relaxed and calm.", "mood": "Calm", "submood": "Relaxed"},
            {"text": "I feel peaceful and at ease.", "mood": "Calm", "submood": "Peaceful"}
        ]
        
        personality_questions = [
            {"text": "I have a vivid imagination.", "trait": "Openness", "facet": "Imagination"},
            {"text": "I have artistic interests.", "trait": "Openness", "facet": "ArtisticInterests"},
            {"text": "I am emotionally expressive.", "trait": "Openness", "facet": "Emotionality"},
            {"text": "I like order and structure.", "trait": "Conscientiousness", "facet": "Orderliness"},
            {"text": "I am dutiful and responsible.", "trait": "Conscientiousness", "facet": "Dutifulness"},
            {"text": "I am outgoing and sociable.", "trait": "Extraversion", "facet": "Sociability"},
            {"text": "I assert myself when needed.", "trait": "Extraversion", "facet": "Assertiveness"},
            {"text": "I often feel happy and upbeat.", "trait": "Extraversion", "facet": "PositiveEmotions"},
            {"text": "I trust others easily.", "trait": "Agreeableness", "facet": "Trust"},
            {"text": "I am altruistic and caring.", "trait": "Agreeableness", "facet": "Altruism"},
            {"text": "I often feel anxious.", "trait": "Neuroticism", "facet": "Anxiety"},
            {"text": "I often feel depressed.", "trait": "Neuroticism", "facet": "Depression"}
        ]

        contexual_questions = [
            # Activity Question
            {"text": "What are you currently doing?", "question_type": "PERSONALITY", "trait": "Activity", "choices": ["Studying", "Working Out", "Relaxing"]},
            # Location Questions
            {"text": "Where are you currently?", "question_type": "PERSONALITY", "trait": "Location", "choices": ["Home", "Work", "Outdoors"]},
            # Time of Day Questions
            {"text": "What time of day is it?", "question_type": "PERSONALITY", "trait": "Time of Day", "choices": ["Morning", "Afternoon", "Evening"]},
            # Social Context Questions
            {"text": "Who are you with?", "question_type": "PERSONALITY", "trait": "Social Context", "choices": ["Alone", "With Friends", "With Family"]},
        ]
        
        for q in questions:
            Question.objects.get_or_create(
                text=q['text'],
                question_type='Mood',
                mood=q['mood'],
                submood=q['submood']
            )
        
        for pq in personality_questions:
            Question.objects.get_or_create(
                text=pq['text'],
                question_type='Personality',
                trait=pq['trait'],
                facet=pq['facet']
            )
        
        for cq in contexual_questions:
            Question.objects.get_or_create(**cq)

        self.stdout.write(self.style.SUCCESS('Successfully populated the Question table with mood and personality questions.'))
