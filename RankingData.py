# Class that will hold all of the data that comes from the crawling services and be used
# in the ranking algorithm (each service will update the class with more relevant data)
BILLBOARD_KEY = "billboard"
YOUTUBE_KEY = "youtube"


class RankingData(object):
    """
    songs = dict that contains the songs search in all of the crawling services
                               the results will be stored in the given dict under the song key and for each
                               different service relevant data will be saved under the service key.
                               e.g songs = {"bad romance lady gaga": {"billboard": billboard_song_data,
                                                                     "youtube": youtube_song_data,}, }
    """

    def __init__(self):
        self.songs = {}

    def __str__(self):
        return "Songs data: {0}\n".format(self.songs)


