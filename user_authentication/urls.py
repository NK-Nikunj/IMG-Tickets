from django.urls import path

# import views to associate urls
from . import views

app_name = 'tickets'
urlpatterns = [
    path('', views.login_view, name='login'),
    path('signup/', views.register_view, name='register'),
    path('signout/', views.logout_view, name='logout'),
]
