from rest_framework.decorators import api_view
from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Song, Playlist, Artist,Occupations
from knox.models import AuthToken
from .serializers import ArtistSerializer, SongSerializer, PlaylistSerializer,UserSerializer, RegisterSerializer
from rest_framework.exceptions import ValidationError

from django.contrib.auth import login
from django.contrib.auth.models import User
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework.pagination import PageNumberPagination

from django.db.models import Q

# pagenation for songs model
class SongPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50

@api_view(['GET', 'POST'])
def clear_data(request):
    datas = [Playlist]
    for data in datas:
        data.objects.all().delete()
    return Response({'msg':'delete successfully'})
@api_view(['GET', 'POST'])
def song_list_create(request):
    if request.method == 'GET':
        # add pagenation for song list
        queryset = Song.objects.all()
        paginator = SongPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = SongSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

        # songs = Song.objects.all()
        # serializer = SongSerializer(songs, many=True)
        # return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data
        title = data.get('title')
        movie_name = data.get('movie_name')
        duration = data.get('duration')

        # Check if the song already exists
        existing_song = Song.objects.filter(title=title, movie_name=movie_name, duration=duration).first()
        if existing_song:
            serializer = SongSerializer(existing_song)
            return Response(serializer.data, status=200)
        serializer = SongSerializer(data=request.data)
        if serializer.is_valid():
            song = serializer.save()

            artists_data = request.data.get('artists', [])
            for artist_data in artists_data:
                artist_name = artist_data['name']
                artist_serializer = ArtistSerializer(data=artist_data)
                artist, _ = Artist.objects.get_or_create(name=artist_name, full_name=artist_data['full_name'])
                for occupations in artist_data['occupation']:
                    for occupation in occupations:
                        # import pdb;pdb.set_trace()
                        occ, _ = Occupations.objects.get_or_create(occ_name=occupations[occupation])
                        artist.occupation.add(occ)

                song.artists.add(artist)

            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)    

@api_view(['GET', 'PUT', 'DELETE'])
def song_retrieve_update_destroy(request, pk):
    try:
        song = Song.objects.get(pk=pk)
    except Song.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = SongSerializer(song)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = SongSerializer(song, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    elif request.method == 'DELETE':
        song.delete()
        return Response(status=204)
    
@api_view(['GET', 'POST'])
def playlist_list_create(request):
    if request.method == 'GET':
        playlists = Playlist.objects.all()
        serializer = PlaylistSerializer(playlists, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = PlaylistSerializer(data=request.data)
        if serializer.is_valid():            
          
            playlist_name = request.data.get('name')
            song_data = request.data.get('songs')

            try:
                # need to get user id from request data
                user =User.objects.get(id=1) # now give static one
                playlist = Playlist.objects.get(user=user, name=playlist_name)
                songs = Song.objects.filter(title=song_data)

                if songs.exists():
                    # Check if the song is already added to the playlist
                    if playlist.songs.filter(title=song_data).exists():
                        raise ValidationError("Song is already added to the playlist.")

                    playlist.songs.add(songs.first())
                    return Response(serializer.data, status=201)
                else:
                    raise ValidationError("Song does not exist. Please create new song")

            except Playlist.DoesNotExist:
                playlist = serializer.save(user=user)
                songs = Song.objects.filter(title=song_data)

                if songs.exists():
                    playlist.songs.add(songs.first())
                    return Response(serializer.data, status=201)
                else:
                    raise ValidationError("Song does not exist.")

        return Response(serializer.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
def playlist_detail(request,playlist_id):
    try:    
        playlist = Playlist.objects.get(pk=playlist_id)
    except Playlist.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = PlaylistSerializer(playlist)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = PlaylistSerializer(playlist, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    elif request.method == 'DELETE':
        playlist.delete()
        return Response({"msg":"Deleted successfully!!"},status=204)

@api_view(['GET'])
def user_detail(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(status=404)
    serializer = UserSerializer(user)
    return Response(serializer.data)


@api_view(['GET'])
def search_songs(request):
    query = request.GET.get('q')
    # get songs matched query
    try:
       if query:
        songs = Song.objects.filter(
            Q(title__icontains=query) |
            Q(artists__name__icontains=query) |
            Q(genre__icontains=query)
        )
        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data)
    except songs.DoesNotExist:
        return Response(status=400, data={'message': 'No search query provided.'})



# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })
    

# Login API
class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)
