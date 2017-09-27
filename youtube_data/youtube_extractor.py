import httplib2
import sys
import logging

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

from VideoInfo import VideoInfo
from RankingData import YOUTUBE_KEY

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret.
CLIENT_SECRETS_FILE = "client_secret.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
YOUTUBE_READ_WRITE_SSL_SCOPE = "https://www.googleapis.com/auth/youtube.readonly"
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

STORAGE_PATH_FORMAT = "{0}-oauth2.json"
# This variable defines a message to display if the CLIENT_SECRETS_FILE is
# missing.
MISSING_CLIENT_SECRETS_MESSAGE = "WARNING: Please configure OAuth 2.0"

SEARCH_PART = "id"
SEARCH_FIELDS = "items(id(videoId))"
SEARCH_TYPE = "video"
SEARCH_MAX_RESULTS = 5
VIDEOS_PART = "id, snippet, contentDetails, statistics"
VIDEOS_FIELDS = "items(id, snippet(publishedAt, title, description)," \
                      "contentDetails(duration)," \
                      "statistics(viewCount, likeCount, dislikeCount, commentCount))"


class YoutubeExtractor(object):
    def __init__(self):
        self.service = YoutubeExtractor.get_authenticated_service()

    @staticmethod
    # Authorize the request and store authorization credentials.
    def get_authenticated_service():
        flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=YOUTUBE_READ_WRITE_SSL_SCOPE,
                                       message=MISSING_CLIENT_SECRETS_MESSAGE)

        storage = Storage(STORAGE_PATH_FORMAT.format(sys.argv[0]))
        credentials = storage.get()

        if credentials is None or credentials.invalid:
            credentials = run_flow(flow, storage)

        # Trusted testers can download this discovery document from the developers page
        # and it should be in the same directory with the code.
        return build(API_SERVICE_NAME, API_VERSION,
                     http=credentials.authorize(httplib2.Http()))

    def youtube_search(self, search_term):
        # Call the search.list method to retrieve results matching the specified
        # query term.
        search_response = self.service.search().list(
            q=search_term,
            type=SEARCH_TYPE,
            part=SEARCH_PART,
            fields=SEARCH_FIELDS,
            maxResults=SEARCH_MAX_RESULTS
        ).execute()

        search_videos = []

        # Add each result to the appropriate list, and then display the list of
        # matching videos.
        for search_result in search_response.get("items", []):
            search_videos.append(search_result["id"]["videoId"])
        video_ids = ",".join(search_videos)

        return video_ids

    def get_videos_information(self, video_ids):
        video_response = self.service.videos().list(
            id=video_ids,
            part=VIDEOS_PART,
            fields=VIDEOS_FIELDS
        ).execute()

        videos = []

        # Add each result to the list, and then display the list of matching videos.
        for video_result in video_response.get("items", []):
            videos.append(VideoInfo(**video_result))

        return videos

    def extract_info_on_video(self, search_term):
        relevant_video_ids = self.youtube_search(search_term)

        return self.get_videos_information(relevant_video_ids)

    def extract_info_on_all_videos(self, videos_records):
        """
        :param videos_records: dict that contains the songs or albums to search in youtube
                               the results will be stored in the given dict under the search term key and
                               will be saved under the youtube key (so that other services can store their info
                               on this songs under a different key)
        """
        logging.info("Getting the data from youtube")
        for vid_name in videos_records:
            # Extract videos related to this search term
            videos_records[vid_name][YOUTUBE_KEY] = self.extract_info_on_video(vid_name)

if __name__ == "__main__":
    # Running example
    videos_obj = {"lady gaga bad romance": {},
                  "LP lost on you": {},
                  "queen don't stop me now": {}
                  }
    try:
        YoutubeExtractor().extract_info_on_all_videos(videos_obj)

        for vid_list in videos_obj.values():
            for vid in vid_list[YOUTUBE_KEY]:
                print vid
            print "###################"

    except HttpError as e:
        print "An HTTP error {0} occurred:\n{1}".format(e.resp.status, e.content)