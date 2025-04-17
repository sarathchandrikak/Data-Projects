CREATE STREAM youtube_videos (
  video_id VARCHAR key,
  title VARCHAR,
  likes INT,
  comments INT,
  views INT,
  favorites INT,
  thumbnails VARCHAR
)
WITH ( KAFKA_TOPIC = 'youtube_videos',
      PARTITIONS = 1,
      VALUE_FORMAT = 'json'
      );  



CREATE TABLE youtube_analytics_changes WITH (KAFKA_TOPIC = 'youtube_videos') AS 
SELECT
  video_id,
  latest_by_offset(title) AS title,
  latest_by_offset(comments, 2)[1] AS comments_prev,
  latest_by_offset(comments, 2)[0] AS comments_curr,
  latest_by_offset(likes, 2)[1] AS likes_prev,
  latest_by_offset(likes, 2)[0] AS likes_curr,
  latest_by_offset(views, 2)[1] AS views_prev,
  latest_by_offset(views, 2)[0] AS views_curr,
  latest_by_offset(favorites, 2) AS favorites
FROM youtube_videos
GROUP BY video_id
EMIT CHANGES;
