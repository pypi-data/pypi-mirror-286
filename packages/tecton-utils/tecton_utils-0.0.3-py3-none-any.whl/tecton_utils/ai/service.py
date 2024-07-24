from typing import Any, Dict, List, Optional, TypeVar

from tecton import (
    FeatureService,
    realtime_feature_view,
    BatchFeatureView,
    RealtimeFeatureView,
)
from tecton.types import Field, String

from ._utils import (
    _REQUEST,
    set_serialization,
    entity_to_tool_schema,
    fields_to_tool_schema,
)
from .deco import _get_from_metastore

FeatureView = TypeVar("FeatureView")


class AgentService:
    def __init__(
        self,
        name: str,
        prompts: Optional[List[Any]] = None,
        tools: Optional[List[Any]] = None,
        knowledge: Optional[List[Any]] = None,
        **feature_service_kwargs: Any,
    ):
        self.name = name
        self.tools: List[Any] = []
        self.prompts: List[Any] = []
        self.offline_fvs: List[FeatureView] = []
        self.metastore: Dict[str, Any] = {}
        if prompts:
            for prompt in prompts:
                self._add_prompt(prompt)
        if tools:
            for tool in tools:
                if isinstance(tool, BatchFeatureView):
                    self._add_fv_tool(tool)
                else:
                    self._add_tool(tool)
        if knowledge:
            for k in knowledge:
                self._add_knowledge(k)
        self.online_fvs: List[RealtimeFeatureView] = [
            *self.tools,
            *self.prompts,
            self._make_metastore(),
        ]
        self._run(name, **feature_service_kwargs)

    def _add_tool(self, func: Any) -> None:
        meta = dict(_get_from_metastore(func))
        if meta.get("type") != "tool":
            raise ValueError(f"Function {func} is not a tool")
        name = meta.pop("name")
        self.tools.append(meta.pop("fv"))
        self.metastore[name] = meta

    def _add_fv_tool(self, fv: BatchFeatureView) -> None:
        if len(fv.entities) != 1:
            raise ValueError(f"BatchFeatureView {fv} must have exactly one entity")
        if not fv.description:
            raise ValueError(f"BatchFeatureView {fv} must have a description")
        description = fv.description
        if fv._is_valid:
            description += (
                "\n\n The output will be a dictionary in the following schema:\n\n"
                + str(fields_to_tool_schema(fv.transformation_schema()))
            )
        tool_name = "fv_tool_" + fv.name
        schema = entity_to_tool_schema(fv.entities[0])
        self.metastore[fv.name] = {
            "name": tool_name,
            "type": "fv_tool",
            "schema": schema,
            "description": description,
        }

        with set_serialization():

            @realtime_feature_view(
                name=tool_name,
                sources=[_REQUEST, fv],
                mode="python",
                schema=[Field("output", String)],
            )
            def fv_tool(request_context, _fv) -> str:
                import json

                if tool_name != request_context["name"]:
                    return {"output": "{}"}
                return {"output": json.dumps({"result": _fv})}

            self.tools.append(fv_tool)

    def _add_prompt(self, func: Any) -> None:
        meta = dict(_get_from_metastore(func))
        if meta.get("type") != "prompt":
            raise ValueError(f"Function {func} is not a prompt")
        name = meta.pop("name")
        self.prompts.append(meta.pop("fv"))
        self.metastore[name] = meta

    def _add_knowledge(self, funcs: Any) -> None:
        self.offline_fvs.append(funcs[0])
        self._add_tool(funcs[1])

    def _make_metastore(self) -> FeatureView:
        _metastore = self.metastore

        with set_serialization():

            @realtime_feature_view(
                name="metastore",
                sources=[_REQUEST],
                mode="python",
                schema=[Field("output", String)],
            )
            def metastore(request_context) -> str:
                import json

                if "metastore" != request_context["name"]:
                    return {"output": "{}"}
                return {"output": json.dumps({"result": _metastore})}

            return metastore

    def _run(self, name: str, **kwargs) -> List[FeatureService]:
        fs = [
            FeatureService(name=name + "_" + tool.name, **kwargs, features=[tool])
            for tool in self.online_fvs
        ]
        for fv in self.offline_fvs:
            fs.append(
                FeatureService(
                    name=name + "_" + fv.name,
                    **kwargs,
                    features=[fv],
                    online_serving_enabled=False,
                )
            )
        return fs
