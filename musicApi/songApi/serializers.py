from rest_framework import serializers
from .models import Artist, Song, Playlist, Occupations
from django.contrib.auth.models import User

class OccupationsSerializer(serializers.ModelSerializer):
    class Meta:
        model:Occupations
        fields = '__all__'
        depth = 2
        
class ArtistSerializer(serializers.ModelSerializer):
    occupation = OccupationsSerializer(many=True)
    class Meta:
        model = Artist
        fields = ['name','full_name','occupation']
        depth = 1

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['occupation'] = [occupation['occ_name'] for occupation in representation['occupation']]
        return representation

class SongSerializer(serializers.ModelSerializer):  
    class Meta:
        model = Song
        fields = ['title','movie_name','genre','duration','release','artists']
        depth = 1


class PlaylistSerializer(serializers.ModelSerializer):
    songs = SongSerializer(many=True, read_only=True)

    class Meta:
        model = Playlist
        fields = ['name','songs']
        depth = 1


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])

        return user
