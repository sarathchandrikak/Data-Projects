import requests
import json
from pprint import pprint
from constants import YOUTUBE_API_KEY, PLAYLIST_ID
import logging

from kafka import KafkaProducer

def fetch_page (url, parameters, page_token=None):
    params = {**parameters, 'key':YOUTUBE_API_KEY, 'page_token':page_token}
    response = requests.get(url, params)
    payload = json.loads(response.text)
    logging.debug("Response => %s", payload)
    return payload

def fetch_page_lists(url, parameters, page_token=None):
    while True:
        payload = fetch_page(url, parameters, page_token)
        yield from payload['items']
        page_token = payload.get('nextPageToken')
        if page_token is None:
            break

def format_response(video):
    video_res = {
        'title': video['snippet']['title'],
        'likes': int(video['statistics'].get('likeCount', 0)),
        'comments': int(video['statistics'].get('commentCount', 0)),
        'views': int(video['statistics'].get('viewCount', 0)),
        'favorites': int(video['statistics'].get('favoriteCount', 0)),
        'thumbnail': video['snippet']['thumbnails']['default']['url']
    }
    return video_res

def on_send_success(record_metadata):
    print(f"Sent to {record_metadata.topic} partition {record_metadata.partition} offset {record_metadata.offset}")

def on_send_error(excp):
    print(f"Error sending: {excp}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    producer = KafkaProducer(bootstrap_servers = ['localhost:9092'])
    for video_item in fetch_page_lists(url="https://www.googleapis.com/youtube/v3/playlistItems"
                                       ,parameters={'playlistId': PLAYLIST_ID, 'part':'snippet,contentDetails,status'}, page_token=None):
        video_id = video_item['contentDetails']['videoId']
        for video in fetch_page_lists(url="https://www.googleapis.com/youtube/v3/videos", 
                                        parameters={'id': video_id,  'part': 'snippet,statistics,status'}, page_token=None):
            logging.info("Video Here => %s", pprint(format_response(video)))
            producer.send('youtube_videos', json.dumps(format_response(video)).encode('utf-8'), key=video_id.encode('utf-8'))\
                    .add_callback(on_send_success)\
                    .add_errback(on_send_error)
    producer.flush()