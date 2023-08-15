package com.finnhub

import com.finnhub.config.StreamProcessorConfig
import com.finnhub.streamprocessor.StreamProcessorJob
import com.finnhub.utils.{CassandraConfigProvider, SparkSessionBuilder}
import com.typesafe.scalalogging.LazyLogging
import org.apache.spark.sql.SparkSession

/**
 * @author ${user.name}
 */
object App extends LazyLogging with SparkSessionBuilder {

  val conf: StreamProcessorConfig = StreamProcessorConfig(
    getClass.getResource("/config/master-configuration.json").getPath
  )

  implicit val spark: SparkSession = _INIT_SPARK(conf, CassandraConfigProvider)
  
  def main(args : Array[String]) {
    new StreamProcessorJob(conf).startProcessJob()
  }

}
