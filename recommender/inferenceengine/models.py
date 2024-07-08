from django.db import models
import uuid

class User(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateField(auto_now_add=True)
    user_name = models.CharField(max_length=100)
    user_mood = models.CharField(max_length=100, default=None, blank=True, null=True)
    user_submood = models.CharField(max_length=100, default=None, blank=True, null=True)
    user_personality = models.CharField(max_length=100, default=None, blank=True, null=True)
    user_personality_degree = models.CharField(max_length=100, default=None, blank=True, null=True)
    user_subpersonality = models.CharField(max_length=100, default=None, blank=True, null=True)
    user_activity = models.CharField(max_length=100, default=None, blank=True, null=True)
    user_location = models.CharField(max_length=100, default=None, blank=True, null=True)
    user_timeofday = models.CharField(max_length=100, default=None, blank=True, null=True)
    user_social_context = models.CharField(max_length=100, default=None, blank=True, null=True)

    # Fields for storing recommendations
    key_signatures = models.JSONField(default=list, blank=True, null=True)
    tempo = models.JSONField(default=list, blank=True, null=True)
    valence = models.JSONField(default=list, blank=True, null=True)
    instrumentalness = models.JSONField(default=list, blank=True, null=True)

class Question(models.Model):
    MOOD = 'MOOD'
    PERSONALITY = 'PERSONALITY'
    CONTEXTUAL = 'CONTEXTUAL'
    QUESTION_TYPE_CHOICES = [
        (MOOD, 'Mood'),
        (PERSONALITY, 'Personality'),
        (CONTEXTUAL, 'Contextual'),
    ]

    id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=255)
    question_type = models.CharField(max_length=15, choices=QUESTION_TYPE_CHOICES)
    mood = models.CharField(max_length=100, blank=True, null=True)
    submood = models.CharField(max_length=100, blank=True, null=True)
    trait = models.CharField(max_length=100, blank=True, null=True)
    facet = models.CharField(max_length=100, blank=True, null=True)
    choices = models.JSONField(blank=True, null=True)

class Answer(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)

class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    current_question = models.IntegerField(default=0)