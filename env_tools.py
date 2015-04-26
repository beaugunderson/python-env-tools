import io
import os

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
        env = load_env()

    os.environ.update(env)
