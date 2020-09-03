import requests  # used to make requests
import base64  # used for token request header
import datetime  # used to determine expiration time of token
from urllib.parse import urlencode  # used to parse URLs for queries in Spotify

class SptfySearchClient:

    """
    Class managing Spotify Web API communication when searching for artists, albums, playlists, etc...
    """

    def __init__(self, client_id, client_secret):

        """
        client_id: client id. Provided by Spotify when we register the app.
        client_secret: client secret. Provided by Spotify when we register the app.
        request_body: request body for the "Clients Credentials Flow" token request.
        token_url: URL to request token.
        base_url: base URL for communicating with the API.
        access_token: token obtained should authorisation be succesful.
        expiration_time: time at which token expires.
        access_token_expired: boolean to determine whether token has expired.
        """

        self.client_id = client_id
        self.client_secret = client_secret

        self.request_body = {"grant_type" : "client_credentials"}
        self.token_url = "https://accounts.spotify.com/api/token"
        self.base_url = "https://api.spotify.com/v1"

        self.access_token = None
        self.expiration_time = None
        self.access_token_expired = True

    def credentials_to_base64(self):

        """
        According to Spotify API, a users' credentials are in the form: <client_id> : <client_secret>
        To create the header for the token request, we have to turn these credentials into a base 64 String
        """

        if self.client_id == None or self.client_secret == None:
            raise Exception("Client ID and Secret required to receive a token")
        else:
            credentials = f"{self.client_id}:{self.client_secret}"
            return base64.b64encode(credentials.encode())

    def get_token_header(self):

        """
        The token header requires the following format
        Authorization: Basic <base64 encoded client_id:client_secret>
        Used to request authorisation & obtain a token
        """

        return {"Authorization" : f"Basic {self.credentials_to_base64().decode()}"}

    def get_auth(self):

        """
        Performs an authorisation request to Spotify API
        If successful, we obtain a token
        """

        r = requests.post(self.token_url, data = self.request_body, headers = self.get_token_header())

        if r.status_code != 200:
            raise Exception("Client couldn't be authenticated")

        now = datetime.datetime.now()
        token_response = r.json()

        self.access_token = token_response["access_token"]
        expires_in = token_response["expires_in"]

        self.expiration_time = now + datetime.timedelta(seconds=expires_in)
        self.access_token_expired = now > self.expiration_time

        return True

    def get_access_token(self):

        """
        Returns the access token
        If it doesn't exist, or is expired, it requests authorisation, and returns the new token
        """

        token = self.access_token
        expires = self.expiration_time
        now = datetime.datetime.now()

        if (token == None) or (expires == None) or (expires < now):
            self.get_auth()
            return self.get_access_token()
        else:
            return token

    def get_request_header(self):

        """
        The request header used to obtain data from the API
        Used in search queries & for getting resources (albums, artists)
        """

        access_token = self.get_access_token()
        return {"Authorization": f"Bearer {access_token}"}

    def simple_search(self, search_query):

        """
        Basic search code
        :param search_query: the parameters that we want to search for
        i.e an artist name, an album name, etc ...
        These are appended to the url that is used when sending a request
        Formatted by the search method
        """
        # https://developer.spotify.com/documentation/web-api/reference/search/search/

        search_endpoint = "https://api.spotify.com/v1/search"  # endpoints are where the program communicates with the API
        lookup_url = f"{search_endpoint}?{search_query}"  # ? tells us that the query begins
        request_header = self.get_request_header()
        r = requests.get(lookup_url, headers = request_header)
        if r.status_code != 200:
            return {}
        return r.json()

    def search(self,search_parameters = None, operator = None, operator_query = None, content_type = "track", limit = 20):

        """
        Used to develop the search query to be appended at the end of the URL for searching in "simple_search"
        :param search_parameters: the name of what we are looking for (i.e the song name, artist name, etc ...)
        as keys for the dictionary, use: album, artist, playlist or track
        i.e {"artist" : "Imagine Dragons", "album" : "Night Visions"}
        :param operator: the operator to use. Either "not" or "or. Used to reduce search results.
        :param operator_query: the object to which we apply the operator (i.e an artist name)
        :param content_type: the "type" of the "search parameter".
        Valid types are: album , artist, playlist, track, show and episode.
        :param limit: maximum number of results to return
        """
        # to understand queries: https://developer.spotify.com/documentation/web-api/reference/search/search/

        if search_parameters == None:
            raise Exception("You need to search for something!")

        if isinstance(search_parameters, dict):  # ensure we have a dictionary
            query_list = [f"{k}:{v}" for k, v in search_parameters.items()]
            query = " ".join(query_list)  # separates items by spaces; urlencode manages the formatting

        if operator != None and operator_query != None:
            if operator.lower() == "or" or operator.lower() == "not":
                operator = operator.upper()  # if valid operator make it a capital letter
                if isinstance(operator_query, str):
                    query = f"{query} {operator} {operator_query}"

        search_query = urlencode({"q": query,
                                  "type": content_type.lower(),
                                  "limit": limit})  # search_query is used to create a URL, so we use urllib to correctly format it

        return self.simple_search(search_query)

    def get_track(self, track_name):

        """
        Returns the URI of a track
        :param track_name: the track that we want to look for
        """

        search_param = {"track" : track_name}
        track = self.search(search_parameters = search_param, content_type = "track", limit = 1)

        return track["tracks"]["items"][0]["uri"]  # returns the URI of the first search result


    def get_albums_url(self, album_id, keyword = "none"):

        """
        Creates the url to get an album, as specified by the provided album_id and keyword
        :param album_id: the id of the desired album.
        :param keyword: keyword used to complete the url
        -> "none": search the album
        -> "tracks": search for the tracks of an album
        -> if any other word is included, a general album search url will be provided
        """

        album_url = f"{self.base_url}/albums"
        search_key = ""

        if keyword == "none":
            search_key = f"/{album_id}"
        elif keyword == "tracks":
            search_key = f"/{album_id}/{keyword}"
        else:
            print(f"You chose the keyword '{keyword}'. You can only use 'none' or 'tracks'.")

        return f"{album_url}{search_key}"

    def get_artists_url(self, artist_id, keyword = "none", country = None):

        """
        Creates the url to get an artist, as specified by the provided artist_id and keyword
        :param artist_id: the id of the desired album
        :param keyword: keyword used to complete the url
        -> "none": search the artist
        -> "albums": search for the artists' albums
        -> "top-tracks": search for the artists' top-tracks
        -> "related-artists": search for the artists' related artists
        -> if any other word is included, a general artist search url will be provided
        """

        keys = ["none", "albums", "top-tracks", "related-artists"]
        artist_url = f"{self.base_url}/artists"
        search_key = ""

        if keyword in keys:
            if keyword == "none":
                search_key = f"/{artist_id}"
            elif keyword == "top-tracks":
                if country is None:
                    print("No country was provided to display top tracks, or an incorrect country code was given. "
                          "\nUsing 'US' as default.")
                    country = "US"
                search_key = f"/{artist_id}/{keyword}?country={country.upper()}"
            else:
                search_key = f"/{artist_id}/{keyword}"
        else:
            print(f"You chose the keyword '{keyword}', which isn't within the allowed ones: {keys}")

        return f"{artist_url}{search_key}"

    def get_resource(self, id, resource_type = "artist", keyword = "none", country = None):

        """
        Returns data concerning a resource of type "resource_type" with id "id"
        Search specified by "keyword"
        Uses the methods get_artists_url and get_albums_url
        :param id: the id corresponding to the resource
        i.e Avicci => 1vCWHaC5f2uS3yhpwWbIA6
        :param resource_type: whether we are looking for an album or an artist. Artist is the defualt
        :param keyword: keyword used to specify the searach
        """

        lookup_url = self.get_artists_url(artist_id = id , keyword = keyword, country = country)

        if resource_type.lower() == "album":
            lookup_url = self.get_albums_url(album_id = id , keyword = keyword)
        elif resource_type.lower() != "artist":
            print(f"'{resource_type}' is not a valid resource type. Passing default value: 'artist'.")

        request_header = self.get_request_header()  # pass in the token
        r = requests.get(lookup_url, headers=request_header)

        if r.status_code != 200:
            print(f"Status Code: {r.status_code}")
            print("There was a problem. Perhaps you need to specify the content_type, or ensure the keyword is appropiate.")
            return {}
        return r.json()

    def print_search_result(self, search_parameters = None, operator = None, operator_query = None, content_type = "track", limit = 20):

        """
        Uses the parameters to execute the method "search" to neatly print the important aspects of a search results:
        - artist: name, id, url, uri
        - album: name, id, number of tracks, release date, url, uri
        """

        search_results = self.search(search_parameters = search_parameters, operator = operator, operator_query = operator_query, content_type = content_type, limit = limit )

        for my_album in search_results["tracks"]["items"]:
            artist_info = my_album["artists"][0]

            artist_url = artist_info["external_urls"]["spotify"]
            artist_id = artist_info["id"]
            artist_name = artist_info["name"]
            artist_uri = artist_info["uri"]

            print(f"Artist: {artist_name}")
            print(f"ID: {artist_id}")
            print(f"URL: {artist_url}")
            print(f"URI: {artist_uri}\n")

            my_album_info = my_album["album"]

            album_url = my_album_info["external_urls"]["spotify"]
            album_id = my_album_info["id"]
            album_release = my_album_info["release_date"]
            album_tracks = my_album_info["total_tracks"]
            album_name = my_album_info["name"]
            album_uri = my_album_info["uri"]

            print(f"Album: {album_name}")
            print(f"ID: {album_id}")
            print(f"Tracks: {album_tracks}")
            print(f"Release Date: {album_release}")
            print(f"URL: {album_url}")
            print(f"URI: {album_uri}\n")
            print("----------------------------\n")

    def print_artist(self, id, keyword = "none", country = None):

        """
        Uses the parameters to execute the method "get_resource"
        to neatly print the important aspects of an artist resource:
        -> name, id, followers, popularity 8out of 100), url and uri
        """

        artist_resource = self.get_resource(id, resource_type = "artist", keyword = keyword, country = country)

        artist_url = artist_resource["external_urls"]["spotify"]
        artist_followers = "{:,}".format(artist_resource["followers"]["total"])
        artist_popularity  = artist_resource["popularity"]
        artist_id = artist_resource["id"]
        artist_name = artist_resource["name"]
        artist_uri = artist_resource["uri"]

        print(f"Artist: {artist_name}")
        print(f"ID: {artist_id}")
        print(f"Followers: {artist_followers}")
        print(f"Popularity: {artist_popularity}/100")
        print(f"URL: {artist_url}")
        print(f"URI: {artist_uri}\n")


    def print_album(self, id, keyword = "none", country = None):

        """
        Uses the parameters to execute the method "get_resource"
        to neatly print the important aspects of an album resource:
        - artist: name, id, url, uri
        - album: name, id, release date, popularity, number of tracks, url, uri and all the songs in the album
        """

        album_resource = self.get_resource(id, resource_type = "album", keyword = keyword, country = country)

        for artist_info in album_resource["artists"]:

            artist_url = artist_info["external_urls"]["spotify"]
            artist_id = artist_info["id"]
            artist_name = artist_info["name"]
            artist_uri = artist_info["uri"]

            print(f"Artist: {artist_name}")
            print(f"ID: {artist_id}")
            print(f"URL: {artist_url}")
            print(f"URI: {artist_uri}\n")

        album_url = album_resource["external_urls"]["spotify"]
        album_id = album_resource["id"]
        album_release = album_resource["release_date"]
        album_popularity = album_resource["popularity"]
        album_tracks = album_resource["total_tracks"]
        album_name = album_resource["name"]
        album_uri = album_resource["uri"]

        print(f"Album: {album_name}")
        print(f"ID: {album_id}")
        print(f"Release Date: {album_release}")
        print(f"Popularity: {album_popularity}/100")
        print(f"Tracks: {album_tracks}")
        print(f"URL: {album_url}")
        print(f"URI: {album_uri}\n")
        print(f"Songs from {album_name}:")
        self.print_tracks(album_resource["tracks"])

    def print_top_tracks(self, id, country):

        """
        Neatly prints the top tracks
        Includes information on the artist, the album of the track, and the track itself.
        :param top_tracks_resource: the dictionary returned from using the get_resource method with "album" as resource_type
        """

        top_tracks_resource = self.get_resource(id, resource_type="artist", keyword="top-tracks", country=country)

        my_top_tracks = top_tracks_resource["tracks"]

        for index,top_track in enumerate(my_top_tracks):

            album_info = top_track["album"]

            album_url = album_info["external_urls"]["spotify"]
            album_id = album_info["id"]
            album_release = album_info["release_date"]
            album_tracks = album_info["total_tracks"]
            album_name = album_info["name"]
            album_uri = album_info["uri"]

            track_duration = top_track["duration_ms"]
            track_popularity = top_track["popularity"]
            track_url = top_track["external_urls"]["spotify"]
            track_id = top_track["id"]
            track_name = top_track["name"]
            track_uri = top_track["uri"]

            print(f"{index + 1} - {track_name} --- {self.from_ms(track_duration)}")
            print(f"\tPopularity: {track_popularity}/100")
            print(f"\tID: {track_id}")
            print(f"\tURL: {track_url}")
            print(f"\tURI: {track_uri}")
            print("\t------------------------")
            for artist_info in top_track["artists"]:

                artist_url = artist_info["external_urls"]["spotify"]
                artist_id = artist_info["id"]
                artist_name = artist_info["name"]
                artist_uri = artist_info["uri"]

                print(f"\tArtist: {artist_name}")
                print(f"\tID: {artist_id}")
                print(f"\tURL: {artist_url}")
                print(f"\tURI: {artist_uri}")
            print("\t------------------------")
            print(f"\tAlbum: {album_name}")
            print(f"\tID: {album_id}")
            print(f"\tRelease Date: {album_release}")
            print(f"\tTracks: {album_tracks}")
            print(f"\tURL: {album_url}")
            print(f"\tURI: {album_uri}\n")

    def print_tracks(self, track_resource):

        """
        Helper method for print_album used to print the information on the tracks from an album
        Info on: track number, duration, url, id, track name, uri
        """

        my_tracks = track_resource["items"]

        for track in my_tracks:
            track_number = track["track_number"]
            track_duration = track["duration_ms"]
            track_url = track["external_urls"]["spotify"]
            track_id = track["id"]
            track_name = track["name"]
            track_uri = track["uri"]

            print(f"{track_number} - {track_name} --- {self.from_ms(track_duration)}")
            print(f"\tID: {track_id}")
            print(f"\tURL: {track_url}")
            print(f"\tURI: {track_uri}\n")


    def from_ms(self,millis):

        """
        Helper method for print_album used to convert milliseconds into minutes and seconds
        """

        seconds = (millis // 1000) % 60
        minutes = (millis // (1000 * 60)) % 60

        if seconds < 10:
            seconds = f"0{seconds}"

        return f"{minutes}:{seconds}"







