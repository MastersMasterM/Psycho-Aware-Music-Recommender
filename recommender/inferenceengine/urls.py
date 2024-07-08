from django.urls import path
from . import views

urlpatterns = [
    path('', views.questionnaire, name='questionnaire'),
    path('results/<uuid:user_id>/', views.results, name='results'),
]
