from datetime import datetime
from isodate import parse_duration


class VideoInfo(object):
    def __init__(self, **kargs):
        if "id" in kargs:
            self.id = kargs["id"]
        else:
            self.id = None

        if "snippet" in kargs:
            self.title = kargs["snippet"]["title"] if "title" in kargs["snippet"] else None
            self.description = kargs["snippet"]["description"] if "description" in kargs["snippet"] else None
            self.publish_date = datetime.strptime(kargs["snippet"]["publishedAt"], "%Y-%m-%dT%H:%M:%S.%fZ") \
                if "publishedAt" in kargs["snippet"] else None
        else:
            self.title = None
            self.description = None
            self.publish_date = None

        if "contentDetails" in kargs:
            # In Seconds
            self.duration = parse_duration(kargs["contentDetails"]["duration"]).seconds \
                if "duration" in kargs["contentDetails"] else None
        else:
            self.duration = None

        if "statistics" in kargs:
            self.view_count = int(kargs["statistics"]["viewCount"]) if "viewCount" in kargs["statistics"] else None
            self.like_count = int(kargs["statistics"]["likeCount"]) if "likeCount" in kargs["statistics"] else None
            self.dislike_count = int(kargs["statistics"]["dislikeCount"]) if "dislikeCount" in kargs["statistics"] else None
            self.comment_count = int(kargs["statistics"]["commentCount"]) if "commentCount" in kargs["statistics"] else None
        else:
            self.view_count = None
            self.like_count = None
            self.dislike_count = None
            self.comment_count = None

    def __str__(self):
        return "{0!r} with id {1} published at {2} with duration of {3}".format(self.title, self.id,
                                                                                self.publish_date, self.duration) \
                if self.title is not None and \
                self.id is not None and \
                self.publish_date is not None and \
                self.duration is not None \
                else "bad youtube result, to ignore"

    def __repr__(self):
        return self.__str__()
