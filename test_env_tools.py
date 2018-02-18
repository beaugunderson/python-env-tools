import os

from env_tools import apply_env, env_to_bool, get_enforcement_context, load_env


def assert_env(env):
    """
    Assert on everything in ./.env.
    """
    assert 'STRING' in env
    assert 'QUOTED_STRING_1' in env
    assert 'QUOTED_STRING_2' in env
    assert 'QUOTED_STRING_3' in env
    assert 'QUOTED_STRING_4' in env
    assert 'NUMBER' in env
    assert 'BOOLEAN_TRUE' in env
    assert 'BOOLEAN_FALSE' in env

    assert env['STRING'] == 'a string'
    assert env['QUOTED_STRING_1'] == 'single quoted'
    assert env['QUOTED_STRING_2'] == 'single quoted'
    assert env['QUOTED_STRING_3'] == 'double quoted'
    assert env['QUOTED_STRING_4'] == 'double quoted'
    assert env['NUMBER'] == '123456789'
    assert env['BOOLEAN_TRUE'] == 'true'
    assert env['BOOLEAN_FALSE'] == 'false'


def test_load_env_defaults():
    """
    Test loading the default .env file.
    """
    env = load_env()

    assert_env(env)


def test_apply_env_defaults():
    """
    Test loading the default .env file.
    """
    apply_env()

    assert_env(os.environ)


def test_env_to_bool():
    """
    Test that env_to_bool does what's expected.
    """
    os.environ['TEST_TRUE'] = 'true'
    os.environ['TEST_YES'] = 'yes'
    os.environ['TEST_1'] = '1'

    os.environ['TEST_FALSE'] = 'false'
    os.environ['TEST_NO'] = 'no'
    os.environ['TEST_0'] = '0'

    assert env_to_bool('TEST_TRUE') is True
    assert env_to_bool('TEST_YES') is True
    assert env_to_bool('TEST_1') is True

    assert env_to_bool('TEST_FALSE') is False
    assert env_to_bool('TEST_NO') is False
    assert env_to_bool('TEST_0') is False

    assert env_to_bool('DOES_NOT_EXIST', default=False) is False
    assert env_to_bool('DOES_NOT_EXIST', default=True) is True


def test_require_env():
    os.environ['TEST_IS_NOT_NULL'] = 'true'

    require_env, enforce_required_envs = get_enforcement_context()

    require_env('TEST_IS_NOT_NULL')
    require_env('FAILED_TEST_IS_NOT_SET')

    exception_happened = False

    try:
        enforce_required_envs()
    except ValueError as e:
        exception_happened = True
        exception_string = str(e)

        assert 'TEST_IS_NOT_NULL' not in exception_string
        assert 'FAILED_TEST_IS_NOT_SET' in exception_string

    assert exception_happened is True
