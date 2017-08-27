# Sample Python code for user authorization

import httplib2
import os
import sys

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

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
SEARCH_FIELDS = "items(id)"
SEARCH_ORDER = "viewCount"
SEARCH_TYPE = "video"
SEARCH_MAX_RESULTS = 10
VIDEOS_PART = "snippet, status"
VIDEOS_FIELDS = "items(snippet, status)"


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
            part=SEARCH_PART,
            fields=SEARCH_FIELDS,
            maxResults=SEARCH_MAX_RESULTS,
            order=SEARCH_ORDER,
            type=SEARCH_TYPE
        ).execute()

        search_videos = []

        # Add each result to the appropriate list, and then display the list of
        # matching videos.
        for search_result in search_response.get("items", []):
            search_videos.append(search_result["id"]["videoId"])
        video_ids = ",".join(search_videos)

        video_response = self.service.videos().list(
            id=video_ids,
            part=VIDEOS_PART,
            fields=VIDEOS_FIELDS
        ).execute()

        videos = []

        # Add each result to the list, and then display the list of matching videos.
        for video_result in video_response.get("items", []):
            videos.append("%s" % (video_result["snippet"]["title"]))

        print "Videos:\n", "\n".join(videos), "\n"

if __name__ == "__main__":

    test_search_term = "Tushar Roy"

    try:
        YoutubeExtractor().youtube_search(test_search_term)
    except HttpError as e:
        print "An HTTP error {0} occurred:\n{1}".format(e.resp.status, e.content)