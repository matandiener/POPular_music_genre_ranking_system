# Class that will hold all of the data that comes from the crawling services and be used
# in the ranking algorithm (each service will update the class with more relevant data)


class RankingData(object):
    def __init__(self):
        self.billboard_data = {}
        self.youtube_data = {}

    def __str__(self):
        return "From Billboard: {0}\n" \
               "From Youtube: {1}".format(self.billboard_data, self.youtube_data)


