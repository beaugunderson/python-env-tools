## env-tools

A simple module for loading and applying .env files.

Works in Python 2 and Python 3.

### Running tests

```bash
$ py.test
```

Or, with `tox` (test with multiple Python versions):

```bash
$ tox
```

### Example

#### .env

```bash
VARIABLE_A=123
VARIABLE_B="testing, testing"
```

#### example.py

```python
import os

from env_tools import apply_env

# loads '.env' by default, to load another file use
# apply_env(load_env('filename'))
apply_env()

assert os.environ['VARIABLE_A'] == '123'
assert os.environ['VARIABLE_B'] == 'testing, testing'
```
