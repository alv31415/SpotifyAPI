# SpotifyAPI

Python project to work with the Spotify Web API. My first serious, independent Python project, and my first time working with APIs.

## Table of Contents

* [Project Structure](#project-structure)
* [Spotify Web API](#spotify-web-api)
  + [Registering an App](#registering-an-app)
  + [API Functionality](#api-functionality)
  + [Console](#console)
  + [Authorisation](#authorisation)
  + [Basic Project Workflow](#basic-project-workflow)
* [Search Client](#search-client)
  + [Requesting Auth and Obtaining a Token](#requesting-auth-and-obtaining-a-token)
  + [Making a Search](#making-a-search)
  + [Obtaining a Resource](#obtaining-a-resource)
  + [Printing Methods](#printing-methods)
* [Playlist Client](#playlist-client)
  + [Requesting Auth and Obtaining a Token](#requesting-auth-and-obtaining-a-token-1)
  + [Accessing Playlist Information](#accessing-playlist-information)
  + [Creating and Modifying a Playlist](#creating-and-modifying-a-playlist)
* [Browse Client](#browse-client)
  + [Requesting Auth and Obtaining a Token](#requesting-auth-and-obtaining-a-token-2)
  + [Query URLs](#query-urls)
  + [Working with Categories and New Releases](#working-with-categories-and-new-releases)
  + [Printing Methods](#printing-methods-1)
* [Navigator](#navigator)


## Project Structure

This project contains 4 files. 3 represent Spotify Clients, used to communicate with the Spotify Web API. 
These are:

* **spotify_search_client.py:** used to access Spotify Search Functionality. This can be used to get and print information on artists, albums, playlists, tracks, etc ...

* **spotify_playlist_client.py:** used to create, modify and acess playlists & their tracks. For creating and modifying playlists, user credentials must be included.

* **spotify_browse_client.py:** used to access the Spotify Browse Tab. This can be used to access the different categories from Spotify (i.e "mood", "summer", etc ...) and new releases.

The last one (**navigator.py**), uses *selenium* to get an access token that requires a user's personal information (Spotify username & password).

## Spotify Web API

The Spotify Web API is very well documented. The following are links to the elements I used:

Anything regarding the API can be found <a href = "https://developer.spotify.com/documentation/web-api/"> here </a>. This page contains information on:

* Spotify Nomenclature
* Response Codes
* Examples

In order to be able to use the API, we must first tell Spotify that we have an app that wants to communicate with it.

### Registering an App

To register an app, we must first have a Spotify account. We then go to <a href = "https://developer.spotify.com/dashboard/"> Dashboard </a>. This takes us to the following page:

<p align="center">
  <img src = "https://github.com/alv31415/SpotifyAPI/blob/master/SAPI%20User%20Pictures/Screenshot%202020-09-04%20at%2015.28.25.png">
</p>

We then click on **Create an App**, and introduce the necessary information. We can edit this information later on. If we want to create a playlist, we must introduce a URI to get redirected to. This will be explained further on.

<p align="center">
  <img src = "https://github.com/alv31415/SpotifyAPI/blob/master/SAPI%20User%20Pictures/Screenshot%202020-09-04%20at%2015.29.35.png">
</p>

### API Functionality

Anything that we can do with the API can be found <a href = "https://developer.spotify.com/documentation/web-api/reference/"> here </a>. It contains the API endpoint references for any possible service, from working with tracks to searching for an artist. It tells us exactly how to make requests, and the format that these requests must have.

### Console

The Spotify Web API Console lets you explore the endpoints through an easy-to-use interface. You can access these <a href = "https://developer.spotify.com/console/"> here </a>. The endpoints is what the code (mainly) uses, but to gain an intutition, the console is a great resource, as it clearly shows you the parameters that a request needs, and returns a nicely formatted output.

### Authorisation

In order to request data from the API, we must request authorisation using the <a href = "https://developer.spotify.com/documentation/general/guides/authorization-guide/"> Authorization Guide </a>. There are 4 ways of requesting Authorisation (Authorisation Flows):

* **Refreshable user authorization:** Authorization Code Flow
* **Refreshable user authorization:** Authorization Code Flow With Proof Key for Code Exchange (PKCE)
* **Temporary user authorization:** Implicit Grant
* **Refreshable app authorization:** Client Credentials Flow 

If our authorisation request is successful, we obtain an access token that we can use to validate our requests to the web API.

### Basic Project Workflow

When making requests, there are 2 key aspects:

* **Header:** Used to contain the credentials required to execute the request. To get a token this authorization is comprised of client credentials (*client id* and *client secret*) obtained when registering an app. These credentials are provided using a base 64 String: `Authorization: Basic <base64 encoded client_id:client_secret>`. For endpoint requests, the header contains the token used for the request, and for some cases, additional information is passed under the key *"Content Type"*. For example, when working with playlists, a typical header is of the form `{Authorization : Bearer <token>, Content-Type : application/json}`.

* **Request Body:** Used to pass parameters required for certain endpoints. For example, according to documentation, to add songs to a playlist, there are 2 optional parameters: a list of uris of the songs, and a position argument. In such a case, the request body would be of the form: `{"uris": <list of uris>, "position": <position number>}`. If optional arguments are not passed, a certain default is used

## Search Client

The Search Client uses the <a href = "https://developer.spotify.com/documentation/web-api/reference/search/search/"> Search Endpoint </a>, described as:
 
 *"Get Spotify Catalog information about albums, artists, playlists, tracks, shows or episodes that match a keyword string."*
 
 the <a href = "https://developer.spotify.com/documentation/web-api/reference/albums/"> Album Endpoint </a>, described as:
 
 *"Endpoints for retrieving information about one or more artists from the Spotify catalog."*
 
 and the <a href = "https://developer.spotify.com/documentation/web-api/reference/artists/"> Artist Endpoint </a>, described as:
 
 *"Endpoints for retrieving information about one or more albums from the Spotify catalog."*
 
 ### Requesting Auth and Obtaining a Token
 
 The Search Client contains the main functionality for requesting authorisation using the **Client Credentials Flow**, via the methods `credentials_to_base64`. `get_token_header`, `get_auth`:
 
 * `credentials_to_base64`: creates a base 64 string from client credentials
 * `get_token_header`: creates the header used when requesting the token
 * `get_auth`: requests the authorisation, receiving a token if succesful. Sets this token as the access token of the class. The method `get_access_token` is used to return this token, and contains logic to ensure that, if the token has expired, a new authorisation request is made
 
 The four methods outlined above are then used and adapted across the other clients, faciliating the token retrieval process.
 
 ### Making a Search
 
 A Spotify search through the API relies on 2 methods: `simple_search` and `search`. `search` is used to format the search parameters, whilst `simple_search` contains the functionality to make the search request.
 
In `search` we define what we want to search for (*album , artist, playlist, track, show and episode*), what type of results we want and the number of results to return. For example:

```
search(search_parameters = {"artist" : "Avicii", "album" : "True"}, "content_type" = "track", "limit" = 10)
```

The following will return 10 tracks from the album *True* by *Avicii*. (Notice that *search_parameters* must be a dictionary)

We can add an *operator* and an *operator query* to reduce the search results that are returned. For example:

```
search(search_parameters = {"track" : "Time"}, "operator" : "NOT", "operator_type  : "billie eilish", "content_type" = "track", "limit" = 10)
```

The following will return 10 tracks whose name contains *Time*, but not including those by Billie Eilish.

 
 ### Obtaining a Resource
 
A resource refers to either an album or an artist. To obtain a resource, we require the resource's ID (this can be obtained from the resource's URI). To obtain a resource, we rely on the `get_resource` method. This method takes 4 arguments:

* **id:** the id of the resource (can be found in the resource's URI)
* **resource_type:** used to determine the type of resource that is returned. Can be either *artist* or *album*. If neither String is provided, *artist* is the default
* **keyword:** a keyword restricting what is returned. For example, when looking for an *album* resource, we can either get the album itself (*keyword = "none"*) or its tracks (*keyword = "tracks"*) (or any album, if no album id is provided). When looking for an *artist* resource, we can either get the artist itself (*keyword = "none"*), its albums (*keyword = "albums"*), its top tracks (*keyword = "top-tracks"*) (depending on a country), or related artists (*keyword = "related-artists"*) (or any artist, if no artist id is provided). 
* **country:** a country used when retrieving an artist's top tracks. US is the default value.

These arguments are used when creating the request URL. Using *id*, we use the helper methods `get_albums_url` or `get_artists_url` to retrieve the appropiate URL, which is then used in the request.

For example,

```
eminem_id = "7dGJo4pcD2V6oG8kP0tJRR"
get_resource(id = eminem_id, resource_type = "artist", keyword = "top-tracks", country = "HUN")
```

Returns the top tracks from *Eminem* in *Hungary*.

```
eminem_album_id = "4otkd9As6YaxxEkIjXPiZ6"
get_resource(id = eminem_album_id, resource_type = "album", keyword = "tracks")
```

Returns tracks from the album *Music To Be Murdered By*

### Printing Methods

I provided a variety of methods that can be used to pretty print the (in my opinion) the most relevant information that is obtained from the requests. The printing methods are:

* `print_search_results`
* `print_artist`
* `print_album` (uses `from_ms` and `print_tracks` as a helper methods)
* `print_top_tracks` (uses `from_ms` as a helper method)

## Playlist Client

The Playlist Client uses the <a href = "https://developer.spotify.com/documentation/web-api/reference/playlists/"> Playlist Endpoint </a>, described as:
 
 *"Endpoints for retrieving information about a user’s playlists and for managing a user’s playlists."*
 
### Requesting Auth and Obtaining a Token
  
The Playlist Client can obtain a token in 2 ways, depending on the functionality that is required.

If we want to work with a general playlist (that is, getting a playlist or its tracks), the authorisation and token request functionality is implemented via the method `get_access_token`. This method uses the Search Client to obtain the token, and contains logic to handle token expiration and saving.

Alternatively, if we want to create and modify a playlist, we use the method `get_token`. This method will take personal information as arguments (Spotify username and password). It uses the `navigator.py` file to create and retrieve a valid token from the <a href = "https://developer.spotify.com/console/post-playlists/"> Create Playlist Console></a>. It also contains the logic used to handle token expiration and saving. Further details on how `navigator.py` works is provided in the section **Navigator**.
 
### Accessing Playlist Information

There are 3 methods that can be used to obtain information that is public from playlists:

* `get_playlist`: given a `playlist_id`, returns the playlist associated with the id. Accepts parameters for `market`, as often Spotify has several instances of a track in its catalogue, each available in a different set of markets. 

* `get_playlist_tracks`: given a `playlist_id`, returns the tracks from a playlist associated with the id. Accepts parameters for `market`, as often Spotify has several instances of a track in its catalogue, each available in a different set of marketsg. Accepts parameters for `limit`, which indicates the number of tracks to be returned. 1 is the minimum. 100 is a maximum and default.

* `get_playlist_id`: given a `playlist_name`, uses the Search Client to return the search for a playlist by name, and returns the id of the top result.

For further (potential) functionality, check <a href = "https://developer.spotify.com/documentation/web-api/reference/playlists/get-playlist/"> Get a Playlist </a> and <a href = "https://developer.spotify.com/documentation/web-api/reference/playlists/get-playlists-tracks/"> Get a Playlist's Items </a>.

### Creating and Modifying a Playlist

There are 3 methods that can be used to create and modify information from a playlist:

* `create_playlist`: given personal information from a user (`user_id` & `password`) creates a playlist in the user's account. The "specifications" of the playlist can be defined within the method's parameters:
    * `playlist_name`: the desired name for our playlist.
    * `public`: a boolean String. *"false"* if you want the playlist to be private.
    * `collaborative`: a boolean String. *"false"* if you want the playlist to not be collaborative.
    * `description`: the description for the playlist.

  Uses a helper method (`check_boolean_value`) to ensure that `public` and `collaborative` only receive *"true"* or *"false"* as arguemnts. Otherwise, returns       *"false"* as a default.
  
  This method returns the id of the playlist that was created.
    
* `add_tracks_to_playlist`: given personal information from a user (`user_id` & `password`), a `playlist_id` and a list of songs/episodes (`tracks`), adds the songs to the playlist with the given id.

* `remove_tracks_from_playlist`: given personal information from a user (`user_id` & `password`), a `playlist_id` and a list of songs/episodes (`remove_tracks`), removes the songs from the playlist with the given id.

It is important to note that these methods all have an argument `walkthrough_mode`, which is required for `navigator.py`. The default (and recommended) value is *False*, as it makes the whole process much faster.

For example,

```
my_new_playlist_id = create_playlist(user_id = "myusername", password = "mypassword", walkthrough_mode=False, playlist_name="My Favourite Songs",
                        public="false", collaborative="true", description="A playlist containing my favourite tracks!")     
```

creates a private, collaborative playlist called *"My Favourite Songs"* with description *"A playlist containing my favourite tracks!"* and id `my_new_playlist_id`

We can then add songs to this playlist:

```
my_songs = ["till' i collapse", "Leaving Heaven", "White America", "Without Me"]
add_tracks_to_playlist(user_id = "myusername", password = "mypassword, playlist_id = my_new_playlist_id, tracks = my_songs, walkthrough_mode=False)
```

or remove them:

```
no_longer_my_favourites = ["Leaving Heaven", "White America", "Without Me"]
remove_tracks_from_playlist(user_id = "myusername", password = "mypassword, playlist_id = my_new_playlist_id, remove_tracks = no_longer_my_favourites, walkthrough_mode=False)
```

## Browse Client

The Browse Client uses the <a href = "https://developer.spotify.com/documentation/web-api/reference/browse/"> Browse Endpoint </a>, described as:
 
 *"Endpoints for getting playlists and new album releases featured on Spotify’s Browse tab."*
 
The Browse Tab is:

<p align = "center">
  <img src = "https://github.com/alv31415/SpotifyAPI/blob/master/SAPI%20User%20Pictures/Screenshot%202020-09-08%20at%2012.35.59.png">
</p>

### Requesting Auth and Obtaining a Token

For the Browse Client, the authorisation and token request functionality is implemented via the method `get_access_token`. This method uses the Search Client to obtain the token, and contains logic to handle token expiration and saving.

### Query URLs

To make request to the browse endpoints, we need to create queries for our request URLs (much like in the Search Client). In order to do this, we use 2 methods:

* `get_request_url_dict`: creates and returns a dictionary, in which the keys are the query, and the values are the query values. Different endpoints require different URLs, and this method manages this. The arguments it takes are:
    * `category_query`: used to fiter out the arguments that certain queries don't need. For example, to get a category's playlist, we require a `country` and a `limit`but to get a category, we require a `country` and a `locale`, but no `limit`. Valid `category_query` arguments are:
        * `get_ids`
        * `get_category`
        * `get_category_playlist`
        * `get_releases`
    * `country`: a country, shown as a ISO 3166-1 alpha-2 country code. No value corresponds to a globally relevant query search.
    * `locale`: the desired language result, consisting of an ISO 639-1 language code and an ISO 3166-1 alpha-2 country code,
        joined by an underscore (i.e "es_MX" refers to Spanish music fromm mexico).
    * `limit`: the maximum number of results that ought to be returned
* `get_request_url`: uses `urllib` to parse the dictionary obtained from `get_request_url_dict` into a URL query. Returns this URL.

### Working with Categories and New Releases

We use `get_reqeust_url` to create a URL used in requests fro the following methods for extracting browse data:

* `get_category_ids`: returns the category ids from the browse tabs. These IDs are used in the following methods when working with a specific category.
* `get_category`: given a `category_id`, returns the category. The category returned depends on a `country` and a `locale`.
* `get_category_playlists`: given a `category_id`, returns the playlists from the corresponding category. The playlists returned depend on a `country` and a `limit`.
* `get_playlist_from_category`: given a `category_id` and a `playlst_name`, returns the playlist with the given name from the corresponding category. The playlist returned depend on a `country`. If the playlist with the given name is not found, a Value Error is raised.
* `get_new_releases`: given a `country` returns the new releases from said country. Number of results depends on `limit`

For example,

```
get_category(category_id = "pop", country = "GB", locale = "en_GB")
```

Returns the category *"Pop"* from the UK (English Language).

```
get_category(category_id = "toplists", country = "BR", limit = "12")
```

Returns 12 playlists the category *"Top Lists"* from Brazil.

```
get_playlist_from_category(playlist_name = "Global Top 50", category_id = "toplists", country = "US")
```

Returns the playlist *"Global Top 50"* from the category *"Top Lists"* from the US.


```
get_new_releases(country = "SE", limit = 15)
```

Returns 15 new releases traacks from Sweden.

### Printing Methods

Printing functionality has been provided to pretty print the results of the Browse Client:

* `print_category_ids`
* `print_category_playlists`
* `print_new_releases`

## Navigator

**navigator.py** uses *selenium* to obtain a token from Spotify, by logging in as a user. It contains 3 methods:

* `spotify_login`: logs in to the user's Spotify account, witht the provided user information.
* `driver_scroll`: used to scroll down a page to access all the necessary elements.
* `extract_token`: used to request authorisation and obtain the token.

All of the methods contain a boolean argument, `walkthrough_mode`. If set to *True*, you, as a user, will see the whole token obtining process. Using the **time** module, this allows for the user to check that everything is correct. If set to *False*, the whole process is done in the background, and the user only sees the returned token.

