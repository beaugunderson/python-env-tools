import io
import os

from distutils import util  # pylint: disable=no-name-in-module

from tini import Tini, StripQuotesInterpolation


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
