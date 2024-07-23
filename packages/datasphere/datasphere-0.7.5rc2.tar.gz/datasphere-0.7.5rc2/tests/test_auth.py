import re
from unittest.mock import Mock, call

import pytest

from datasphere.auth import create_iam_token, get_md
from yandex.cloud.iam.v1.iam_token_service_pb2 import CreateIamTokenRequest, CreateIamTokenResponse


def test_create_iam_token_with_sdk(mocker):
    def Create(req: CreateIamTokenRequest):  # noqa
        return CreateIamTokenResponse(iam_token=f'iam token for oauth token {req.yandex_passport_oauth_token}')

    stub = mocker.patch('datasphere.auth.IamTokenServiceStub')()
    stub.Create = Create

    assert create_iam_token('AQAD***') == 'iam token for oauth token AQAD***'


def test_create_iam_token_with_compute_metadata(requests_mock):
    requests_mock.get(
        'http://169.254.169.254/computeMetadata/v1/instance/service-accounts/default/token',
        json={'access_token': 'iam token from compute metadata'}
    )
    assert create_iam_token(None) == 'iam token from compute metadata'


def test_create_iam_token_with_yc(mocker):
    yc_process = Mock()
    yc_process.stdout = """

You are going to be authenticated via federation-id 'team.example.federation'.
Your federation authentication web site will be opened.
After your successful authentication, you will be redirected to cloud console'.

Press 'enter' to continue...
t1.9eudm***
    """

    mocker.patch('subprocess.run', return_value=yc_process)

    assert create_iam_token(None) == 't1.9eudm***'


def test_get_iam_token_from_env(mocker, caplog):
    mocker.patch.dict('os.environ', {'YC_IAM_TOKEN': 'iam token'})
    assert create_iam_token(None) == 'iam token'
    assert caplog.record_tuples == [
        (
            'datasphere.auth', 30,
            'iam token from env var is not refreshable, so it may expire over time',
        )
    ]


def test_error_no_yc(mocker, caplog):
    mocker.patch('subprocess.run', side_effect=FileNotFoundError)

    with pytest.raises(
            RuntimeError,
            match=re.escape('None of authorization methods=[OAUTH,COMPUTE_METADATA,YC_UTILITY] returned result'),
    ):
        create_iam_token(None)

    assert caplog.record_tuples == [
        (
            'datasphere.auth', 30,
            '`yc` utility was not found. See https://yandex.cloud/cli/ for instructions.',
        )
    ]


def test_iam_token_refresh(mocker):
    oauth_token = 'AQAD***'

    iam_tokens = ['iam_token_1', 'iam_token_2']
    iam_tokens_md = [('authorization', f'Bearer {iam_token}') for iam_token in iam_tokens]

    create_iam_token_stub = mocker.patch('datasphere.auth.create_iam_token')
    create_iam_token_stub.return_value = iam_tokens[0]

    md1 = get_md(oauth_token, None)
    md2 = get_md(oauth_token, None)

    create_iam_token_stub.assert_called_once_with(oauth_token, None)
    assert iam_tokens_md[0] in md1
    assert iam_tokens_md[0] in md2

    create_iam_token_stub.return_value = iam_tokens[1]

    iam_token_refresh_period = mocker.patch('datasphere.auth.iam_token_refresh_period')
    iam_token_refresh_period.__lt__.return_value = True

    md3 = get_md(oauth_token, None)

    create_iam_token_stub.assert_has_calls([call(oauth_token, None), call(oauth_token, None)])

    assert iam_tokens_md[1] in md3


def test_override_auth_methods(mocker):
    oauth = mocker.patch('datasphere.auth.create_iam_token_by_oauth_token')
    oauth.return_value = None
    md = mocker.patch('datasphere.auth.create_iam_token_with_compute_metadata')
    md.return_value = None
    yc = mocker.patch('datasphere.auth.create_iam_token_with_yc')
    yc.return_value = None

    # Default auth methods. None of them returned token, resulting in runtime error.
    with pytest.raises(
            RuntimeError,
            match=re.escape('None of authorization methods=[OAUTH,COMPUTE_METADATA,YC_UTILITY] returned result'),
    ):
        create_iam_token('oauth token', 'yc profile')

    oauth.assert_called_once_with(oauth_token='oauth token')
    md.assert_called_once()
    yc.assert_called_once_with(yc_profile='yc profile')

    # Metadata handler first returned something, it will be in result.
    md.return_value = 'md iam token'
    yc.return_value = 'yc iam token'

    assert create_iam_token(None) == 'md iam token'

    # We change order so yc result will be first.
    mocker.patch.dict('os.environ', {'YC_AUTH': 'oauth,yc,md'})

    assert create_iam_token(None) == 'yc iam token'

    # Now only oauth method left, which has no result.
    mocker.patch.dict('os.environ', {'YC_AUTH': 'oauth'})

    with pytest.raises(RuntimeError, match=re.escape('None of authorization methods=[OAUTH] returned result')):
        create_iam_token(None)
