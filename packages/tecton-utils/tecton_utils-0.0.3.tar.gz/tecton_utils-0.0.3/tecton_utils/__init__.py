# flake8: noqa
from contextlib import suppress

with suppress(ImportError):
    from tecton_utils.utils import chunked_get_historical_features
