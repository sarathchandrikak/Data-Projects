# 🚩Kafka Streaming Pipeline

Apache Kafka is an open-source distributed event streaming platform designed for handling real-time data feeds. 
It acts as a high-throughput, fault-tolerant message broker for building data pipelines, real-time analytics, and event-driven applications.

## 🚩Core Concepts
  * Producer: Sends messages (events) to Kafka topics.
  * Consumer: Reads messages from Kafka topics.
  * Topic: A category or stream of messages, like a queue. Messages in a topic are partitioned for scalability.
  * Partition: Each topic is split into partitions to enable parallel processing.
  * Broker: A Kafka server that stores data and serves clients (producers/consumers).
  * ZooKeeper (deprecated): Manages Kafka's metadata and distributed coordination. Being replaced by Kafka's own metadata quorum.

## 🚩KRaft
Apache Kafka has been transitioning away from ZooKeeper in favor of its own KRaft (Kafka Raft) consensus protocol. 
KRaft eliminates the need for ZooKeeper, simplifying Kafka's architecture and improving scalability and manageability.
It integrates metadata management and consensus directly into Kafka brokers using the Raft protocol, removing ZooKeeper entirely.

# 🚩Real time Streaming Pipeline

## Design Architecture

## Input Data

## Commands 

## Images
