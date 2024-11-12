
# Commands to Run the Project


#### Install Kafka
wget https://archive.apache.org/dist/kafka/3.3.1/kafka_2.12-3.3.1.tgz
tar -xvf kafka_2.12-3.3.1.tgz

#### Install Java
sudo yum install java-1.8.0-openjdk
java -version


#### Start ZooKeeper
cd kafka-folder
bin/zookeeper-server-start.sh config/zookeeper.properties

### Kafka

   * Before starting kafka server, change advertised.listeners in config/server.properties, provide ec2-instance public ip 
   * export KAFKA_HEAP_OPTS="-Xmx256M -Xms128M" - Memory related config with Kafka
   * bin/kafka-server-start.sh config/server.properties

    If encountered any issues, find pid using Kafka server using this command
            sudo lsof -i : 9092
    Kill the PID using 
            sudo kill -9 PID
    Stop Kafka Server 
            bin/kafka-server-stop.sh 


### Topic, Producer consumer 

   * Create topic in Kafka using the command 

            bin/kafka-topics.sh --create --topic demotesting2 --bootstrap-server public-ip:9092 --replication-factor 1 --partitions 1

   * Testing Purpose
        * Start Producer 
                bin/kafka-console-producer.sh --topic demotesting2 --bootstrap-server  public-ip:9092

        * Start Consumer
                bin/kafka-console-consumer.sh --topic demotesting2 --bootstrap-server public-ip:9092