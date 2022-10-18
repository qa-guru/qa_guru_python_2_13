import requests
from requests import Response
from voluptuous import Schema, PREVENT_EXTRA, Required, Optional, ALLOW_EXTRA
from pytest_voluptuous import S

from utils.base_session import reqres_session

create_user_schema = Schema(
    {
        "name": str,
        "job": str,
        "id": str,
        "createdAt": str,
    },
    required=True,
    extra=PREVENT_EXTRA,
)


def test_create_user_schema():
    name = "morpheus_2"
    job = "leader"

    result = requests.post(
        url="https://reqres.in/api/users",
        json={"name": name, "job": job}
    )

    assert result.status_code == 201
    assert result.json()['name'] == name
    assert result.json()['job'] == job
    assert isinstance(result.json()['id'], str)
    assert result.json() == S(create_user_schema)


def test_create_user_schema_v2():
    name = "morpheus_2"
    job = "leader"

    result: Response = reqres_session().post(
        url="/api/users",
        json={"name": name, "job": job}
    )
    print(result.text)
    assert result.status_code == 201
    assert result.json()['name'] == name
    assert result.json()['job'] == job
    assert isinstance(result.json()['id'], str)
    assert result.json() == S(create_user_schema)