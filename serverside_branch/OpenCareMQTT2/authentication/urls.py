from django.contrib import admin
from django.urls import path, include
from . import views

app_name = "opencare"

urlpatterns = [
    path('', views.home, name="home"), #runs the function home() in views
    path('signin', views.signin, name="signin"),
    path('signup', views.signup, name="signup"),
    path('signout', views.signout, name="signout"),
    path('profile',views.profile, name="profile"),
    path('profileedit',views.profileedit, name="profileedit"),
    path('homepage',views.homepage, name="homepage"),
    path('yourdata',views.yourdata, name="yourdata"),
    path('favorites',views.favorites, name="favorites"),
    path('search', views.search, name="search"),
    path('chart',views.chart, name="chart"),
    path('getdata',views.fetch_values, name="getdata"),
    path('livechart/<id>',views.livechart, name="livechart"),
    path('leaderboard',views.leaderboard, name="leaderboard"),
    path('keyreq',views.keyreq, name="publickey")
]