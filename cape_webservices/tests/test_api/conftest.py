# Copyright 2018 BLEMUNDSBURY AI LIMITED
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from cape.client import CapeClient, CapeException
import pytest
from cape_webservices.tests.tests_settings import URL
from cape_webservices import webservices_settings

API_URL = URL + '/api'


def _delete_user(login):
    client = CapeClient(API_URL)
    response = client._raw_api_call('user/delete-user', parameters={'userId': login,
                                                                    'superAdminToken': webservices_settings.SUPER_ADMIN_TOKEN})
    print("Deletion", response.json())


def _init_user(login, password, user_attributes):
    client = CapeClient(API_URL)
    try:
        _delete_user(login)
    except CapeException:
        pass
    new_user_parameters = {'userId': login,
                           'password': password,
                           'superAdminToken': webservices_settings.SUPER_ADMIN_TOKEN}
    new_user_parameters.update(user_attributes)
    url = 'user/create-user?'
    for k, v in new_user_parameters.items():
        url += "%s=%s&" % (k, v)
    response = client._raw_api_call(url)
    print(response.json())
    assert response.status_code == 200
    client.login(login, password)
    return client


@pytest.fixture(scope="session")
def cape_client():
    client = _init_user('testuser', 'testpass', {})
    yield client
    client.logout()


@pytest.fixture(scope="session")
def cape_client_answer():
    client = _init_user('testuser_answer', 'testpass_answer', {})
    yield client
    client.logout()
