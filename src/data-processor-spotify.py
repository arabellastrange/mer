import socketserver
from http.server import SimpleHTTPRequestHandler
import spotipy
import spotipy.util as util

# authenticate app
username = "angelaodinsdotir"
scope = 'user-library-read'


def run(port, handler):
    with socketserver.TCPServer(("", port), handler) as httpd:
        try:
            print("serving at port", port)
            httpd.serve_forever()
        finally:
            httpd.server_close()


def get_artists():
    token = util.prompt_for_user_token(username, scope, client_id='bcc543d6f5564761ac2548ded2bdd20d',
                                       client_secret='6422b1e96ecf4c99a27d8c364560eb14',
                                       redirect_uri='http://localhost:8888/callback')
    if token:
        sp = spotipy.Spotify(auth=token)
        results = sp.current_user_saved_tracks()
        for item in results['items']:
            track = item['track']
            print(track['name'] + ' - ' + track['artists'][0]['name'])
    else:
        print("Can't get token for", username)


def main():
    run(8888, SimpleHTTPRequestHandler)
    get_artists()


if __name__ == '__main__':
    main()

# save track information to a dataframe
