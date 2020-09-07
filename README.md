# SpotifyAPI
Python project to work with the Spotify Web API. My first serious, independent Python project, and my first time working with APIs.

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
 
 ### Request Auth & Obtaining a Token
 
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
* **keyword:** a keyword restricting what is returned. For example, when looking for an *album* resource, we can either get the album itself (*keyword = "none"*) or its tracks (*keyword = "tracks"*) (or any album, if no album id is provided). When looking for an *artist* resource, we can either get the artist itself (*keyword = "none"*), its albums (*keyword = "albums"*), its top tracks (*keyword = "top-tracks"*) (depending on a country), or related artists (*keyword = "related-artists"*) (or any artist, if no artist id is provided). For more information, these are the <a href = "https://developer.spotify.com/documentation/web-api/reference/albums/"> album endpoints </a> and the <a href = "https://developer.spotify.com/documentation/web-api/reference/artists/"> artist endpoints </a>.
* **country:** a country used when retirieving an artist's top tracks. US is the default value.

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

### Printing Information

I provided a variety of methods that can be used to pretty print the (in my opinion) the most relevant information that is obtained from the requests. The printing methods are:

* `print_search_results`
* `print_artist`
* `print_album` (uses `from_ms` and `print_tracks` as a helper methods)
* `print_top_tracks` (uses `from_ms` as a helper method)

## Playlist Client

The Playlist Client uses the <a href = "https://developer.spotify.com/documentation/web-api/reference/playlists/"> Playlist Endpoint </a>, described as:
 
 *"Endpoints for retrieving information about a user’s playlists and for managing a user’s playlists."*

## Browse Client


## Navigator
