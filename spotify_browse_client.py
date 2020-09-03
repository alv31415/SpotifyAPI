import requests
import json
import datetime
from urllib.parse import urlencode
from spotify_search_client import SptfySearchClient

class SptfyBrowseClient:

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

        self.browse_url = "https://api.spotify.com/v1/browse"
        self.categories_url = f"{self.browse_url}/categories"
        self.releases_url = f"{self.browse_url}/new-releases"

        self.access_token = None
        self.expiration_time = None

    def get_access_token(self):

        s = SptfySearchClient(client_id = self.client_id, client_secret = self.client_secret)

        token = self.access_token
        expires = self.expiration_time
        now = datetime.datetime.now()

        if (token == None) or (expires == None) or (expires < now):
            token = s.get_access_token()
            self.access_token = token
            self.expiration_time = s.expiration_time

        return token

    def get_request_url_dict(self, category_query = "get_ids", country = None, locale = None, limit = 20):
            request_dict = {}

            valid_category_query = ["get_ids", "get_category", "get_category_playlist", "get_releases"]

            if not (category_query in valid_category_query):
                raise ValueError("You must select a valid category query for a valid query. Use either 'ids', 'get_category' or 'get_category_playlist'")

            if country != None:
                request_dict["country"] = country
            if locale != None and category_query != "get_category_playlist" and category_query != "get_releases":
                request_dict["locale"] = locale
            if (limit > 0) and (limit <= 50) and isinstance(limit, int) and category_query != "get_category":
                request_dict["limit"] = limit
            elif category_query != "get_category":
                print("Limit must be a postitive integer between 1 and 50 (inclusive). Using '20' as default")

            return request_dict

    def get_request_url(self, base_url, category_query = "get_ids", country = None, locale = None, limit = 20):
        """
        :param category_query: the type of query. Depening on it (ids, get_category, get_category_playlist), certain arguments (i.e country, locale, limit) are innecessary
        :param country: A country, shown as n ISO 3166-1 alpha-2 country code. No value corresponds to a globally relevant query search.
        :param locale: The desired language, consisting of an ISO 639-1 language code and an ISO 3166-1 alpha-2 country code, joined by an underscore.
        (i.e "es_MX" refers to Spanish music fromm mexico)
        :param limit: The maximum number of categories to return. Default: 20. Minimum: 1. Maximum: 50.
        :return: A url used to get a browse result
        """

        query_dict = self.get_request_url_dict(category_query = category_query, country = country, locale = locale, limit = limit)

        browse_query = urlencode(query_dict)

        return f"{base_url}?{browse_query}"

    def get_header(self, token = None):

        my_token = token

        if my_token is None:
            my_token = self.get_access_token()

        return {"Authorization" : f"Bearer {my_token}"}

    def get_category_ids(self, country = None, locale = None, limit = 20):
        token = self.get_access_token()
        category_id_url = self.get_request_url(base_url = self.categories_url, category_query = "get_ids", country = country, locale = locale, limit = limit)
        header = self.get_header(token)

        r = requests.get(url = category_id_url, headers = header)
        print(f"Retrieving List of Categories: {r.status_code}\n")

        return r.json()

    def print_category_ids(self, country = None, locale = None, limit = 20):
        category_ids = self.get_category_ids(country = country, locale = locale, limit = limit)

        print(f"Showing Results for {len(category_ids['categories']['items'])} Category ID(s)\n")

        for category in category_ids["categories"]["items"]:
            id = category["id"]
            name = category["name"]
            print(f"Category ID: {id}")
            print(f"Category Name: {name}\n")

    def get_category(self, category_id = "toplists", country = None, locale = None):
        base_url = f"{self.categories_url}/{category_id}"

        token = self.get_access_token()
        category_url = self.get_request_url(base_url = base_url, category_query = "get_category", country = country, locale = locale)
        header = self.get_header(token)

        r = requests.get(url = category_url, headers = header)

        print(f"Retrieving Category with ID {category_id}: {r.status_code}\n")

        return r.json()

    def get_category_playlists(self, category_id = "toplists", country = None, limit = 20):
        base_url = f"{self.categories_url}/{category_id}/playlists"

        token = self.get_access_token()
        category_playlist_url = self.get_request_url(base_url = base_url, category_query = "get_category_playlist", country = country, limit = limit)
        header = self.get_header(token)

        r = requests.get(url = category_playlist_url, headers = header)

        print(f"Retrieving Playlist(s) for Category with ID {category_id}: {r.status_code}\n")

        return r.json()

    def print_category_playlists(self, category_id = "toplists", country = None, limit = 20):
        category_playlists = self.get_category_playlists(category_id = category_id, country = country, limit = limit)

        for playlist in category_playlists["playlists"]["items"]:
            collaborative = playlist["collaborative"]
            description = playlist["description"]
            url = playlist["external_urls"]["spotify"]
            id = playlist["id"]
            name = playlist["name"]
            tracks = playlist["tracks"]["total"]
            public = playlist["public"]

            print(f"Playlist Name: {name}")
            print(f"Description: {description}")
            print(f"Collaborative: {collaborative}")
            print(f"Public: {public}")
            print(f"Tracks: {tracks}")
            print(f"Playlist ID: {id}")
            print(f"Playlist URL: {url}\n")

    def get_playlist_from_category(self, playlist_name, category_id = "toplists", country = None, limit = 20):
        category_playlists = self.get_category_playlists(category_id = category_id, country = country, limit = limit)

        for playlist in category_playlists["playlists"]["items"]:
            if playlist["name"] == playlist_name:
                return playlist
            else:
                print(playlist["name"])

        raise ValueError(f"{playlist_name} is not a playlist within the category {category_id}")

    def get_new_releases(self, country = None, limit = 20):
        base_url = self.releases_url

        token = self.get_access_token()
        category_playlist_url = self.get_request_url(base_url=base_url, category_query="get_releases", country=country, limit=limit)
        header = self.get_header(token)

        r = requests.get(url=category_playlist_url, headers=header)

        print(f"Retrieving New Releases: {r.status_code}\n")

        with open("JSONs/new-releases.json", "w") as f:
            json.dump(r.json(), f, indent = 4)

        return r.json()

    def print_new_releases(self, country = None, limit = 20):
        new_releases = self.get_new_releases(country = country, limit = limit)

        for release in new_releases["albums"]["items"]:
            for artist in release["artists"]:
                artist_url = artist["external_urls"]["spotify"]
                artist_id = artist["id"]
                artist_name = artist["name"]
                artist_uri = artist["uri"]

                print(f"Artist: {artist_name}")
                print(f"ID: {artist_id}")
                print(f"URL: {artist_url}")
                print(f"URI: {artist_url}\n")

            track_url = release["external_urls"]["spotify"]
            track_id = release["id"]
            track_name = release["name"]
            track_date = release["release_date"]
            track_tracks = release["total_tracks"]
            track_uri = release["uri"]

            print(f"Album: {track_name}")
            print(f"Tracks: {track_tracks}")
            print(f"Release Date: {track_date}")
            print(f"ID: {track_id}")
            print(f"URL: {track_url}")
            print(f"URI: {track_uri}\n")
            print("----------------------------\n")

