import json
from unittest import mock

import pytest
from pydantic import ValidationError

from pydantic_settings_aws import aws

from .aws_mocks import (
    TARGET_SECRET_CONTENT,
    TARGET_SECRETS_BOTO3_CLIENT,
    TARGET_SECRETS_CLIENT,
    TARGET_SESSION,
    TARGET_SSM_CLIENT,
    BaseSettingsMock,
    mock_create_client,
    mock_secrets_content_empty,
    mock_secrets_content_invalid_json,
    mock_ssm,
)
from .boto3_mocks import SessionMock


@mock.patch(TARGET_SSM_CLIENT, mock_ssm)
def test_get_ssm_content_must_return_parameter_content_if_annotated_with_parameter_name(*args):
    settings = BaseSettingsMock()
    settings.model_config = {"aws_region": "region", "aws_profile": "profile"}
    parameter_value = aws.get_ssm_content(settings, "field", "my/parameter/name")

    assert parameter_value is not None
    assert isinstance(parameter_value, str)


@mock.patch(TARGET_SSM_CLIENT, mock_ssm)
def test_get_ssm_content_must_return_parameter_content_if_annotated_with_dict_args(*args):
    settings = BaseSettingsMock()
    settings.model_config = {"aws_region": "region", "aws_profile": "profile"}
    parameter_value = aws.get_ssm_content(settings, "field", {"ssm": "my/parameter/name"})

    assert parameter_value is not None
    assert isinstance(parameter_value, str)


@mock.patch(TARGET_SSM_CLIENT, mock_ssm)
def test_get_ssm_content_must_use_client_if_present_in_metadata(*args):
    settings = BaseSettingsMock()
    settings.model_config = {"aws_region": "region", "aws_profile": "profile"}
    parameter_value = aws.get_ssm_content(settings, "field", {"ssm": "my/parameter/name", "ssm_client": mock_ssm()})

    assert parameter_value is not None
    assert isinstance(parameter_value, str)


@mock.patch(TARGET_SSM_CLIENT, mock_ssm)
def test_get_ssm_content_must_use_field_name_if_ssm_name_not_in_metadata(*args):
    settings = BaseSettingsMock()
    settings.model_config = {"aws_region": "region", "aws_profile": "profile"}
    parameter_value = aws.get_ssm_content(settings, "field", None)

    assert parameter_value is not None
    assert isinstance(parameter_value, str)


@mock.patch(TARGET_SESSION, SessionMock)
def test_create_ssm_client(*args):
    settings = BaseSettingsMock()
    settings.model_config = {"aws_region": "region", "aws_profile": "profile"}
    client = aws._create_ssm_client(settings)

    assert client is not None


@mock.patch(TARGET_SSM_CLIENT, mock_create_client)
def test_get_ssm_boto3_client_must_create_a_client_if_its_not_given(*args):
    settings = BaseSettingsMock()
    settings.model_config = {}
    client = aws._get_ssm_boto3_client(settings)

    assert client is not None


@mock.patch(TARGET_SESSION, SessionMock)
def test_create_secrets_client(*args):
    settings = BaseSettingsMock()
    settings.model_config = {"aws_region": "region", "aws_profile": "profile"}
    client = aws._create_secrets_client(settings)

    assert client is not None


@mock.patch(TARGET_SECRETS_CLIENT, mock_create_client)
def test_get_secrets_boto3_client_must_create_a_client_if_its_not_given(*args):
    settings = BaseSettingsMock()
    settings.model_config = {}
    client = aws._get_secrets_boto3_client(settings)

    assert client is not None


@mock.patch(TARGET_SECRETS_BOTO3_CLIENT, mock_secrets_content_empty)
@mock.patch(TARGET_SECRET_CONTENT, lambda *args: None)
def test_get_secrets_content_must_raise_value_error_if_secrets_content_is_none(
    *args,
):
    settings = BaseSettingsMock()
    settings.model_config = {
        "secrets_name": "secrets/name",
        "aws_region": "region",
        "aws_profile": "profile",
    }

    with pytest.raises(ValueError):
        aws.get_secrets_content(settings)


@mock.patch(TARGET_SECRETS_BOTO3_CLIENT, mock_secrets_content_invalid_json)
def test_should_not_obfuscate_json_error_in_case_of_invalid_secrets(*args):
    settings = BaseSettingsMock()
    settings.model_config = {
        "secrets_name": "secrets/name",
        "aws_region": "region",
        "aws_profile": "profile",
    }

    with pytest.raises(json.decoder.JSONDecodeError):
        aws.get_secrets_content(settings)


def test_get_secrets_content_must_get_binary_content_if_string_is_not_set(*args):
    content = {
        "SecretBinary": json.dumps({"username": "admin"}).encode("utf-8")
    }
    secret_content = aws._get_secrets_content(content)

    assert isinstance(secret_content, str)


def test_get_secrets_content_must_not_hide_decode_error_if_not_binary_in_secret_binary(*args):
    content = {
        "SecretBinary": json.dumps({"username": "admin"})
    }

    with pytest.raises(AttributeError):
        aws._get_secrets_content(content)


def test_get_secrets_content_must_return_none_if_neither_string_nor_binary_are_present(*args):
    secret_content = aws._get_secrets_content({})

    assert secret_content is None


def test_get_secrets_content_must_return_none_if_binary_is_present_but_none(*args):
    content = {
        "SecretBinary": None
    }
    secret_content = aws._get_secrets_content(content)

    assert secret_content is None


def test_get_secrets_args_must_not_shadow_pydantic_validation_if_required_args_are_not_present(*args):
    settings = BaseSettingsMock()
    settings.model_config = {}

    with pytest.raises(ValidationError):
        aws._get_secrets_args(settings)
