import io
import os

from distutils import util  # pylint: disable=no-name-in-module

from six import iteritems
from tini import Tini, StripQuotesInterpolation


def get_enforcement_context():
    context = {}

    def require_env(name, default=None):
        value = os.getenv(name, default)
        context[name] = value

        return value

    def enforce_required_envs():
        missing_envs = [name for name, value in iteritems(context)
                        if value is None]

        if missing_envs:
            missing_env_list = '\n'.join(missing_envs)

            raise ValueError(
                'Required environment variables missing:\n{}'.format(
                    missing_env_list))

    return require_env, enforce_required_envs


class NamedStringIO(io.StringIO):
    """
    StringIO with a `name` property.
    """

    def __init__(self, string, name=None):
        self.name = name

        super(NamedStringIO, self).__init__(string)


def load_env(filename='.env'):
    """
    Read the `.env` file and return it.
    """
    env = '[root]\n' + io.open(filename, 'r').read()

    config = Tini(f=NamedStringIO(env, filename),
                  interpolation=StripQuotesInterpolation())

    return config.root


def apply_env(env=None):
    """
    Apply the given env to os.environ just like using `foreman run` would.
    """
    if not env:
        # don't raise when the default .env is missing
        try:
            env = load_env()
        except IOError:
            return

    os.environ.update(env)


def env_to_bool(env, default='false'):
    """
    Convert a string like 'true' or 'false' to a bool.
    """
    return bool(util.strtobool(os.getenv(env, str(default))))
