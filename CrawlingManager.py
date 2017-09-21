import logging
from datetime import datetime

from RankingData import RankingData, YOUTUBE_KEY, BILLBOARD_KEY
from youtube_data.youtube_extractor import YoutubeExtractor, HttpError
from billboard_data.BillboardExtractor import BillboardParseException, get_all_charts_items,\
    RELEVANT_SONGS_CHARTS_NAMES, RELEVANT_ALBUMS_CHARTS_NAMES


# Class that will call all of the project crawling services and will pass the
# result to the ranking algorithm using the RankingData object
class CrawlingManager(object):
    def __init__(self):
        self.ranking_data = RankingData()

    def crawl(self):
        logging.info("Start the crawling logic")

        # Get data from Billboard
        billboard_songs_data = get_all_charts_items(RELEVANT_SONGS_CHARTS_NAMES)
        billboard_albums_data = get_all_charts_items(RELEVANT_ALBUMS_CHARTS_NAMES)

        # Prepare to get data from youtube
        for chart_name in billboard_songs_data:
            for song, data in billboard_songs_data[chart_name].items():
                self.ranking_data.songs[song] = {BILLBOARD_KEY: data,
                                                 YOUTUBE_KEY: {}}
        for chart_name in billboard_albums_data:
            for album, data in billboard_albums_data[chart_name].items():
                self.ranking_data.albums[album] = {BILLBOARD_KEY: data,
                                                   YOUTUBE_KEY: {}}

        try:
            # The extractor updates the youtube_data
            youtube_extractor = YoutubeExtractor()
            youtube_extractor.extract_info_on_all_videos(self.ranking_data.songs)
            youtube_extractor.extract_info_on_all_videos(self.ranking_data.albums)
        except HttpError as ex:
            logging.error("Network error when connecting to youtube\ndetails: {0}\n"
                          "skipping on youtube extraction".format(e))

        # Call the ranking algorithm with ranking_data (should handle both songs and albums)
        logging.info("Rank all of the songs and albums according to our algorithm")

        # Save the results to the DB to be viewed in the website

        logging.info("Crawling script finished")


if __name__ == "__main__":
    try:
        logging.basicConfig(filename=r'logs\\popular_{0}.log'.format(datetime.strftime(datetime.now(),
                                                                                       "%Y_%m_%dT%H_%M_%S")),
                            level=logging.DEBUG,
                            format="%(asctime)s - %(module)s -"
                                   " %(levelname)s - %(message)s")
        crawler = CrawlingManager()
        crawler.crawl()
        print crawler.ranking_data
    except Exception as e:
        print "Program failed for unknown reason, details: {0}".format(e)
