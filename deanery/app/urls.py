from django.urls import path, include
from django.contrib.auth import views as auth_views
from app import views

urlpatterns = [
    path('', views.HomePageView.as_view()),
    # path('', auth_views.LoginView.as_view()),
    # path('about/', views.AboutPageView.as_view()),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    # path('register/', views.RegisterView.as_view(), name='register'),
    path('register/', views.AddPerson.as_view()),
    # path('register/', views.AddPerson.as_view(), name='register'),
    # path('add_person', views.RegisterView.as_view()
    path('password-change-done/',
         auth_views.password_change_done,
         {'template_name': 'app/password_change_done.html'},
         name='password_change_done'
         ),
    path('accounts/', include('django.contrib.auth.urls'))
    # path('')
]
