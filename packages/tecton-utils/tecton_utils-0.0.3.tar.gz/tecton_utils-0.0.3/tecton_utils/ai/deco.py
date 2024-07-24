from typing import Any, Callable, Dict, List, Optional, TypeVar

from typing_extensions import ParamSpec

from tecton import FeatureView

from ._utils import FuncWrapper, build_dummy_function

_METASTORE: Dict[str, Any] = {}

T = TypeVar("T")
P = ParamSpec("P")


def _get_from_metastore(obj: Any) -> Dict[str, Any]:
    key = id(obj)
    if key not in _METASTORE:
        raise ValueError(
            f"{obj} not found in metastore, did you forget to decorate it?"
        )
    return _METASTORE[key]


def prompt(
    func: Optional[Callable[P, T]] = None,
    name: Optional[str] = None,
    sources: Optional[List[FeatureView]] = None,
) -> Callable[P, T]:
    def wrapper(
        _func: Callable[P, T],
        _name: Optional[str],
        _features: Optional[List[FeatureView]],
    ) -> Callable[P, T]:
        if _name is None:
            _name = _func.__name__
        wrapper = FuncWrapper(_name, _func, _features)
        fv = wrapper.make_feature_view()
        _METASTORE[id(_func)] = {
            "name": _name,
            "fv": fv,
            "type": "prompt",
            "llm_args": wrapper.llm_args,
            "entity_args": wrapper.entity_args,
            "feature_args": wrapper.feature_args,
        }
        return _func

    if func is None:
        return lambda _func: wrapper(_func, name, sources)
    return wrapper(func, name, sources)


def tool(
    func: Optional[Callable[P, T]] = None,
    name: Optional[str] = None,
    sources: Optional[List[FeatureView]] = None,
    descripton: Optional[str] = None,
) -> Callable[P, T]:
    def wrapper(
        _func: Callable[P, T],
        _name: Optional[str],
        _features: Optional[List[FeatureView]],
    ) -> Callable[P, T]:
        if _name is None:
            _name = _func.__name__
        wrapper = FuncWrapper(
            _name,
            _func,
            _features,
            assert_entity_defined=True,
        )
        fv = wrapper.make_feature_view()
        _METASTORE[id(_func)] = {
            "name": _name,
            "fv": fv,
            "type": "tool",
            "llm_args": wrapper.llm_args,
            "entity_args": wrapper.entity_args,
            "feature_args": wrapper.feature_args,
            "def": build_dummy_function(
                _func,
                _name,
                exclude_args=wrapper.feature_args,
            ),
            "description": descripton or _func.__doc__,
        }
        return _func

    if func is None:
        return lambda _func: wrapper(_func, name, sources)
    return wrapper(func, name, sources)
