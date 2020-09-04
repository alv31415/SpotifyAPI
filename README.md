# SpotifyAPI
Python project to work with the Spotify Web API. My first serious, independent Python project, and my first time working with APIs.

## Project Structure

This project contains 4 files. 3 represent Spotify Clients, used to communicate with the Spotify Web API. 
These are:

* **spotify_search_client.py:** used to access Spotify Search Functionality. This can be used to get and print information on artists, albums, playlists, tracks, etc ...

* **spotify_playlist_client.py:** used to create, modify and acess playlists & their tracks. For creating and modifying playlists, user credentials must be included.

* **spotify_browse_client.py:** used to access the Spotify Browse Tab. This can be used to access the different categories from Spotify (i.e "mood", "summer", etc ...) and new releases.

The last one (**navigator.py**), uses *selenium* to get an access token that requires a user's personal information (Spotify username & password).

### Basic Project Functionality

## Spotify Web API

The Spotify Web API is very well documented. The following are links to the elements I used:

Anything regarding the API can be found <a href = "https://developer.spotify.com/documentation/web-api/"> here </a>. This page contains information on:

* Spotify Nomenclature
* Response Codes
* Examples

In order to be able to use the API, we must first tell Spotify that we have an app that wants to communicate with it.

### Registering an App

To register an app, we must first have a Spotify account. We then go to <a href = "https://developer.spotify.com/dashboard/"> Dashboard </a>. This takes us to the following page:


We then click on **Create an App**, and introduce the necessary information. We can edit this information later on. If we want to create a playlist, we must introduce a URI to get redirected to. This will be explained further on.

### API Functionality

Anything that we can do with the API can be found <a href = "https://developer.spotify.com/documentation/web-api/reference/"> here </a>. It contains the API endpoint references for any possible service, from working with tracks to searching for an artist. It tells us exactly how to make requests, and the format that these requests must have.

### Console

The Spotify Web API Console lets you explore the endpoints through an easy-to-use interface. You can access these <a href = "https://developer.spotify.com/console/"> here </a>. The endpoints is what the code (mainly) uses, but to gain an intutition, the console is a great resource, as it clearly shows you the parameters that a request needs, and returns a nicely formatted output.

## Search Client

The Search Client uses the <a href = "https://developer.spotify.com/documentation/web-api/reference/playlists/"> Playlist Endpoint </a>, described as:
 
 *"Endpoints for retrieving information about a user’s playlists and for managing a user’s playlists."*

## Playlist Client


## Browse Client


## Navigator
