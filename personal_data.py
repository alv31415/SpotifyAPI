
# Info from # https://developer.spotify.com/documentation/web-api/reference/

class PersonalData:

    def __init__(self, client_id, client_secret, user_id, password):

        """
        Optional Method to initialise personal information to use the Spotify clients
        Might be used if we want to keep all the data "in one place"
        If we want to use all the clients (for searching, browsing and working with playlists),
        it is recommended to initialise this class, and use its properties to initialise the corresponding classes
        client_id: client id. Provided by Spotify when we register the app.
        client_secret: client secret. Provided by Spotify when we register the app.
        user_id: your username. Used to create playlists.
        password: the password linked to your username
        """

        self.client_id = client_id
        self.client_secret = client_secret
        self.user_id = user_id
        self.password = password


