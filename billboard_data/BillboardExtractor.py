from billboard import ChartData, BillboardParseException

RELEVANT_CHARTS_NAMES = ["billboard-200", "hot-100"]


def get_chart_songs(chart_name):
    chart_songs_by_title = {}

    chart = ChartData(chart_name)
    for song in chart:
        key = "{0} {1}".format(song.title, song.artist)
        chart_songs_by_title[key] = song

    return chart_songs_by_title


def get_all_charts_songs(requested_charts):
    charts_songs_by_chart_name = {}

    for chart_name in requested_charts:
        try:
            charts_songs_by_chart_name[chart_name] = get_chart_songs(chart_name)
        except BillboardParseException as e:
            print "Failed to fetch data from Billboard about {0}\n" \
                  "reason: {1}\n" \
                  "skipping this chart name".format(chart_name, e)

    return charts_songs_by_chart_name


if __name__ == "__main__":
    print get_all_charts_songs(RELEVANT_CHARTS_NAMES)
