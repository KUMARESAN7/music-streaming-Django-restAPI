# music-streaming-Django-restAPI

Certainly! Here's an example of how you can prepare the documentation for your Django REST Framework project to submit to the client:

# Project Name

## Overview
Provide a brief overview of the project, describing its purpose and main functionalities.

## Technologies Used
- Django: [4.2.3]
- Django REST Framework: [3.14.0]
- Other relevant technologies used in the project

## Setup Instructions
Provide step-by-step instructions for setting up and running the project locally. Include any necessary dependencies and configuration steps. For example:

1. Clone the repository: `git clone [repository_url]`
2. Install dependencies: `pip install -r requirements.txt`
3. Configure the database settings in `settings.py`
4. Apply migrations: `python manage.py migrate`
5. Start the development server: `python manage.py runserver`
6. Access the project at `http://localhost:8000/`

## API Endpoints

### Songs
- `GET /api/songs/`: Retrieves a list of all songs.
    
- `POST /api/songs/`: Creates a new song.
- `GET /api/songs/{song_id}/`: Retrieves details of a specific song.
- `PUT /api/songs/{song_id}/`: Updates details of a specific song.
- `DELETE /api/songs/{song_id}/`: Deletes a specific song.

### Playlists
- `GET /api/playlists/`: Retrieves a list of all playlists.
- `POST /api/playlists/`: Creates a new playlist.
- `GET /api/playlists/{playlist_id}/`: Retrieves details of a specific playlist.
- `PUT /api/playlists/{playlist_id}/`: Updates details of a specific playlist.
- `DELETE /api/playlists/{playlist_id}/`: Deletes a specific playlist.

### Search data
- `GET /api/search/?q={query}` Filer songs from songlist.
## Data Models

### Song
- `id`: Auto-generated identifier for the song.
- `title`: The title of the song.
- `movie_name`: The movie_name of this song.
- `genre`: The genre of this song.
- `artist`: Many-to-many relationship with the `Artist` model.
- Any other relevant fields.

### Playlist
- `id`: Auto-generated identifier for the playlist.
- `name`: The name of the playlist.
- `songs`: Many-to-many relationship with the `Song` model.
- Any other relevant fields.
### Artist
- `id`: Auto-generated identifier for the playlist.
- `name`: The name of the Artist.
- `full_name`:Full name of the Artist
- `occupation`: Many-to-many relationship with the `Occupations` model.

## Serializers
Provide a description of the serializers used to convert the model instances to JSON and vice versa.

- `SongSerializer`: Serializes/deserializes the `Song` model.
- `PlaylistSerializer`: Serializes/deserializes the `Playlist` model.
- `ArtistSerializer`:Serializes/deserializes the `Artist` model.



