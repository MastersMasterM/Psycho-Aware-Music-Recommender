from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('questionnaire/<uuid:user_id>/', views.questionnaire, name='questionnaire'),
    path('results/<uuid:user_id>/', views.results, name='results'),
]
