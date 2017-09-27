from RankingData import YOUTUBE_KEY, BILLBOARD_KEY

POPULAR_RANK_KEY = 'POPular_rank'


def rank_songs(songs):
    for song in songs:
        songs[song][POPULAR_RANK_KEY] = rank_song(songs[song][YOUTUBE_KEY])


def rank_song(song_data):
    total_views = 0
    total_like_and_dislikes = 0
    total_comments = 0
    for youtube_vid in song_data:
        total_views += youtube_vid.view_count if youtube_vid.view_count is not None else 0
        total_like_and_dislikes += youtube_vid.like_count if youtube_vid.like_count is not None else 0
        total_like_and_dislikes += youtube_vid.dislike_count if youtube_vid.dislike_count is not None else 0
        total_comments += youtube_vid.comment_count if youtube_vid.comment_count is not None else 0

    alpha = 0.6
    beta = 0.3
    gama = 0.1

    return alpha*total_views + beta*total_like_and_dislikes + gama*total_comments
