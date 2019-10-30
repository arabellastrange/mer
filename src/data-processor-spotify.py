import spotipy
import spotipy.util as util

# authenticate app
username = "angelaodinsdotir"
scope = 'user-library-read'
token = util.prompt_for_user_token(username, scope, client_id='bcc543d6f5564761ac2548ded2bdd20d',
                                   client_secret='6422b1e96ecf4c99a27d8c364560eb14',
                                   redirect_uri='http://localhost/')
spotify = spotipy.Spotify(auth=token)


def get_artists():
    if token:
        results = spotify.current_user_saved_tracks()
        for item in results['items']:
            track = item['track']
            print(track['name'] + ' - ' + track['artists'][0]['name'])
    else:
        print("Can't get token for", username)


def main():
    get_artists()


if __name__ == '__main__':
    main()