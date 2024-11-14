FROM openjdk:11-jre-slim
WORKDIR /kafka
RUN wget https://downloads.apache.org/kafka/3.8.0/kafka_2.13-3.8.0.tgz && \
    tar -xzf kafka_2.13-3.8.0.tgz
CMD ["/kafka/kafka_2.13-3.8.0/bin/kafka-server-start.sh", "/kafka/kafka_2.13-3.8.0/config/server.properties"]
