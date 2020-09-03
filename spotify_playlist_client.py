import requests
import navigator
import json
import datetime

from urllib.parse import urlencode

from spotify_search_client import SptfySearchClient

class SptfyPlaylistClient:

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

        self.token_code = None

        self.access_token = None
        self.expiration_time = None

    def get_request_body(self, playlist_name, public = "false", collaborative = "false", description = "A playlist"):
        return {
                "name": playlist_name,
                "description": description,
                "public": public,
                "collaborative" : collaborative
                }

    def get_header(self, token):

        return {
                "Authorization": f"Bearer {token}",
                "Content-Type" : "application/json"
               }

    def get_token(self, user_id, password, walkthrough_mode = False):
        expires = self.expiration_time
        now = datetime.datetime.now()

        if (self.access_token == None) or (expires == None) or (expires < now):
            self.access_token = navigator.extract_token(user_id = user_id, password = password, walkthrough_mode = walkthrough_mode)
            expires_in = 3600
            self.expiration_time = now + datetime.timedelta(seconds=expires_in)

        return self.access_token

    def get_access_token(self):

        s = SptfySearchClient(client_id = client_id, client_secret = client_secret)

        token = self.access_token
        expires = self.expiration_time
        now = datetime.datetime.now()

        if (token == None) or (expires == None) or (expires < now):
            token = s.get_access_token()
            self.access_token = token
            self.expiration_time = s.expiration_time

        return token

    def check_boolean_value(self, playlist_argument, playlist_parameter):

        my_parameter = playlist_parameter.lower()

        if (my_parameter != "false") and (my_parameter != "true"):
            print(f"Parameter '{playlist_parameter}' is invalid for argument '{playlist_argument}'. Only 'true' and 'false' are allowed. Using 'false' as default")
            my_parameter = "false"

        return my_parameter


    def create_playlist(self, user_id, password, walkthrough_mode = False, playlist_name = "Automated Playlist", public = "false", collaborative = "false", description = "A playlist"):
        token = self.get_token(user_id = user_id, password = password, walkthrough_mode = walkthrough_mode)

        user_playlist_url = f"https://api.spotify.com/v1/users/{user_id}/playlists"

        playlist_public = self.check_boolean_value(playlist_argument = "public", playlist_parameter = public)

        playlist_collaborative = self.check_boolean_value(playlist_argument = "collaborative", playlist_parameter = collaborative)

        request_body = json.dumps(self.get_request_body(playlist_name, public = playlist_public, collaborative = playlist_collaborative, description = description))
        header = self.get_header(token = token)

        r = requests.post(user_playlist_url, data = request_body, headers = header)
        print(f"Create Playlist: {r.status_code}")
        return r.json()["id"]

    def get_playlist(self, playlist_id, market = None):
        token = self.get_access_token()
        header = {"Authorization": f"Bearer {token}"}

        url = f"https://api.spotify.com/v1/playlists/{playlist_id}"

        if market != None:
            query = urlencode({"market" : market})
            url = f"{url}?{query}"

        r = requests.get(url = url, headers = header)

        print(f"Get Playlist with ID {playlist_id}: {r.status_code}")

        return r.json()

    def get_playlist_tracks(self, playlist_id, market = None, limit = 20):
        token = self.get_access_token()
        header = {"Authorization": f"Bearer {token}"}

        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"

        if market != None:
            query = urlencode({"market": market, "limit" : limit})
            url = f"{url}?{query}"

        r = requests.get(url=url, headers=header)

        print(f"Get Tracks from Playlist with ID {playlist_id}: {r.status_code}")

        return r.json()

    def get_playlist_id(self, playlist_name):
        s = SptfySearchClient(client_id = client_id, client_secret = client_secret)
        playlists_found = s.search({"playlist" : playlist_name}, content_type = "playlist", limit = 50)

        for playlist in playlists_found["playlists"]["items"]:
            if playlist["name"] == playlist_name:
                return playlist["id"]

        raise ValueError(f"{playlist_name} was not found in our search results")

    def add_tracks_to_playlist(self, user_id, password, playlist_id, tracks, walkthrough_mode = False):

        if isinstance(tracks, list):
            s = SptfySearchClient(client_id=self.client_id, client_secret=self.client_secret)
            uri_tracks = [uri for uri in [s.get_track(track) for track in tracks]]
            playlist_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
            token = self.get_token(user_id=user_id, password=password, walkthrough_mode=walkthrough_mode)

            header = self.get_header(token=token)
            request_body = json.dumps({"uris": uri_tracks})

            r = requests.post(url=playlist_url, data=request_body, headers=header)
            print(f"Add {len(tracks)} items to playlist {playlist_id}: {r.status_code}")
        else:
            raise TypeError("You need to provide a list of song names to add to a playlist")

    def remove_tracks_from_37i9dQZEVXbMDoHDwVN2tFplaylist(self, user_id, password, playlist_id, remove_tracks, walkthrough_mode = False):

        if isinstance(remove_tracks, list):
            playlist_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
            token = self.get_token(user_id=user_id, password=password, walkthrough_mode=walkthrough_mode)

            s = SptfySearchClient(client_id=self.client_id, client_secret=self.client_secret)

            uri_tracks = [uri for uri in [s.get_track(track) for track in remove_tracks]]
            remove_tracks_dict_list = [{"uri" : track_uri} for track_uri in uri_tracks]
            request_body = json.dumps({"tracks" : remove_tracks_dict_list})

            header = self.get_header(token=token)

            r = requests.delete(playlist_url, data = request_body, headers = header)
            print(f"Remove {len(remove_tracks)} items from playlist {playlist_id}: {r.status_code}")
        else:
            raise TypeError("You need to provide a list of song names to remove from a playlist")


