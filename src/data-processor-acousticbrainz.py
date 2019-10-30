import pandas as pd
import requests

# the song Bohemian Rhapsody by Queen has a MBID of: b1a9c0e9-d987-4042-ae91-78d6a3267d69
response = requests.get("https://acousticbrainz.org/b1a9c0e9-d987-4042-ae91-78d6a3267d69/high-level")

if response.status_code != 200:
    # This means something went wrong.
    print('GET /api/mbid/high-level/ {}'.format(response.status_code))

print(response.json())
