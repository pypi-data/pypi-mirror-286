import pyspark
import socket

__DEFAULT__JAR_PACKAGES = [
    'com.google.cloud.spark:spark-bigquery-with-dependencies_2.12:0.39.0',

    'com.microsoft.azure:spark-mssql-connector_2.12:1.2.0',
    'com.microsoft.sqlserver:mssql-jdbc:12.6.2.jre11',
]


def get_spark_session(
        name: str,
        cpu: str = "1",
        memory: str = "1024m",
        monitor: bool = False,
        config: dict = {}
):
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    jars = __DEFAULT__JAR_PACKAGES

    if "spark.jars.packages" in config:
        _jars = config["spark.jars.packages"].split(",")
        jars.extend(_jars)
        del config["spark.jars.packages"]

    conf = pyspark.SparkConf()

    conf.setMaster("spark://raya-spark-master-0.raya-spark-headless.spark.svc.cluster.local:7077")
    conf.setAppName(name)

    conf.set("spark.driver.host", ip_address)

    conf.set("spark.dynamicAllocation.enabled", "true")
    conf.set("spark.executor.cores", cpu)
    conf.set("spark.executor.memory", memory)

    conf.set("spark.jars.packages", ",".join(jars))

    if monitor:
        conf.set('spark.extraListeners', 'sparkmonitor.listener.JupyterSparkMonitorListener')
        conf.set('spark.driver.extraClassPath', '/opt/conda/lib/python3.11/site-packages/sparkmonitor/listener_2.12.jar')
    else:
        conf.set('spark.ui.showConsoleProgress', 'false')

    for key, value in config.items():
        conf.set(key, value)

    return pyspark.sql.SparkSession.builder \
        .config(conf=conf) \
        .enableHiveSupport() \
        .getOrCreate()