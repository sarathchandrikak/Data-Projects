# ♦️ Real Time Streaming Data Pipeline

The goal of this project is to fetch and store real-time engagement data from YouTube videos such as views, likes, and comments into a centralized database. 
This data can then be used for performance tracking, audience insights, trend forecasting, and strategic content decisions.

### ♦️ Business Use Case

To provide real-time updates on the latest YouTube metrics for user playlists, ensuring accurate and timely visibility into views, likes, and comments.

### ♦️ Stages of Pipeline

| Stage | Description                     | Input           | Output           | Tech                          |
|-------|---------------------------------|------------------|------------------|-------------------------------|
| 1. Fetch | Get real-time stats from YouTube | Playlist ID      | Video metrics    | YouTube API, Python           |
| 2. Stream | Push data to Kafka topic       | YouTube data     | Kafka messages   | Kafka Producer                |
| 3. Analyze | Process in real-time using SQL | Kafka topic      | Aggregated results | ksqlDB                      |

### ♦️ Architecture Diagram

![Image](https://github.com/sarathchandrikak/Data-Projects/blob/main/youtube-analysis/YoutubeAnalytics%20architecture.png)

### ♦️ Files Description

constants.py -> Fetches constants related to playlist_id and API key\
docker-compose.yml -> This Docker Compose file launches a full Confluent Kafka stack with the following services:

  1. **Zookeeper & Kafka Broker** – Core components for managing and running Kafka.
  2. **Schema Registry** – Stores and manages Avro schemas for Kafka data.
  3. **Kafka Connect** – Handles data integration (source/sink connectors).
  4. **ksqlDB Server** – Enables real-time SQL-based stream processing on Kafka topics.
  5. **Control Center** – A UI dashboard for monitoring and managing the entire Kafka ecosystem.

ksqldb.sql -> Queries to create streams and tables from the data coming from kafka-topic\
requirements.txt -> File containing all the package requirements of the project\
youtubeanalytics.py -> Main file that gets data from youtube videos and sends to kafka topic
