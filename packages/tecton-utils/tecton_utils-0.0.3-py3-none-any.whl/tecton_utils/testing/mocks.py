from datetime import timedelta
from typing import Any, List, Optional

import pandas as pd
import pyarrow as pa
from tecton import (
    BatchFeatureView,
    BatchSource,
    Entity,
    batch_feature_view,
    pandas_batch_config,
)

from ..core_utils import get_df_schema

_MAX_ROWS = 100


def mock_source(name: str, df: pd.DataFrame, **source_kwargs: Any) -> BatchSource:

    if len(df) > _MAX_ROWS:
        raise ValueError(f"Dataframe has more than {_MAX_ROWS} rows")

    data = df.to_dict("records")
    pa.Table.from_pandas(df).schema

    @pandas_batch_config()
    def api_df():
        return pd.DataFrame(data)

    return BatchSource(name=name, batch_config=api_df, **source_kwargs)


def mock_feature_view(
    name: str,
    df: pd.DataFrame,
    entity_keys: List[str],
    timestamp_field: Optional[str] = None,
    **fv_kwargs: Any,
) -> BatchFeatureView:

    if timestamp_field is None:
        timestamp_field = "_tecton_auto_ts"
        df = df.assign(**{timestamp_field: "2024-01-01"})
    df = df.assign(**{timestamp_field: pd.to_datetime(df[timestamp_field])})

    source = mock_source(name + "_source", df)
    schema = get_df_schema(df)
    join_keys = [x for x in schema if x.name in entity_keys]
    if len(join_keys) != len(entity_keys):
        raise ValueError(f"Entity keys {entity_keys} not all found in schema {schema}")
    entity = Entity(name=name + "_entity", join_keys=join_keys)

    base_args = dict(
        name=name,
        sources=[source],
        entities=[entity],
        mode="pandas",
        online=True,
        offline=True,
        schema=schema,
        feature_start_time=df[timestamp_field].min().to_pydatetime(),
        batch_schedule=timedelta(days=1),
        timestamp_field=timestamp_field,
        environment="tecton-rift-core-0.9.0",
    )
    base_args.update(fv_kwargs)

    @batch_feature_view(**base_args)
    def dummy(_df):
        return _df

    return dummy
