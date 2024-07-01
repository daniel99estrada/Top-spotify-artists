from spotify import SpotifyAPI
import requests

class Playlist:
    def __init__(self, spotify_api, name, description="", playlist_id=None):
        self.spotify_api = spotify_api
        self.name = name
        self.description = description
        self.playlist_id = playlist_id
        
        if not self.playlist_id:
            self._create_playlist()

    def _create_playlist(self):
        response = self.spotify_api.create_playlist(self.name, self.description)
        if response and 'id' in response:
            self.playlist_id = response['id']
        else:
            raise Exception("Failed to create playlist")

    def add_tracks(self, track_ids):
        if not self.playlist_id:
            raise Exception("Playlist ID is not set")
        
        url = f"https://api.spotify.com/v1/playlists/{self.playlist_id}/tracks"
        data = {"uris": [f"spotify:track:{track_id}" for track_id in track_ids]}
        
        return self.spotify_api.request('POST', url, data=data)

    def get_tracks(self, limit=100, offset=0):
        if not self.playlist_id:
            raise Exception("Playlist ID is not set")
        
        url = f"https://api.spotify.com/v1/playlists/{self.playlist_id}/tracks"
        params = {"limit": limit, "offset": offset}
        
        return self.spotify_api.request('GET', url, params=params)

    def remove_tracks(self, track_ids):
        if not self.playlist_id:
            raise Exception("Playlist ID is not set")
        
        url = f"https://api.spotify.com/v1/playlists/{self.playlist_id}/tracks"
        data = {"tracks": [{"uri": f"spotify:track:{track_id}"} for track_id in track_ids]}
        
        return self.spotify_api.request('DELETE', url, data=data)

    def update_details(self, name=None, description=None, public=None):
        if not self.playlist_id:
            raise Exception("Playlist ID is not set")
        
        url = f"https://api.spotify.com/v1/playlists/{self.playlist_id}"
        data = {}
        if name:
            data['name'] = name
        if description:
            data['description'] = description
        if public is not None:
            data['public'] = public
        
        return self.spotify_api.request('PUT', url, data=data)