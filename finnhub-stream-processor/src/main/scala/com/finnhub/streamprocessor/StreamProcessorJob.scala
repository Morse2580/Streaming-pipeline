package com.finnhub.streamprocessor

import com.datastax.oss.driver.api.core.uuid.Uuids
import com.finnhub.config.StreamProcessorConfig
import com.typesafe.scalalogging.LazyLogging
import org.apache.spark.sql.avro.functions._
import org.apache.spark.sql.cassandra.DataFrameWriterWrapper
import org.apache.spark.sql.expressions.UserDefinedFunction
import org.apache.spark.sql.functions._
import org.apache.spark.sql.streaming.Trigger
import org.apache.spark.sql.{DataFrame, SparkSession}

import scala.io.Source

class StreamProcessorJob(
                          config: StreamProcessorConfig
                        ) extends LazyLogging{

  def startProcessJob()(implicit sparkSession: SparkSession): Unit = {
    val dataStream = kafkaStreamConsumer(config)

    val streamEventSchema: String = Source.fromFile(getClass.getResource(config.schema).getPath).mkString

    val deserializedDf = deserializeAvroStream(dataStream, streamEventSchema)

    // generate unique string identifier
    val generateUUID = udf(() => Uuids.timeBased().toString)

    //------ Unaggregated Dataframe ------------
    val finalDf: DataFrame = createFinalDF(deserializedDf, generateUUID)

    writeFinalDF(finalDf, config)

    //------ aggregated Dataframe ------------
    val aggregateDf = fifteenMinuteAggregate(finalDf, generateUUID)

    writeAggregateDf(aggregateDf, config)

    sparkSession.streams.awaitAnyTermination()
  }
  def kafkaStreamConsumer(
                           config: StreamProcessorConfig
                         )(implicit spark: SparkSession): DataFrame = {

    val bootstrapServer = s"${config.kafkaConfig.server}:${config.kafkaConfig.port}"

    // read streams from Kafka
    val inputDF = spark
      .readStream
      .format("kafka")
      .option("kafka.bootstrap.servers", bootstrapServer)
      .option("subscribe", config.kafkaConfig.topic)
      .option("minPartitions", config.kafkaConfig.min_partitions)
      .option("maxOffsetsPerTrigger", config.sparkConfig.max_offsets_per_trigger)
      .option("useDeprecatedOffsetFetching", config.sparkConfig.deprecated_offsets)
      .load()

    inputDF
  }

  def deserializeAvroStream(
                             kafkaStream: DataFrame,
                            EventStreamSchema: String
                           ): DataFrame = {

    val expandedDF = kafkaStream
      .withColumn("avroData", from_avro(col("value"), EventStreamSchema))
      .select(col("avroData.*"))
      .select(explode(col("data")), col("type"))
      .select("col.*")

    expandedDF
  }

  def createFinalDF(
                     deserializedStream: DataFrame,
                     generateUUID: UserDefinedFunction
                   ): DataFrame = {

    val finalDF = deserializedStream
      .withColumn("uuid", generateUUID())
      .withColumnRenamed("c", "trade_conditions")
      .withColumnRenamed("p", "price")
      .withColumnRenamed("s", "symbol")
      .withColumnRenamed("t", "trade_timestamp")
      .withColumnRenamed("v", "volume")
      .withColumn("trade_timestamp", (col("trade_timestamp") / 1000).cast("timestamp"))
      .withColumn("ingest_timestamp", current_timestamp().as("ingest_timestamp"))

    finalDF
  }

  def writeFinalDF(
                    finalDF: DataFrame,
                    config: StreamProcessorConfig
                  ): Unit = {
    // write query to Cassandra
    val query = finalDF
      .writeStream
      .foreachBatch { (batchDF: DataFrame, batchID: Long) =>
        println(s"Writing to Cassandra $batchID")
        batchDF.write
          .cassandraFormat(config.cassandraConfig.cassandraTables.trades, config.cassandraConfig.keyspace)
          .mode("append")
          .save()
      }
      .outputMode("update")
      .start()
  }


  /*
  *
  * run for the aggregates tables
  *
  * */

  def fifteenMinuteAggregate(df: DataFrame,
                             generateUUID: UserDefinedFunction): DataFrame = {

    // another dataframe with aggregates - running averages from last 15 seconds
    val summaryDF = df
      .withColumn("price_volume_multiply",
        col("price") * col("volume"))
      .withWatermark("trade_timestamp", "15 seconds")
      .groupBy("symbol")
      .agg(avg("price_volume_multiply"))

    //rename columns in dataframe and add UUIDs before inserting to Cassandra
    val finalSummaryDF = summaryDF
      .withColumn("uuid", generateUUID())
      .withColumn("ingest_timestamp", current_timestamp().as("ingest_timestamp"))
      .withColumnRenamed("avg(price_volume_multiply)", "price_volume_multiply")


    finalSummaryDF
  }

  def writeAggregateDf(aggDf: DataFrame, config: StreamProcessorConfig): Unit = {
    val aggDF = aggDf
      .writeStream
      .trigger(Trigger.ProcessingTime("5 seconds"))
      .foreachBatch { (batchDF: DataFrame, batchID: Long) =>
        println(s"Writing to Cassandra $batchID")
        batchDF.write
          .cassandraFormat(config.cassandraConfig.cassandraTables.aggregates, config.cassandraConfig.keyspace)
          .mode("append")
          .save()
      }
      .outputMode("update")
      .start()
  }
}
