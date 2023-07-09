from typing import Any
from django.db import models
from django.contrib.auth.models import User
class Occupations(models.Model):
    occ_name = models.CharField(max_length=100)

class Artist(models.Model):
    name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=100,null=True)
    occupation = models.ManyToManyField(Occupations,related_name='artist')

class Song(models.Model):
    title = models.CharField(max_length=100)    
    movie_name = models.CharField(max_length=100,null=True)
    genre = models.CharField(max_length=100,null=True)
    duration = models.PositiveIntegerField()  # Duration in seconds
    release = models.CharField(max_length=25,null=True)
    artists = models.ManyToManyField(Artist, related_name='song')


    def __str__(self):
        return self.title
    
class Playlist(models.Model):    
    name = models.CharField(max_length=100)
    user = models.ManyToManyField(User, related_name='playlist')
    songs = models.ManyToManyField(Song, related_name='playlist')
    # Add more fields as per your requirements
    
