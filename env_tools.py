import io
import os

from six import iteritems
from tini import StripQuotesInterpolation, Tini


def get_enforcement_context():
    context = {}

    def require_env(name, default=None):
        value = os.getenv(name, default)
        context[name] = value

        return value

    def enforce_required_envs():
        missing_envs = [name for name, value in iteritems(context) if value is None]

        if missing_envs:
            missing_env_list = "\n".join(missing_envs)

            raise ValueError(
                "Required environment variables missing:\n{}".format(missing_env_list)
            )

    return require_env, enforce_required_envs


class NamedStringIO(io.StringIO):
    """
    StringIO with a `name` property.
    """

    def __init__(self, string, name=None):
        self.name = name

        super(NamedStringIO, self).__init__(string)


def load_env(filename=".env"):
    """
    Read the `.env` file and return it.
    """
    env = "[root]\n" + io.open(filename, "r").read()

    config = Tini(
        f=NamedStringIO(env, filename), interpolation=StripQuotesInterpolation()
    )

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


def strtobool(val):
    """
    Based on strtobools from distutils.util.

    Convert a string representation of truth to true (1) or false (0).

    True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values
    are 'n', 'no', 'f', 'false', 'off', and '0'.  Raises ValueError if
    'val' is anything else.
    """
    val = val.lower()

    if val in ("y", "yes", "t", "true", "on", "1"):
        return True
    elif val in ("n", "no", "f", "false", "off", "0"):
        return False
    else:
        raise ValueError(f"Invalid truth value {val!r}")


def env_to_bool(env, default="false"):
    """
    Convert a string like 'true' or 'false' to a bool.
    """
    return strtobool(os.getenv(env, str(default)))
