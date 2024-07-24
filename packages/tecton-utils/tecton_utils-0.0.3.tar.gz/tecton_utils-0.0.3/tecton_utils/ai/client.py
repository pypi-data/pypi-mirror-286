import json
from datetime import datetime

# for executing function declarations
from typing import Any, Dict, List, Tuple  # noqa

import pandas as pd
from tecton import BatchFeatureView, RealtimeFeatureView

from .service import AgentService

_DEFAULT_TOP_K = 5
_SEARCH_TOOL_PREFIX = "search_"


class AgentClient:
    @staticmethod
    def from_remote(
        url: str, workspace: str, service: str, api_key: str
    ) -> "AgentClient":
        return _AgentClientRemote(url, workspace, service, api_key)

    @staticmethod
    def from_local(service: AgentService) -> "AgentClient":
        return _AgentClientLocal(service)

    def _get_feature_value(
        self, name: str, key_map: Dict[str, Any], request_map: Dict[str, Any]
    ):
        raise NotImplementedError

    @property
    def metastore(self):
        return self._invoke("metastore", [], [], {})

    def invoke_tool(self, name, **kwargs):
        meta = self.metastore[name]
        if meta["type"] == "fv_tool":
            return self.invoke_feature_view(name, **kwargs)
        entity_args = meta.get("entity_args", [])
        llm_args = meta.get("llm_args", [])
        return self._invoke(name, entity_args, llm_args, kwargs)

    def invoke_feature_view(self, name, **kwargs):
        tool_name = "fv_tool_" + name
        tool = self.metastore[name]

        key_map = {k: kwargs[k] for k in tool["schema"].keys()}

        return self._get_feature_value(tool_name, key_map, {})

    def invoke_prompt(self, name, **kwargs):
        metastore = self.metastore
        entity_args = metastore[name].get("entity_args", [])
        llm_args = metastore[name].get("llm_args", [])
        return self._invoke(name, entity_args, llm_args, kwargs)

    def search(self, name, query: str, top_k: int = _DEFAULT_TOP_K):
        return self.invoke_tool(
            _SEARCH_TOOL_PREFIX + name,
            query=query,
            top_k=top_k,
        )

    def _invoke(self, name, entity_args, llm_args, kwargs):
        ctx_map = {}
        key_map = {}
        for k, v in kwargs.items():
            if k in entity_args:
                key_map[k] = v
            elif k not in llm_args:
                raise ValueError(f"Unknown argument {k}")
            if k in llm_args:
                ctx_map[k] = v

        return self._get_feature_value(name, key_map, ctx_map)

    def make_lc_tool(self, name):
        from langchain_core.tools import StructuredTool

        meta = self.metastore[name]
        if meta["type"] == "tool":
            code = meta["def"]
        elif meta["type"] == "fv_tool":
            schema = meta["schema"]
            params = ",".join(f"{k}:{v}" for k, v in schema.items())
            code = f"def func({params}) -> 'Dict[str,Any]'\n    pass"
        else:
            raise ValueError(f"Unknown tool type {meta['type']}")
        exec(code, globals(), locals())
        descripton = meta.get("description")
        f = locals()[name]
        _tool = StructuredTool.from_function(name=name, func=f, description=descripton)
        _tool.func = lambda **kwargs: self.invoke_tool(name, **kwargs)
        return _tool

    def to_lc_tools(self):
        return [
            self.make_lc_tool(name)
            for name, value in self.metastore.items()
            if value["type"] == "tool"
        ]

    def make_agent(self, llm, system_prompt=None) -> "Agent":
        if system_prompt:
            if self.metastore.get(system_prompt).get("type") != "prompt":
                raise ValueError(f"{system_prompt} is not a prompt.")
        return Agent(self, llm, system_prompt=system_prompt)


class _AgentClientRemote(AgentClient):
    def __init__(self, url: str, workspace: str, service: str, api_key: str):
        from tecton_client import TectonClient

        self.client = TectonClient(
            url, api_key=api_key, default_workspace_name=workspace
        )
        self.service = service

    def _get_feature_value(
        self, name: str, key_map: Dict[str, Any], request_map: Dict[str, Any]
    ):
        gf = self.client.get_features(
            feature_service_name=self.service + "_" + name,
            join_key_map=key_map,
            request_context_map={
                "name": name,
                "input": json.dumps(request_map),
            },
        )
        resp = json.loads(gf.get_features_dict()[name + ".output"])
        if "error" in resp:
            raise Exception(resp["error"])
        return resp["result"]


class _AgentClientLocal(AgentClient):
    def __init__(self, service: AgentService):
        self.service = service
        self.tool_map = {tool.name: tool for tool in service.online_fvs}

    def _get_feature_value(
        self, name: str, key_map: Dict[str, Any], request_map: Dict[str, Any]
    ):
        fv: RealtimeFeatureView = self.tool_map[name]
        if not fv._is_valid:
            fv.validate()
        res = dict(key_map)
        res.update(
            {
                "name": name,
                "input": json.dumps(request_map),
            }
        )
        if len(fv.sources) > 1:
            bfv: BatchFeatureView = fv.sources[1].feature_definition
            res[bfv.get_timestamp_field()] = datetime.now()
        odf = fv.get_features_for_events(pd.DataFrame([res])).to_pandas()
        resp = json.loads(odf[name + "__output"].iloc[0])
        if "error" in resp:
            raise Exception(resp["error"])
        return resp["result"]


class Agent:
    def __init__(self, client: AgentClient, llm, system_prompt=None) -> None:
        self.client = client
        self.llm = llm
        self._system_prompt = system_prompt

    def __call__(self, question, history=None, context=None) -> str:
        from langchain.agents import AgentExecutor, create_openai_tools_agent
        from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

        history = history or []
        context = context or {}
        history = self._add_sys_prompt(history, context)
        messages = history + [("human", question)]
        tools = self.client.to_lc_tools()
        if len(tools) == 0:
            return self.llm.invoke(messages).content
        else:
            prompt = ChatPromptTemplate.from_messages(
                [
                    MessagesPlaceholder("messages"),
                    MessagesPlaceholder("agent_scratchpad"),
                ]
            )
            agent = create_openai_tools_agent(self.llm, tools, prompt)
            agent_executor = AgentExecutor(agent=agent, tools=tools)
            return agent_executor.invoke({"messages": messages})["output"]

    def _add_sys_prompt(self, history, context):
        if not self._system_prompt:
            return history
        name = self._system_prompt
        value = self.client.metastore.get(name)
        match = all(key in context for key in value.get("keys", [])) and all(
            key in context for key in value.get("args", [])
        )
        if not match:
            raise ValueError(
                f"Prompt {name} is required, but context does not have all required keys."
            )
        sys_prompt = ("system", self.client.invoke_prompt(name, **context))
        history.insert(0, sys_prompt)
        return history
