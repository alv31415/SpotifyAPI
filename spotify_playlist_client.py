import requests  # used to make requests
import navigator  # file containing code using selenium to automatically browse
import json  # used to create JSON strings
import datetime  # used to determine expiration time of token

from urllib.parse import urlencode  # used to parse URLs for queries in Spotify

from spotify_search_client import SptfySearchClient  # used to search using the Spotify API


class SptfyPlaylistClient:
    """
    Class managing Spotify Web API communication when working with playlists
    """

    def __init__(self, client_id, client_secret):

        """
        client_id: client id. Provided by Spotify when we register the app.
        client_secret: client secret. Provided by Spotify when we register the app.
        access_token: token obtained should authorisation be successful.
        expiration_time: time at which token expires.
        """

        self.client_id = client_id
        self.client_secret = client_secret

        self.access_token = None
        self.expiration_time = None

    def get_request_body(self, playlist_name, public="false", collaborative="false", description="A playlist"):

        """
        Creates a request body for Spotify API when working with playlists.
        :param playlist_name: name for the playlist we want to create.
        :param public: a boolean String used to determine whether the playlist ought to be public or private.
        :param collaborative: a boolean String used to determine whether the playlist ought to be collaborative or not.
        :param description: the description for the playlist
        """

        return {
            "name": playlist_name,
            "description": description,
            "public": public,
            "collaborative": collaborative
        }

    def get_header(self, token):

        """
        Creates a header for the request to the Spotify API when working with playlists.
        :param token: the token to be used within the header.
        """

        my_token = token

        if my_token is None:
            my_token = self.get_access_token()

        return {
            "Authorization": f"Bearer {my_token}",
            "Content-Type": "application/json"
        }

    def get_token(self, user_id, password, walkthrough_mode=False):

        """
        Returns the access token, using "navigator".
        This method is used to get a token that requires user identification (i.e to modify a personal playlist)
        If it doesn't exist, or is expired, it requests authorisation, and returns the new token
        :param user_id: the username of the Spotify Account in which the playlist is to be created.
        :param password: the password of the Spotify Account in which the playlist is to be created.
        :param walkthrough_mode: a boolean value used to determine whether the user sees the token obtaining process
        """

        expires = self.expiration_time
        now = datetime.datetime.now()

        if (self.access_token == None) or (expires == None) or (expires < now):
            self.access_token = navigator.extract_token(user_id=user_id, password=password,
                                                        walkthrough_mode=walkthrough_mode)
            expires_in = 3600
            self.expiration_time = now + datetime.timedelta(seconds=expires_in)

        return self.access_token

    def get_access_token(self):

        """
        Returns the access token, using spotify_search_client.
        This method is used to get a token when getting data from public (or private) playlists
        If it doesn't exist, or is expired, it requests authorisation, and returns the new token
        :param user_id: the username of the Spotify Account in which the playlist is to be created.
        :param password: the password of the Spotify Account in which the playlist is to be created.
        :param walkthrough_mode: a boolean value used to determine whether the user sees the token obtaining process
        """

        s = SptfySearchClient(client_id=self.client_id, client_secret=self.client_secret)

        token = self.access_token
        expires = self.expiration_time
        now = datetime.datetime.now()

        if (token == None) or (expires == None) or (expires < now):
            token = s.get_access_token()
            self.access_token = token
            self.expiration_time = s.expiration_time

        return token

    def check_boolean_value(self, playlist_argument, playlist_parameter):

        """
        Used to ensure that boolean Strings are either "true" or "false"
        For example, when creating a request body
        :param playlist_argument: the argument that receives the parameter. Either "public" or "collaborative".
        :param playlist_parameter: the parameter of the argument. If it isn't "true" or "false",
        we return "false" as a default value
        """

        my_parameter = playlist_parameter.lower()

        if (my_parameter != "false") and (my_parameter != "true"):
            print(
                f"Parameter '{playlist_parameter}' is invalid for argument '{playlist_argument}'. Only 'true' and 'false' are allowed. Using 'false' as default")
            my_parameter = "false"

        return my_parameter

    def create_playlist(self, user_id, password, walkthrough_mode=False, playlist_name="Automated Playlist",
                        public="false", collaborative="false", description="A playlist"):

        """
        Creates a playlist using the provided parameters. Returns the id of the created playlist.
        :param user_id: the username of the Spotify Account in which the playlist is to be created.
        :param password: the password of the Spotify Account in which the playlist is to be created.
        :param walkthrough_mode: a boolean value used to determine whether the user sees the token obtaining process
        :param playlist_name: name for the playlist we want to create.
        :param public: a boolean String used to determine whether the playlist ought to be public or private.
        :param collaborative: a boolean String used to determine whether the playlist ought to be collaborative or not.
        :param description: the description for the playlist
        """

        token = self.get_token(user_id=user_id, password=password, walkthrough_mode=walkthrough_mode)

        user_playlist_url = f"https://api.spotify.com/v1/users/{user_id}/playlists"

        playlist_public = self.check_boolean_value(playlist_argument="public", playlist_parameter=public)

        playlist_collaborative = self.check_boolean_value(playlist_argument="collaborative",
                                                          playlist_parameter=collaborative)

        request_body = json.dumps(
            self.get_request_body(playlist_name, public=playlist_public, collaborative=playlist_collaborative,
                                  description=description))
        header = self.get_header(token=token)

        r = requests.post(user_playlist_url, data=request_body, headers=header)
        print(f"Create Playlist: {r.status_code}")
        return r.json()["id"]

    def add_tracks_to_playlist(self, user_id, password, playlist_id, tracks, walkthrough_mode=False):

        """
        Given a list of songs, adds them to a playlist.
        If no list is provided, a ValueError is raised.
        :param user_id: the username of the Spotify Account in which the playlist is to be created.
        :param password: the password of the Spotify Account in which the playlist is to be created.
        :param walkthrough_mode: a boolean value used to determine whether the user sees the token obtaining process
        :param playlist_id: the id of the playlist.
        :param tracks: a list of song names to be added to the playlist
        """

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
            raise ValueError("You need to provide a list of song names to add to a playlist")

    def remove_tracks_from_playlist(self, user_id, password, playlist_id, remove_tracks,
                                    walkthrough_mode=False):

        """
        Given a list of songs, removes them from a playlist.
        If no list is provided, a ValueError is raised.
        :param user_id: the username of the Spotify Account in which the playlist is to be created.
        :param password: the password of the Spotify Account in which the playlist is to be created.
        :param walkthrough_mode: a boolean value used to determine whether the user sees the token obtaining process
        :param playlist_id: the id of the playlist.
        :param remove_tracks: a list of song names to be removed from the playlist
        """

        if isinstance(remove_tracks, list):
            playlist_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
            token = self.get_token(user_id=user_id, password=password, walkthrough_mode=walkthrough_mode)

            s = SptfySearchClient(client_id=self.client_id, client_secret=self.client_secret)

            uri_tracks = [uri for uri in [s.get_track(track) for track in remove_tracks]]
            remove_tracks_dict_list = [{"uri": track_uri} for track_uri in uri_tracks]
            request_body = json.dumps({"tracks": remove_tracks_dict_list})

            header = self.get_header(token=token)

            r = requests.delete(playlist_url, data=request_body, headers=header)
            print(f"Remove {len(remove_tracks)} items from playlist {playlist_id}: {r.status_code}")
        else:
            raise TypeError("You need to provide a list of song names to remove from a playlist")

    def get_playlist(self, playlist_id, market=None):

        """
        Given a playlist_id and its market, returns a JSON containing the playlist's information.
        :param playlist_id: the id of the playlist.
        :param market: an ISO 3166-1 alpha-2 country code, for the market of interest.
        """

        token = self.get_access_token()
        header = {"Authorization": f"Bearer {token}"}

        url = f"https://api.spotify.com/v1/playlists/{playlist_id}"

        if market != None:
            query = urlencode({"market": market})
            url = f"{url}?{query}"

        r = requests.get(url=url, headers=header)

        print(f"Get Playlist with ID {playlist_id}: {r.status_code}")

        return r.json()

    def get_playlist_tracks(self, playlist_id, market=None, limit=20):

        """
        Given a playlist_id and its market, returns a JSON containing the playlist's information.
        :param playlist_id: the id of the playlist.
        :param market: an ISO 3166-1 alpha-2 country code, for the market of interest.
        :param limit: the number of tracks returned.
        """

        token = self.get_access_token()
        header = {"Authorization": f"Bearer {token}"}

        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"

        if market != None:
            query = urlencode({"market": market, "limit": limit})
            url = f"{url}?{query}"

        r = requests.get(url=url, headers=header)

        print(f"Get Tracks from Playlist with ID {playlist_id}: {r.status_code}")

        return r.json()

    def get_playlist_id(self, playlist_name):

        """
        Given the name of a playlist, returns its id.
        We use the SptfySearchClient class to search for playlist_name.
        If a playlist's name is playlist_name, return the corresponding id.
        If there is no match, a ValueError is raised.
        :param playlist_name: the name of the playlist.
        """

        s = SptfySearchClient(client_id=self.client_id, client_secret=self.client_secret)
        playlists_found = s.search({"playlist": playlist_name}, content_type="playlist", limit=50)

        for playlist in playlists_found["playlists"]["items"]:
            if playlist["name"] == playlist_name:
                return playlist["id"]

        raise ValueError(f"{playlist_name} was not found in our search results")
