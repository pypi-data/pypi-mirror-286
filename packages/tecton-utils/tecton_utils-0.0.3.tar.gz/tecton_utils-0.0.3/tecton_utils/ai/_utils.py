import ast
import inspect
from contextlib import contextmanager
from typing import Any, Callable, Dict, Iterator, List, Optional, Tuple, Union

from tecton import (
    Entity,
    FeatureView,
    RequestSource,
    realtime_feature_view,
    RequestSource,
)
from tecton.types import Bool, Field, Float32, Float64, Int32, Int64, String
from tecton_core import conf as tecton_conf

from tecton_utils.core_utils import set_conf

_REQUEST = RequestSource(schema=[Field("name", String), Field("input", String)])


class FuncWrapper:
    def __init__(
        self,
        name: str,
        func: Callable,
        sources: Optional[List[FeatureView]] = None,
        assert_entity_defined: bool = False,
    ):
        self.name = name
        self.views = sources or []
        self.func = func
        self.llm_args, self.feature_args, self.entity_args, self.use_request_source = (
            _parse_arguments(
                func, self.views, assert_entity_defined=assert_entity_defined
            )
        )
        if self.use_request_source:
            self.views = self.views[1:]

    def make_feature_view(self, **odfv_kwargs: Any) -> FeatureView:
        name = self.name
        func = self.func
        func_name = func.__name__
        doc = func.__doc__
        use_request_source = self.use_request_source
        fv_names = [fv.name for fv in self.views]
        deco = realtime_feature_view(
            name=name,
            description=doc,
            sources=[_REQUEST] + self.views,
            mode="python",
            schema=[Field("output", String)],
            **odfv_kwargs,
        )

        def tool_service(request_context, *fvs):
            import json

            if name != request_context["name"]:
                return {"output": "{}"}
            if use_request_source:
                pos_args: List[Any] = [json.loads(request_context["input"])]
                params = {}
            else:
                pos_args: List[Any] = []
                params = json.loads(request_context["input"])
            try:  # make tecton compiler embed this function
                f = func  # running locally
            except Exception:  # tecton runtime can't really get this function
                f = globals()[func_name]  # running on server
            for key, fv in zip(fv_names, fvs):
                params[key] = fv
            try:
                res = f(*pos_args, **params)
                return {"output": json.dumps({"result": res})}
            except Exception:
                from traceback import format_exc

                return {"output": json.dumps({"error": format_exc()})}

        with set_serialization():

            if len(self.views) == 0:

                def tool_service_wrapper(request_context):
                    return tool_service(request_context)

                return deco(tool_service_wrapper)
            if len(self.views) == 1:

                def tool_service_wrapper(request_context, fv1):
                    return tool_service(request_context, fv1)

                return deco(tool_service_wrapper)
            if len(self.views) == 2:

                def tool_service_wrapper(request_context, fv1, fv2):
                    return tool_service(request_context, fv1, fv2)

                return deco(tool_service_wrapper)
            if len(self.views) == 3:

                def tool_service_wrapper(request_context, fv1, fv2, fv3):
                    return tool_service(request_context, fv1, fv2, fv3)

                return deco(tool_service_wrapper)
            if len(self.views) == 4:

                def tool_service_wrapper(request_context, fv1, fv2, fv3, fv4):
                    return tool_service(request_context, fv1, fv2, fv3, fv4)

                return deco(tool_service_wrapper)
            if len(self.views) == 5:

                def tool_service_wrapper(request_context, fv1, fv2, fv3, fv4, fv5):
                    return tool_service(request_context, fv1, fv2, fv3, fv4, fv5)

                return deco(tool_service_wrapper)
        raise NotImplementedError("Too many sources")


def build_dummy_function(
    func: Callable, name: str, exclude_args: Optional[Iterator[str]] = None
):
    if not name.isidentifier():
        raise ValueError(f"{name} is not a valid identifier")
    code = _prepare_code(inspect.getsource(func))
    func_def = ast.parse(code).body[0]
    func_def.name = name
    func_def.body = [ast.Pass()]
    exclude = set(exclude_args or [])
    args: Any = []
    for arg in func_def.args.args:
        if arg.arg not in exclude:
            args.append(arg)
    func_def.args.args = args
    return ast.unparse(func_def)


@contextmanager
def set_serialization():
    import sys

    if "ipykernel" in sys.modules or tecton_conf.get_bool("TECTON_DEBUG"):
        yield
    else:  # not in notebook
        with set_conf({"TECTON_FORCE_FUNCTION_SERIALIZATION": "true"}):
            yield


def entity_to_tool_schema(entity: Entity) -> Dict[str, str]:
    schema: Dict[str, str] = {}
    for item in entity._args.join_keys:
        name = item.name
        if not name.isidentifier():
            raise ValueError(f"{name} is not a valid identifier")
        tp = item.offline_data_type
        if String.tecton_type.proto == tp:
            schema[name] = "str"
        elif Int32.tecton_type.proto == tp:
            schema[name] = "int"
        elif Int64.tecton_type.proto == tp:
            schema[name] = "int"
        elif Float32.tecton_type.proto == tp:
            schema[name] = "float"
        elif Float64.tecton_type.proto == tp:
            schema[name] = "float"
        elif Bool.tecton_type.proto == tp:
            schema[name] = "bool"
        else:
            raise ValueError(f"Unsupported type {tp} for {name}")
    return schema


def fields_to_tool_schema(fields: List[Field]) -> Dict[str, str]:
    schema: Dict[str, str] = {}
    for item in fields:
        name = item.name
        if not name.isidentifier():
            raise ValueError(f"{name} is not a valid identifier")
        tp = item.dtype.tecton_type
        if String.tecton_type == tp:
            schema[name] = "str"
        elif Int32.tecton_type == tp:
            schema[name] = "int"
        elif Int64.tecton_type == tp:
            schema[name] = "int"
        elif Float32.tecton_type == tp:
            schema[name] = "float"
        elif Float64.tecton_type == tp:
            schema[name] = "float"
        elif Bool.tecton_type == tp:
            schema[name] = "bool"
        else:
            raise ValueError(f"Unsupported type {tp} for {name}")
    return schema


def _prepare_code(code):
    lines = code.splitlines()
    for i, line in enumerate(lines):
        if line.strip().startswith("def "):
            indent = line.index("def ")
            return "\n".join(x[indent:] for x in lines[i:])


def _parse_arguments(
    func: Callable,
    sources: List[Union[Union[RequestSource, FeatureView]]],
    assert_entity_defined: bool,
) -> Tuple[List[str], List[str], List[str], bool]:
    if len(sources) == 0 or not isinstance(sources[0], RequestSource):
        # request source is not used
        orig_args = inspect.getfullargspec(func).args
        llm_args, feature_args, entitye_args = _parse_arguments_no_request_sourcre(
            func,
            orig_args,
            sources,
            assert_entity_defined,
            assert_all_feature_args=False,
        )
        return llm_args, feature_args, entitye_args, False
    else:
        orig_args = inspect.getfullargspec(func).args
        _, feature_args, entitye_args = _parse_arguments_no_request_sourcre(
            func,
            orig_args[1:],
            sources[1:],
            assert_entity_defined,
            assert_all_feature_args=True,
        )
        llm_args = [x.name for x in sources[0].schema]
        return llm_args, feature_args, entitye_args, True


def _parse_arguments_no_request_sourcre(
    func: Callable,
    orig_args: List[str],
    sources: List[FeatureView],
    assert_entity_defined: bool,
    assert_all_feature_args: bool,
) -> Tuple[List[str], List[str], List[str]]:

    feature_args = [source.name for source in sources]
    if not set(feature_args).issubset(orig_args):
        raise ValueError(
            f"All feature view names ({feature_args}) "
            f"must be defined in {func} arguments"
        )
    if len(sources) == 0:
        entity_args: List[str] = []
    else:
        jk = sources[0].join_keys
        for source in sources[1:]:
            if set(jk) != set(source.join_keys):
                raise ValueError("All sources must have the same join keys")
        entity_args = jk
    if assert_entity_defined:
        if not set(entity_args).issubset(orig_args):
            raise ValueError(
                f"All entity keys ({entity_args}) must be defined in {func}"
            )
    else:
        if len(set(entity_args).intersection(orig_args)) > 0:
            raise ValueError(
                f"All entity keys ({entity_args}) must not be defined in {func}"
            )
    llm_args = [x for x in orig_args if x not in feature_args]
    if assert_all_feature_args and len(llm_args) > 0:
        raise ValueError(
            f"Only features and request source arguments are allowed: {llm_args}"
        )
    return llm_args, feature_args, entity_args
