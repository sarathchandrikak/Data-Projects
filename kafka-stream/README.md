# 🚩Kafka Streaming Pipeline

Apache Kafka is an open-source distributed event streaming platform designed for handling real-time data feeds. 
It acts as a high-throughput, fault-tolerant message broker for building data pipelines, real-time analytics, and event-driven applications.

![img](https://github.com/sarathchandrikak/Data-Projects/blob/main/kafka-stream/images.png)

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

## 🚩 Design Architecture

![img](https://github.com/sarathchandrikak/Data-Projects/blob/main/kafka-stream/Architecture.jpg)

## 🚩 Input Data

Data for this stock market project is available ![here](https://github.com/sarathchandrikak/Data-Projects/blob/main/kafka-stream/indexProcessed.csv)

## 🚩Commands 

#### Install Kafka

          wget https://archive.apache.org/dist/kafka/3.3.1/kafka_2.12-3.3.1.tgz
          tar -xvf kafka_2.12-3.3.1.tgz

#### Install Java

           sudo yum install java-1.8.0-openjdk
           java -version

#### Start ZooKeeper
          
          cd kafka_2.12-3.3.1
          bin/zookeeper-server-start.sh config/zookeeper.properties

### Kafka

Before starting kafka server, change advertised.listeners in config/server.properties to ec2-instance public ip 

            export KAFKA_HEAP_OPTS="-Xmx256M -Xms128M"
            bin/kafka-server-start.sh config/server.properties

 If encountered any issues, find pid using Kafka server using this command and kill PIDs running default zookeeper and kafka servers
         
            sudo lsof -i: 9092
            sudo lsof -i: 2181            
            sudo kill -9 PID
            bin/kafka-server-stop.sh 

 ### Topic, Producer consumer 

   * Create topic in Kafka using the command 

            bin/kafka-topics.sh --create --topic topid-name --bootstrap-server public-ip:9092 --replication-factor 1 --partitions 1

  * Start Producer 

           bin/kafka-console-producer.sh --topic topic-name --bootstrap-server  public-ip:9092

 * Start Consumer

           bin/kafka-console-consumer.sh --topic topic-name --bootstrap-server public-ip:9092

## Images

   After successful costruction of data pipeline, can query on the table available in athena

   ![image](https://github.com/user-attachments/assets/4edb2674-88fe-4947-8a32-e9bf13614c9e)



