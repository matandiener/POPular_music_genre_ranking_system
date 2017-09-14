from RankingData import RankingData
from youtube_data.youtube_extractor import YoutubeExtractor, HttpError
from billboard_data.BillboardExtractor import BillboardParseException, get_all_charts_songs, RELEVANT_CHARTS_NAMES


# Class that will call all of the project crawling services and will pass the
# result to the ranking algorithm using the RankingData object
class CrawlingManager(object):
    def __init__(self):
        self.ranking_data = RankingData()

    def crawl(self):
        # Get data from Billboard
        self.ranking_data.billboard_data = get_all_charts_songs(RELEVANT_CHARTS_NAMES)

        # Get data from youtube
        for chart_name in self.ranking_data.billboard_data:
            for song in self.ranking_data.billboard_data[chart_name]:
                self.ranking_data.youtube_data[song] = []
        try:
            # The extractor updates the youtube_data
            YoutubeExtractor().extract_info_on_all_videos(self.ranking_data.youtube_data)
        except HttpError as ex:
            "Network error when connecting to youtube\ndetails: {0}\n" \
             "skipping on youtube extraction".format(e)

        # Call the ranking algorithm with ranking_data
        # Save the results to the DB to be viewed in the website


if __name__ == "__main__":
    try:
        crawler = CrawlingManager()
        crawler.crawl()
        print crawler.ranking_data
    except Exception as e:
        print "Program failed for unknown reason, details: {0}".format(e)
