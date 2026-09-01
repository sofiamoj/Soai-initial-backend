from django.urls import path
from . import views


app_name = 'course'
urlpatterns = [
    path('', views.CourseView.as_view(), name='course'),
    path('exercise/<int:pk>/', views.ExerciseView.as_view(), name='exercise'),
]
