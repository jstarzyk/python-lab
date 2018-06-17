from django.contrib.auth import views as auth_views
from django.urls import path

from app import views

urlpatterns = [
    path('', views.HomePageView.as_view()),
    path('login/', views.CustomLoginView.as_view()),
    path('logout/', auth_views.LogoutView.as_view()),
    path('register/', views.CustomRegisterView.as_view()),
    path('home/', views.HomePageView.as_view()),
    path('student/', views.StudentView.as_view()),
    path('teacher/', views.TeacherView.as_view()),
    path('mark/<int:pk>/', views.UpdateMark.as_view()),
    path('mark/add/', views.AddMark.as_view()),
    path('mark/<int:pk>/delete/', views.DeleteMark.as_view())
]
