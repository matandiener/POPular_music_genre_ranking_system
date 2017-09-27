import logging
from datetime import datetime
import os
import django
from django.db import transaction
from django.utils import timezone

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "popular.settings")
django.setup()

from ranking.models import Ranks
from RankingData import RankingData, YOUTUBE_KEY, BILLBOARD_KEY
from youtube_data.youtube_extractor import YoutubeExtractor, HttpError
from billboard_data.BillboardExtractor import BillboardParseException, get_all_charts_items,\
    RELEVANT_SONGS_CHARTS_NAMES
from ranking_algorithm.ranking_algorithm import rank_songs, POPULAR_RANK_KEY


# Class that will call all of the project crawling services and will pass the
# result to the ranking algorithm using the RankingData object
class CrawlingManager(object):
    SONGS_TYPE = "songs"

    def __init__(self):
        self.ranking_data = RankingData()

    def crawl(self):
        logging.info("Start the crawling logic")

        # Get data from Billboard
        billboard_songs_data = get_all_charts_items(RELEVANT_SONGS_CHARTS_NAMES)

        # Prepare to get data from youtube
        self.prepare_data_for_extraction(billboard_songs_data, CrawlingManager.SONGS_TYPE)

        try:
            # The extractor updates the youtube_data
            youtube_extractor = YoutubeExtractor()
            youtube_extractor.extract_info_on_all_videos(self.ranking_data.songs)
        except HttpError as ex:
            logging.error("Network error when connecting to youtube\ndetails: {0}\n"
                          "skipping on youtube extraction".format(e))

        # Call the ranking algorithm with ranking_data (should handle both songs and albums)
        logging.info("Rank all of the songs according to our algorithm")
        rank_songs(self.ranking_data.songs)

        # Save the results to the DB to be viewed in the website later
        self.save_results()

        logging.info("Crawling script finished")

    def prepare_data_for_extraction(self, billboard_data, data_type):
        """
        Use the data extracted from billboard as a starting point to create the generic dict
        that will save all of the extracted data on the songs and albums using the billboard data
        and the service name as keys
        :param billboard_data: the data extracted from billboard
        :param data_type: the type of the data (songs, albums etc...)
        """
        for chart_name in billboard_data:
            for key, data in billboard_data[chart_name].items():
                getattr(self.ranking_data, data_type)[key] = {BILLBOARD_KEY: data,
                                                              YOUTUBE_KEY: {}}

    @transaction.atomic
    def save_results(self):
        logging.info("Replacing the old results from the DB with the new calculated results")

        # Empty the DB from old results
        Ranks.objects.all().delete()

        for song, services in self.ranking_data.songs.items():
            Ranks.objects.create(title=self.ranking_data.songs[song][BILLBOARD_KEY].title,
                                 artist=self.ranking_data.songs[song][BILLBOARD_KEY].artist,
                                 ranking_creation_date=timezone.now(),
                                 rank=self.ranking_data.songs[song][POPULAR_RANK_KEY])

        logging.info("Finished saving the results to the DB")


if __name__ == "__main__":
    logging.basicConfig(filename=r'logs\\popular_{0}.log'.format(datetime.strftime(datetime.now(),
                                                                                   "%Y_%m_%dT%H_%M_%S")),
                        level=logging.DEBUG,
                        format="%(asctime)s - %(module)s -"
                               " %(levelname)s - %(message)s")

    try:
        crawler = CrawlingManager()
        crawler.crawl()
        # print crawler.ranking_data
    except Exception as e:
        logging.error("Program failed for unknown reason, details: {0}".format(e))
