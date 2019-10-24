import tensorflow as tf
import spotipy
import spotipy.util as util

# authenticate app
username = ""
scope = 'user-library-read'

util.prompt_for_user_token(username, scope, client_id='your-app-redirect-url',
                           client_secret='your-app-redirect-url',
                           redirect_uri='your-app-redirect-url')
