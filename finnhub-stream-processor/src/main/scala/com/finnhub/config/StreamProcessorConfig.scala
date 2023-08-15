package com.finnhub.config

import com.typesafe.scalalogging.LazyLogging
import org.json4s.DefaultFormats
import org.json4s.jackson.JsonMethods

import java.nio.file.{Files, Paths}
import scala.util.{Failure, Success, Try}


case class SparkConfig(
                        master: String,
                        appName: String,
                        max_offsets_per_trigger: String,
                        shuffle_partitions: String,
                        deprecated_offsets: String
                      )

case class KafkaConfig(
                        server: String,
                        port: String,
                        topic: String,
                        min_partitions: String
                      )

case class CassandraTables(
                          trades: String,
                          aggregates: String
                          )
case class CassandraConfig(
                     host: String,
                     user: String,
                     password: String,
                     keyspace: String,
                     cassandraTables: CassandraTables
                   )

case class StreamProcessorConfig(
                      sparkConfig: SparkConfig,
                      kafkaConfig: KafkaConfig,
                      cassandraConfig: CassandraConfig,
                      schema: String,
                      resource_path:String
                    )

/** Object to creating a Configuration object
 */
object StreamProcessorConfig extends LazyLogging {

  /** Load configuration from a file.
   */
  private def loadConfig[T](configPath: String)(implicit m: Manifest[T]): Option[T] = {
    Try(Files.readAllBytes(Paths.get(configPath))) match {
      case Success(bytes) =>
        val configStr = new String(bytes)
        parseConfig[T](configStr)

      case Failure(exception) =>
        logger.error(s"Failed to read configuration file: $configPath", exception)
        None
    }
  }

  /** Parse configuration from a JSON string.
   *
   */
  private def parseConfig[T](configStr: String)(implicit m: Manifest[T]): Option[T] = {
    implicit val formats: DefaultFormats = DefaultFormats

    Try(JsonMethods.parse(configStr).extract[T]) match {
      case Success(config) =>
        Some(config)

      case Failure(exception) =>
        logger.error("Failed to parse configuration", exception)
        None
    }
  }

  /** Load configuration from a file using the apply method.
   *
   */
  def apply(configPath: String): StreamProcessorConfig = {
    loadConfig[StreamProcessorConfig](configPath) match {
      case Some(config) => config
      case None => throw new Exception(s"Failed to load configuration from file: $configPath")
    }
  }
}