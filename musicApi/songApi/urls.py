from django.urls import path,include
from knox import views as knox_views

from .views import LoginAPI,RegisterAPI

from . import views

urlpatterns = [
    path('songs/', views.song_list_create, name='song-list-create'),
    path('songs/<int:pk>/', views.song_retrieve_update_destroy, name='song-retrieve-update-destroy'),
    path('playlists/', views.playlist_list_create, name='playlist-list-create'),
    path('playlists/<int:playlist_id>/', views.playlist_detail, name='playlist-retrieve-update-destroy'),
    path('users/<int:user_id>/',views.user_detail,name='user_detail'),
    path('search/',views.search_songs,name='search_songs'),
    

    # user register and login
    path('register/', RegisterAPI.as_view(), name='register'),    
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
]
