package com.finhubb

import com.finnhub.config.StreamProcessorConfig
import org.json4s.DefaultFormats
import org.json4s.jackson.JsonMethods
import org.scalatest.{FunSuite, Matchers}
import com.holdenkarau.spark.testing.{DataFrameSuiteBase, SharedSparkContext}
import org.apache.spark.SparkConf

import scala.io.Source

trait StreamProcessorTestSuite
  extends FunSuite
    with Matchers
    with DataFrameSuiteBase
    with SharedSparkContext {
  implicit val streamProcessorConf: StreamProcessorConfig = readConfig[StreamProcessorConfig](
    getClass.getResource("/config/master-configuration.json").getPath
  )

  implicit val actualConfigInstance: StreamProcessorConfig = StreamProcessorConfig(
    getClass.getResource("/config/master-configuration.json").getPath
  )

  val warehouseLocation = "${system:user.dir}/spark-warehouse"

  override def conf: SparkConf = {
    new SparkConf()
      .setMaster("local[*]")
      .setAppName("test")
      .set("spark.sql.warehouse.dir", warehouseLocation)
      .set("spark.ui.enabled", "false")
      .set("spark.app.id", appID)
      .set("spark.driver.host", "localhost")
  }

  implicit val streamEventSchema: String = Source.fromFile(getClass.getResource(actualConfigInstance.schema).getPath).mkString

  private def readConfig[T](configPath: String)(implicit m: Manifest[T]): T = {
    implicit val formats: DefaultFormats = DefaultFormats

    println(configPath)
    val source = Source.fromFile(configPath)
    val configStr = source.mkString

    print(configStr)
    source.close()
    JsonMethods.parse(configStr).extract[T]
  }
}
