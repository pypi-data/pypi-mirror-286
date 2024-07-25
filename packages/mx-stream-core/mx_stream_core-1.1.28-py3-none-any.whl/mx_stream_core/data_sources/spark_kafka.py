from pyspark.sql import DataFrame

from mx_stream_core.infrastructure.spark import spark
from mx_stream_core.infrastructure.kafka import read_stream_from_kafka

from mx_stream_core.data_sources.base import BaseDataSource


class SparkKafkaDataSource(BaseDataSource):
    def __init__(self, topic_name, schema, checkpoint_location, kafka_bootstrap_server = None) -> None:
        self.topic_name = topic_name
        self.schema = schema
        self.query = None
        self.checkpoint_location = checkpoint_location
        self.kafka_bootstrap_server = kafka_bootstrap_server

    def get(self) -> DataFrame:
        return read_stream_from_kafka(spark, self.topic_name, self.schema, self.kafka_bootstrap_server)

    def foreach(self, func):
        df = self.get()
        self.query = df.writeStream \
            .option("checkpointLocation", self.checkpoint_location) \
            .foreachBatch(lambda df, ep: func(df)).start()

    def awaitTermination(self):
        if self.query:
            self.query.awaitTermination()
