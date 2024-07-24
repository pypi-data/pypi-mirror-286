import pandas as pd
from pytest import fixture
from tecton import RequestSource
from tecton.types import Field, String

from tecton_utils.ai import AgentClient, AgentService, prompt, tool
from tecton_utils.testing import mock_feature_view


@fixture
def mock_data():
    return pd.DataFrame(
        [
            {
                "user_id": "user1",
                "name": "Jim",
                "age": 30,
                "food_preference": "American",
            },
            {
                "user_id": "user2",
                "name": "John",
                "age": 40,
                "food_preference": "Italian",
            },
            {
                "user_id": "user3",
                "name": "Jane",
                "age": 50,
                "food_preference": "Chinese",
            },
        ]
    )


@fixture
def mock_agent_service(tecton_unit_test, mock_data):
    user_info = mock_feature_view(
        "user_info", mock_data, entity_keys=["user_id"], description="User info"
    )

    @prompt(sources=[user_info])
    def sys_prompt(location: str, user_info):
        name = user_info["name"]
        return f"You are serving {name} in {location}"

    request = RequestSource(schema=[Field("location", String)])

    @prompt(sources=[request, user_info])
    def sys_prompt_request_source(request, user_info):
        name = user_info["name"]
        location = request["location"]
        return f"You are serving {name} in {location}"

    @tool
    def get_tecton_employee_count() -> int:
        """
        Returns the number of employees in Tecton
        """
        return 110

    return AgentService(
        name="test",
        prompts=[sys_prompt, sys_prompt_request_source],
        tools=[user_info, get_tecton_employee_count],
    )


def test_agent(mock_agent_service):
    client = AgentClient.from_local(mock_agent_service)
    assert (
        client.invoke_prompt("sys_prompt", user_id="user3", location="Chicago")
        == "You are serving Jane in Chicago"
    )
    assert (
        client.invoke_prompt(
            "sys_prompt_request_source", user_id="user3", location="Chicago"
        )
        == "You are serving Jane in Chicago"
    )
    assert client.invoke_tool("user_info", user_id="user1") == {
        "name": "Jim",
        "age": 30,
        "food_preference": "American",
    }
    assert client.invoke_tool("get_tecton_employee_count") == 110
