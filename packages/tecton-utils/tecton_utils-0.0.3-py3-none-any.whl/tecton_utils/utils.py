import logging
from datetime import timedelta
from typing import Optional, Union

import pyspark
import tecton
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.utils import AnalysisException

logger = logging.getLogger(__name__)


def _get_partitions(output_path, partition_col):
    try:
        spark = SparkSession.getActiveSession()
        df = spark.read.parquet(output_path)
    except AnalysisException as e:
        if "Path does not exist" in str(e):
            return []
        raise
    partitions = df.select(F.col(partition_col)).distinct().collect()
    return set([i[partition_col] for i in partitions])


def _chunkify(l, n):
    return [l[i : i + n] for i in range(0, len(l), n)]


def _format_partition_list(l):
    return [p.strftime("%Y-%m-%d") for p in sorted(list(l))]


def chunked_get_historical_features(
    fv_or_fs: Union[tecton.FeatureView, tecton.FeatureService],
    spine: pyspark.sql.DataFrame,
    timestamp_key: str,
    output_path: str,
    partition_col: str,
    repartition: Optional[int] = 16,
    split_size_days: int = 10,
    **get_historical_features_kwargs,
) -> pyspark.sql.DataFrame:
    """
    Computes historical features for a given spine. This function breaks the
    computation into chunks by day based on split_size_days.

    This persists any results in a day-partitioned Parquet table at output_path.
    If this function is interrupted, re-running it will pick off from where it left off.

    Args:
        fv_or_fs: The feature view or feature service to compute historical features for.
        spine: The spine to compute historical features for, as a Spark DataFrame.
        timestamp_key: The name of the timestamp column in the spine, passed to get_historical_features.
        output_path: The path to write the historical features to.
        partition_col: The name of the daily partition column in the output table.
            Must not overlap with any existing columns.
        repartition: The number of partitions to repartition the output table to. Affects the
            numbers of file per partition. If None, no repartitioning is done.
        split_size_days: The number of days to compute historical features for at a time.
        get_historical_features_kwargs: Additional keyword arguments to pass to get_historical_features.

    Returns:
        pyspark.sql.DataFrame: The spine with the historical features joined, partitioned by partition_col.
    """
    spark = SparkSession.getActiveSession()
    row = spine.select(
        F.expr(f"max({timestamp_key}) as max_ts"),
        F.expr(f"min({timestamp_key}) as min_ts"),
    ).collect()[0]
    min_ds = row["min_ts"].date()
    max_ds = row["max_ts"].date() + timedelta(days=1)
    total_days = (max_ds - min_ds).days

    existing_partitions = _get_partitions(output_path, partition_col)

    logger.info(
        f"{len(existing_partitions)} existing partitions found: {_format_partition_list(existing_partitions)}"
    )

    partitions_to_compute = []

    for i in range(total_days):
        ds = min_ds + timedelta(days=i)
        if ds not in existing_partitions:
            partitions_to_compute.append(ds)

    partitions_to_compute = sorted(partitions_to_compute)

    logger.info(
        f"Computing the following {len(partitions_to_compute)} partitions: {_format_partition_list(partitions_to_compute)}"
    )

    splits = _chunkify(partitions_to_compute, split_size_days)

    for partition_list in splits:
        logger.info(
            f"Starting GHF computation for partitions {_format_partition_list(partition_list)}"
        )
        filtered_spine = spine.filter(
            F.to_date(F.col(timestamp_key)).isin(partition_list)
        )
        ghf_result = fv_or_fs.get_historical_features(
            spine=filtered_spine,
            timestamp_key=timestamp_key,
            **get_historical_features_kwargs,
        ).to_spark()
        if repartition:
            ghf_result = ghf_result.repartition(repartition)
        ghf_result = ghf_result.withColumn(
            partition_col, F.expr(f"to_date({timestamp_key})")
        )
        ghf_result.write.option("partitionOverwriteMode", "dynamic").partitionBy(
            partition_col
        ).parquet(output_path, mode="overwrite")
        logger.info(
            f"GHF result saved for partitions {_format_partition_list(partition_list)}"
        )
    return spark.read.parquet(output_path)
