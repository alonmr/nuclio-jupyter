# Copyright 2018 Iguazio
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest

from nuclio import config


def get_env_var_from_list_by_key(env, key):
    for env_var in env:
        if env_var['name'] == key:
            return env_var
    return None


def test_update_env_var_missing_value():
    config_dict = {'spec': {'env': []}}
    with pytest.raises(Exception):
        config.update_env_var(config_dict, 'name')


def test_update_env_var_existing_key():
    config_dict = {'spec': {'env': [{'name': 'key', 'value': 'value1'}, {'name': 'key2', 'value': 'value1'}]}}
    config.update_env_var(config_dict, 'key', value='value2')
    assert get_env_var_from_list_by_key(config_dict['spec']['env'], 'key')['value'] == 'value2',\
        'env var was not updated'

    value_from = {"secretKeyRef": {"name": "secret1", "key": "secret-key1"}}
    config.update_env_var(config_dict, 'key2', value_from=value_from)
    assert get_env_var_from_list_by_key(config_dict['spec']['env'], 'key2')['valueFrom'] == value_from,\
        'env var was not updated'


def test_update_env_var_new_key():
    config_dict = {'spec': {'env': []}}
    config.update_env_var(config_dict, 'key', value='value2')
    assert get_env_var_from_list_by_key(config_dict['spec']['env'], 'key')['value'] == 'value2',\
        'env var was not updated'

    value_from = {"secretKeyRef": {"name": "secret1", "key": "secret-key1"}}
    config.update_env_var(config_dict, 'key2', value_from=value_from)
    assert get_env_var_from_list_by_key(config_dict['spec']['env'], 'key2')['valueFrom'] == value_from,\
        'env var was not updated'


def test_set_secrets_dict():
    config_dict = {'spec': {'env': []}}
    secrets = {
        'name1': {"secret_key_ref": {"name": "secret1", "key": "secret-key1"}},
        'name2': {"secret_key_ref": {"name": "secret2", "key": "secret-key2"}},
    }
    config.set_secrets_dict(config_dict, secrets)

    # verify changed to CamelCase
    expected_value_from1 = {"secretKeyRef": {"name": "secret1", "key": "secret-key1"}}
    expected_value_from2 = {"secretKeyRef": {"name": "secret2", "key": "secret-key2"}}
    assert get_env_var_from_list_by_key(config_dict['spec']['env'], 'name1')['valueFrom'] == expected_value_from1,\
        'unexpected value from'
    assert get_env_var_from_list_by_key(config_dict['spec']['env'], 'name2')['valueFrom'] == expected_value_from2,\
        'unexpected value from'


def test_set_secrets_dict_missing_entries():
    config_dict = {'spec': {'env': []}}
    secrets = {
        'name1': {"secret_key_ref": {"key": "secret-key1"}},
        'name2': {"secret_key_ref": {"name": "secret2"}},
    }
    with pytest.raises(Exception) as exc:
        config.set_secrets_dict(config_dict, secrets)
        value_from = secrets['name1']
        assert str(exc) == f'Env variable from secret must not be nameless nor keyless: {value_from}'

    del secrets['name1']
    with pytest.raises(Exception) as exc:
        config.set_secrets_dict(config_dict, secrets)
        value_from = secrets['name2']
        assert str(exc) == f'Env variable from secret must not be nameless nor keyless: {value_from}'
