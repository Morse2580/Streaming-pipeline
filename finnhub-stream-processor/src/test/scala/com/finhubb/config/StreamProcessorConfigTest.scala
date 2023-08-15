package com.finhubb.config

import com.finhubb.StreamProcessorTestSuite
import com.finnhub.config.{CassandraConfig, CassandraTables, KafkaConfig, SparkConfig, StreamProcessorConfig}

class StreamProcessorConfigTest extends StreamProcessorTestSuite {
  test("A configuration file should be loaded and parse correctly"){
    actualConfigInstance shouldEqual StreamProcessorConfig(
      sparkConfig = SparkConfig(
        "local[*]",
        "Stream Processor",
        "1000",
        "2",
        "false"
      ),
       kafkaConfig = KafkaConfig(
        "localhost",
        "9092",
        "raw-live-trades",
         "1"
      ),
       cassandraConfig = CassandraConfig(
        "jdbc:mysql://localhost:3306/my_database",
        "db_user",
        "db_password",
         "market",
         cassandraTables = CassandraTables(
           "trades",
           "running_averages_15_sec"
         )
      ),
       schema = "/schemas/trades.asvc",
       resource_path = "/config/master-configuration.json"
    )
  }

  test("display schema as a string"){
    println(streamEventSchema)
  }
}
