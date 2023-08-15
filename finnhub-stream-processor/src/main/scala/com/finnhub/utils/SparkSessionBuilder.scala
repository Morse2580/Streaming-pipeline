package com.finnhub.utils

import com.finnhub.config.StreamProcessorConfig
import org.apache.spark.SparkConf
import org.apache.spark.sql.SparkSession

/*
* While the code may seem a bit verbose for a small task(spark initialization), it provides a solid foundation for managing Spark session
* initialization in a scalable and maintainable way. It's important to consider the long-term requirements and potential
* future enhancements of your application when designing the initialization code.
* */

trait SparkConfigProvider[T] {

  val warehouseLocation = "${system:user.dir}/spark-warehouse"
  def sparkConf(config: T): SparkConf
}

object BaseSparkConfigProvider extends SparkConfigProvider[StreamProcessorConfig] {
  override def sparkConf(config: StreamProcessorConfig): SparkConf = {
    new SparkConf()
      .setMaster(config.sparkConfig.master)
      .setAppName(config.sparkConfig.appName)
      .set("spark.sql.warehouse.dir", warehouseLocation)
      .set("spark.ui.enabled", "false")
      .set("spark.driver.host", "localhost")
      .set("spark.sql.shuffle.partitions", config.sparkConfig.shuffle_partitions)
  }
}

object CassandraConfigProvider extends SparkConfigProvider[StreamProcessorConfig] {
  override def sparkConf(config: StreamProcessorConfig): SparkConf = {
    BaseSparkConfigProvider.sparkConf(config)
      .set("spark.cassandra.connection.host", config.cassandraConfig.host)
      .set("spark.cassandra.auth.username", config.cassandraConfig.user)
      .set("spark.cassandra.auth.password", config.cassandraConfig.password)
  }
}

trait SparkSessionBuilder {
  def _INIT_SPARK[T](config: T, configProvider: SparkConfigProvider[T]): SparkSession = {
    val sparkConf = configProvider.sparkConf(config)
    createSparkSession(sparkConf)
  }

  private def createSparkSession(sparkConf: SparkConf): SparkSession = {
    SparkSession
      .builder()
      .config(sparkConf)
      .getOrCreate()
  }
}






