import requests
import socket
import json
import base64
import random

# Spotify API: https://api.spotify.com
# I ended up using only post_auth() and spotify_init() because the other authetication methods required more overhead

def post_auth():
    #This function uses the Client Credentials Flow on Spotify API which allows you
    #to access publicly available information, but not user specific stuff (which is 
    #a shame). I'm using it here because I don't want to deploy a localhost.

    #spotify api requires you to create an app on spotify developer and send a post request
    #using the client id and client secret that is provided to you.
    client_id = 'e7efe30cb6ab46c8a85bed9ff5ef5cae'
    client_secret = 'df75e915e70d4863aa852d4c92be7b54'
    credentials = f"{client_id}:{client_secret}"

    data = {
        'grant_type': "client_credentials",
    }

    headers = {
        #The Authorization key format that Spotify requires is the base64 encoding of the credentials.
        #I used fstrings here but there are other ways to do this as well
        'Authorization': f"Basic {base64.b64encode(credentials.encode()).decode()}",
        'Content-Type': "application/x-www-form-urlencoded"
    }
    postreq = requests.post("https://accounts.spotify.com/api/token",
                            data=data, headers=headers)

    response_data = postreq.json()

    #get access token information (expires in 3600s/1hr)
    # print(json.dumps(response_data, indent=4))

    access_token = response_data["access_token"]
    token_type = response_data["token_type"]

    return (token_type, access_token)

def get_auth():
    # This function uses the default authentication method that the Spotify API uses
    # for web applications. It needs a functional redirect_uri so that we can retrieve
    # requests from a localhost development server, which is not my goal right now;
    # i just want a functional project so we're using post_auth.
    headers = {
    }
    params = {
        'client_id': 'e7efe30cb6ab46c8a85bed9ff5ef5cae',
        'response_type': 'code',
        'redirect_uri': 'http://localhost:3000',
        'scope': 'user-read-private user-read-email'

    }

    response = requests.get('https://accounts.spotify.com/authorize?',
                            headers = headers, params = params)

    if response.status_code==200:
        print(type(response))

        return None
    else:
        print('error: got response code %d' % response.status_code)
        print(response.text)
        return None

def get_userID(auth_string):
    # In order to get user ID I need higher OAuth, so I will not be using this.
    # I'm still going to keep the function though because I want to continue
    # looking at this later.
    headers = {
        #getting current user's ID from spotifyAPI so I can access 
        'Authorization': auth_string,
    }

    params = {
        'id': '11dFghVXANMlKmJXsNCbNl',
    }

    response = requests.get('https://api.spotify.com/v1/me/', 
                            params = params, headers = headers)

    if response.status_code == 200:
        user_info = response.json()

        print(json.dumps(user_info, indent = 4))
        quote = 'quote'
        return quote

    else:
        print('error: got response code %d' % response.status_code)
        print(response.text)
        return None

def spotify_init():

    retrieve_post = post_auth()
    auth_string = retrieve_post[0] + " " + retrieve_post[1]

    headers = {
        #SpotifyAPI requires Authorization from your app, which is generated from the post_auth()
        'Authorization': auth_string
    }

    params = {
        'playlist_id': '37i9dQZEVXbNG2KDcFcKOF',
        'market': 'ES',
        'limit': 50,
    }

    #I am going to get songs on the top global spotify playlist
    response = requests.get('https://api.spotify.com/v1/playlists/37i9dQZEVXbNG2KDcFcKOF/tracks',
                            params=params, headers=headers)

    if response.status_code == 200: # Status: OK
        playlist_info = response.json()
        rand_index = random.randrange(50)
        # print(json.dumps(playlist_info, sort_keys=False, indent=4))

        song_name = playlist_info["items"][rand_index]["track"]["name"]
        artist_names = []

        for i in range(0, len(playlist_info["items"][rand_index]["track"]["artists"])):
            artist_names.append(playlist_info["items"][rand_index]["track"]["artists"][i]["name"])

        song_text = "song: " + song_name + ", artists: "

        for i in range(0, len(spotify_output[1])):
            song_text = song_text + artist_names[i] + ", "
    
        song_text = song_text[0:len(song_text) - 2]

        return song_text

    else:
        print('error: got response code %d' % response.status_code)
        print(response.text)
        return None


SPOTIFY_APP = {
    'name': 'Find Top Songs',
    'init': spotify_init
}


if __name__ == '__main__':
    # retrieve_post = post_auth()

    # auth_string = retrieve_post[0] + " " + retrieve_post[1]

    spotify_output = spotify_init()

    # song_text = "song: " + spotify_output[0] + ", artists: "

    # for i in range(0, len(spotify_output[1])):
    #     song_text = song_text + spotify_output[1][i] + ", "
    
    # song_text = song_text[0:len(song_text) - 2]

    print(spotify_output)