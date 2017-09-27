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

    norm_views = 0
    norm_like_and_dislike = 0
    norm_comments = 0
    if total_views >= 1000000000:
        norm_views = total_views / 10000000.0
        norm_like_and_dislike = total_like_and_dislikes / 100000.0
        norm_comments = total_comments / 10000.0
    elif 100000000 <= total_views < 1000000000:
        norm_views = total_views / 1000000.0
        norm_like_and_dislike = total_like_and_dislikes / 10000.0
        norm_comments = total_comments / 1000.0
    elif 10000000 <= total_views < 100000000:
        norm_views = total_views / 100000.0
        norm_like_and_dislike = total_like_and_dislikes / 1000.0
        norm_comments = total_comments / 100.0
    elif 1000000 <= total_views < 10000000:
        norm_views = total_views / 10000.0
        norm_like_and_dislike = total_like_and_dislikes / 100.0
        norm_comments = total_comments / 10.0
    elif total_views <= 1000000:
        norm_views = total_views / 1000.0
        norm_like_and_dislike = total_like_and_dislikes / 10.0
        norm_comments = total_comments

    alpha = 0.6
    beta = 0.3
    gama = 0.1

    return alpha*norm_views + beta*norm_like_and_dislike + gama*norm_comments
