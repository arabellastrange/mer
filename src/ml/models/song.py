class Song:
    artist = ''
    title = ''
    id = ''
    tags = []

    def __init__(self, artist, title, id, tags):
        self.artist = artist
        self.title = title
        self.id = id
        self.tags = tags
