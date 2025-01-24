import googleapiclient.discovery

# YouTube Data API key
API_KEY = 'AIzaSyCXxwa709nJao-P8tbnkD_VlDPJ2qA2JOY'  # Replace with your YouTube Data API key

def get_youtube_service():
    """Builds the YouTube service object for API calls."""
    api_service_name = "youtube"
    api_version = "v3"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=API_KEY)
    return youtube

def search_youtube_videos(query, max_results=5):
    """
    Searches for YouTube videos based on a query and returns a list of video IDs.

    :param query: The search query string.
    :param max_results: The maximum number of results to return.
    :return: A list of video IDs.
    """
    youtube = get_youtube_service()
    search_response = youtube.search().list(
        q=query,
        part="id",
        type="video",
        maxResults=max_results
    ).execute()

    video_ids = [item['id']['videoId'] for item in search_response.get('items', [])]
    return video_ids

def get_video_details(video_id):
    """
    Retrieves detailed information for a specific YouTube video.

    :param video_id: The ID of the YouTube video.
    :return: A dictionary containing video details.
    """
    youtube = get_youtube_service()
    video_response = youtube.videos().list(
        part="snippet,statistics",
        id=video_id
    ).execute()

    if not video_response['items']:
        return None

    video = video_response['items'][0]
    snippet = video['snippet']
    statistics = video['statistics']

    video_details = {
        'title': snippet['title'],
        'channel': snippet['channelTitle'],
        'likes': int(statistics.get('likeCount', 0)),
        'views': int(statistics.get('viewCount', 0)),
        'comments': int(statistics.get('commentCount', 0)),
        'description': snippet['description']
    }

    return video_details

def fetch_youtube_video_details(query, max_results=5):
    """
    Searches for videos based on a query and fetches details for multiple videos.

    :param query: The search query string.
    :param max_results: The maximum number of videos to fetch details for.
    :return: A list of dictionaries containing video details.
    """
    video_ids = search_youtube_videos(query, max_results=max_results)

    video_details_list = []
    for video_id in video_ids:
        video_details = get_video_details(video_id)
        if video_details:
            video_details_list.append(video_details)

    return video_details_list
