import base64
import os
from tempfile import gettempdir

import pandas as pd
from pyarrow.fs import FileType
from pytest import raises
from tecton.types import Bool, Field, Float64, Int64, String, Timestamp
from tecton_core import conf as tecton_conf
from tecton_proto.materialization.params_pb2 import MaterializationTaskParams

from tecton_utils.core_utils import (
    _CACHE_PREFIX,
    featurize_async,
    get_cache_base_path,
    get_df_schema,
    run_async,
    run_async_jobs,
    set_conf,
)


def test_get_df_schema():
    df = pd.DataFrame(
        [
            dict(a=1, b=1.0, c="a", d=True, e=pd.Timestamp("2021-01-01")),
        ]
    )
    schema = get_df_schema(df)
    assert schema == [
        Field("a", Int64),
        Field("b", Float64),
        Field("c", String),
        Field("d", Bool),
        Field("e", Timestamp),
    ]

    with raises(ValueError):
        df = pd.DataFrame([dict(a=[1, 2, 3])])
        get_df_schema(df)


def test_get_cache_base_path(tmp_path):
    # test service mode
    temp_dir = str(tmp_path)
    params = MaterializationTaskParams()
    params.offline_store_path = os.path.join(temp_dir, "test", "randomid", "data")
    data = params.SerializeToString()
    data_str = base64.standard_b64encode(data).decode("utf-8")
    os.environ["MATERIALIZATION_TASK_PARAMS"] = data_str
    fs, p = get_cache_base_path()
    assert fs is not None
    assert p == os.path.join(temp_dir, "test", _CACHE_PREFIX)
    assert fs.get_file_info(p).type == FileType.Directory
    with raises(ValueError):
        # The offline_store_path format is invalid
        params.offline_store_path = os.path.join(temp_dir, "test", "randomid")
        data = params.SerializeToString()
        data_str = base64.standard_b64encode(data).decode("utf-8")
        os.environ["MATERIALIZATION_TASK_PARAMS"] = data_str
        fs, p = get_cache_base_path()

    # test dev mode
    temp_dir = gettempdir()
    del os.environ["MATERIALIZATION_TASK_PARAMS"]
    fs, p = get_cache_base_path()
    assert fs is not None
    assert p == os.path.join(temp_dir, _CACHE_PREFIX)
    assert fs.get_file_info(p).type == FileType.Directory


def test_run_async():
    async def _coro():
        return 1

    assert run_async(_coro()) == 1

    async def _coro():
        raise ValueError("error")

    with raises(ValueError):
        run_async(_coro())


def test_run_async_jobs():
    async def _coro(n):
        if n < 2:
            return n
        raise ValueError("error")

    assert run_async_jobs([_coro(0), _coro(1)], concurrency=1) == [0, 1]

    with raises(ValueError):
        run_async_jobs([_coro(0), _coro(2)], concurrency=1)


def test_featurize_async():
    async def _f1(n):
        return n + 10

    async def _f2(batch):
        return [n + 20 for n in batch]

    df = pd.DataFrame(dict(a=[1, 2, 1]))
    res = featurize_async(df, "a", "b", _f1, concurrency=2, dedup=False)
    assert res.b.tolist() == [11, 12, 11]

    df = pd.DataFrame(dict(a=[1, 2, 1]))
    res = featurize_async(
        df, "a", "b", _f2, concurrency=2, dedup=False, mini_batch_size=2
    )
    assert res.b.tolist() == [21, 22, 21]


def test_set_conf():
    tecton_conf.set("TECTON_FORCE_FUNCTION_SERIALIZATION", "false")
    assert tecton_conf.get_or_none("TECTON_FORCE_FUNCTION_SERIALIZATION") == "false"
    with set_conf({"TECTON_FORCE_FUNCTION_SERIALIZATION": "true"}):
        assert tecton_conf.get_or_none("TECTON_FORCE_FUNCTION_SERIALIZATION") == "true"
    assert tecton_conf.get_or_none("TECTON_FORCE_FUNCTION_SERIALIZATION") == "false"

    tecton_conf.set("TECTON_FORCE_FUNCTION_SERIALIZATION", None)
    with set_conf({"TECTON_FORCE_FUNCTION_SERIALIZATION": "true"}):
        assert tecton_conf.get_or_none("TECTON_FORCE_FUNCTION_SERIALIZATION") == "true"
    assert tecton_conf.get_or_none("TECTON_FORCE_FUNCTION_SERIALIZATION") is None
