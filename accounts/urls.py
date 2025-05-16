from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login', views.login_user, name='login'),
    path('home/',views.render_home, name='home' ),
    path('activate/<uid>/<token>/', views.activate_user, name='activate'),
]
