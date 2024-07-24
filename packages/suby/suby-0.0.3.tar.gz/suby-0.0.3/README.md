![logo](https://raw.githubusercontent.com/pomponchik/suby/develop/docs/assets/logo_5.svg)

[![Downloads](https://static.pepy.tech/badge/suby/month)](https://pepy.tech/project/suby)
[![Downloads](https://static.pepy.tech/badge/suby)](https://pepy.tech/project/suby)
[![codecov](https://codecov.io/gh/pomponchik/suby/graph/badge.svg?token=IyYI7IaSet)](https://codecov.io/gh/pomponchik/suby)
[![Lines of code](https://sloc.xyz/github/pomponchik/suby/?category=code)](https://github.com/boyter/scc/)
[![Hits-of-Code](https://hitsofcode.com/github/pomponchik/suby?branch=main)](https://hitsofcode.com/github/pomponchik/suby/view?branch=main)
[![Test-Package](https://github.com/pomponchik/suby/actions/workflows/tests_and_coverage.yml/badge.svg)](https://github.com/pomponchik/suby/actions/workflows/tests_and_coverage.yml)
[![Python versions](https://img.shields.io/pypi/pyversions/suby.svg)](https://pypi.python.org/pypi/suby)
[![PyPI version](https://badge.fury.io/py/suby.svg)](https://badge.fury.io/py/suby)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)


Here is a small wrapper around the [subprocesses](https://docs.python.org/3/library/subprocess.html). You can find many similar wrappers, but this particular one differs from the others in the following parameters:

- Beautiful minimalistic call syntax.
- Ability to specify your callbacks to catch `stdout` and `stderr`.
- Support for [cancellation tokens](https://github.com/pomponchik/cantok).
- You can set timeouts for subprocesses.
- Logging of command execution.


## Table of contents

- [**Quick start**](#quick-start)
- [**Run subprocess and look at the result**](#run-subprocess-and-look-at-the-result)
- [**Output**](#output)
- [**Logging**](#logging)
- [**Exceptions**](#exceptions)
- [**Working with Cancellation Tokens**](#working-with-cancellation-tokens)
- [**Timeouts**](#timeouts)


## Quick start

Install it:

```bash
pip install suby
```

And use:

```python
import suby

suby('python', '-c', 'print("hello, world!")')
# > hello, world!
```


## Run subprocess and look at the result

The `suby` module is a callable object and can be imported like this:

```python
import suby
```

If you use static type checking and get an error that it is impossible to call the module, use a more detailed import form - functionally, these two import ways are identical:

```python
from suby import suby
```

Let's try to call `suby`. You can use strings or [`pathlib.Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path) objects as positional arguments, but now we call it with only simple strings:

```python
result = suby('python', '-c', 'print("hello, world!")')
print(result)
# > SubprocessResult(id='e9f2d29acb4011ee8957320319d7541c', stdout='hello, world!\n', stderr='', returncode=0, killed_by_token=False)
```

We can see that it returns an object of the `SubprocessResult` class. It contains the following required fields:

- **id** - a unique string that allows you to distinguish one result of calling the same command from another.
- **stdout** - a string containing the entire buffered output of the command being run.
- **stderr** - a string containing the entire buffered stderr of the command being run.
- **returncode** - an integer indicating the return code of the subprocess. `0` means that the process was completed successfully, the other options usually indicate something bad.
- **killed_by_token** - a boolean flag indicating whether the subprocess was killed due to [token](https://cantok.readthedocs.io/en/latest/the_pattern/) cancellation.


## Output

By default, the `stdout` and `stderr` of the subprocess are forwarded to the `stdout` and `stderr` of the current process. The reading from the subprocess is continuous, and the output is every time a full line is read. For continuous reading from `stderr`, a separate thread is created in the main process, so that `stdout` and `stderr` are read independently.

You can override the output functions for `stdout` and `stderr`. To do this, you need to pass as arguments `stdout_callback` and `stderr_callback`, respectively, some functions that accept a string as an argument. For example, you can color the output (the code example uses the [`termcolor`](https://github.com/termcolor/termcolor) library):

```python
import suby
from termcolor import colored

def my_new_stdout(string: str) -> None:
    print(colored(string, 'red'), end='')

suby('python', '-c', 'print("hello, world!")', stdout_callback=my_new_stdout)
# > hello, world!
# You can't see it here, but believe me, if you repeat the code at home, the output in the console will be red!
```

You can also completely disable the output by passing `True` as the `catch_output` parameter:

```python
suby('python', '-c', 'print("hello, world!")', catch_output=True)
# There's nothing here.
```

If you specify `catch_output=True`, and at the same time redefine your functions for output, your functions will not be called either. In addition, `suby` always returns [the result](#run-subprocess-and-look-at-the-result) of executing the command, containing the full output. The `catch_output` argument can stop exactly the output, but it does not prevent the collection and buffering of the output.


## Logging

By default, `suby` does not log command execution. However, you can pass a logger object to the function, and in this case logs will be recorded at the start of the command execution and at the end of the execution:

```python
import logging
import suby

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
    ]
)

suby('python', '-c', 'pass', logger=logging.getLogger('logger_name'))
# > 2024-02-22 02:15:08,155 [INFO] The beginning of the execution of the command "python -c pass".
# > 2024-02-22 02:15:08,190 [INFO] The command "python -c pass" has been successfully executed.
```

The message about the start of the command execution is always done with the `INFO` [level](https://docs.python.org/3.8/library/logging.html#logging-levels). If the command is completed successfully, the end message will also be with the `INFO` level. And if not - `ERROR`:

```python
suby('python', '-c', 'raise ValueError', logger=logging.getLogger('logger_name'), catch_exceptions=True, catch_output=True)
# > 2024-02-22 02:20:25,549 [INFO] The beginning of the execution of the command "python -c "raise ValueError"".
# > 2024-02-22 02:20:25,590 [ERROR] Error when executing the command "python -c "raise ValueError"".
```

If you don't need these details, just don't pass the logger object.

If you still prefer logging, you can use any object that implements the [logger protocol](https://github.com/pomponchik/emptylog?tab=readme-ov-file#universal-logger-protocol) from the [`emptylog`](https://github.com/pomponchik/emptylog) library, including ones from third-party libraries.


## Exceptions

By default, `suby` raises exceptions in three cases:

1. If the command you are calling ended with a return code not equal to `0`. In this case, you will see an exception `suby.RunningCommandError`:

```python
import suby

try:
    suby('python', '-c', '1/0')
except suby.RunningCommandError as e:
    print(e)
    # > Error when executing the command "python -c 1/0".
```

2. If you passed a [cancellation token](https://cantok.readthedocs.io/en/latest/the_pattern/) when calling the command, and the token was canceled, an exception will be raised [corresponding to the type](https://cantok.readthedocs.io/en/latest/what_are_tokens/exceptions/) of canceled token. [This part of the functionality](#working-with-cancellation-tokens) is integrated with the [cantok](https://cantok.readthedocs.io/en/latest/) library, so we recommend that you familiarize yourself with it beforehand.

3. You have set a [timeout](#timeouts) for the operation and it has expired.

You can prevent `suby` from raising any exceptions. To do this, set the `catch_exceptions` parameter to `True`:

```python
result = suby('python', '-c', 'import time; time.sleep(10_000)', timeout=1, catch_exceptions=True)
print(result)
# > SubprocessResult(id='c9125b90d03111ee9660320319d7541c', stdout='', stderr='', returncode=-9, killed_by_token=True)
```

Keep in mind that the full result of the subprocess call can also be found through the `result` attribute of any raised exception:

```python
try:
    suby('python', '-c', 'import time; time.sleep(10_000)', timeout=1)
except suby.TimeoutCancellationError as e:
    print(e.result)
    # > SubprocessResult(id='a80dc26cd03211eea347320319d7541c', stdout='', stderr='', returncode=-9, killed_by_token=True)
```


## Working with Cancellation Tokens

`suby` is fully compatible with the [cancellation token pattern](https://cantok.readthedocs.io/en/latest/the_pattern/) and supports any token objects from the [`cantok`](https://github.com/pomponchik/cantok) library.

The essence of the pattern is that you can pass an object to `suby`, from which it can find out whether the operation still needs to be continued or not. If not, it kills the subprocess. This pattern can be especially useful in the case of commands that are executed for a long time or for an unpredictably long time. When the result becomes unnecessary, there is no point in sitting and waiting for the command to work out.

So, you can pass your cancellation tokens to `suby`. By default, canceling a token causes an exception to be raised:

```python
from random import randint
import suby
from cantok import ConditionToken

token = ConditionToken(lambda: randint(1, 1000) == 7)  # This token will be cancelled when a random unlikely event occurs.
suby('python', '-c', 'import time; time.sleep(10_000)', token=token)
# > cantok.errors.ConditionCancellationError: The cancellation condition was satisfied.
```

However, if you pass the `catch_exceptions=True` argument, the exception [will not be raised](#exceptions). Instead, you will get the [usual result](#run-subprocess-and-look-at-the-result) of calling `suby` with the `killed_by_token=True` flag:

```python
token = ConditionToken(lambda: randint(1, 1000) == 7)
print(suby('python', '-c', 'import time; time.sleep(10_000)', token=token, catch_exceptions=True))
# > SubprocessResult(id='e92ccd54d24b11ee8376320319d7541c', stdout='', stderr='', returncode=-9, killed_by_token=True)
```

"Under the hood" a separate thread is created to track the status of the token. When the token is canceled, the thread kills the subprocess.

## Timeouts

You can set a timeout for `suby`. It must be an integer greater than zero, which indicates the number of seconds that the subprocess can continue to run. If the timeout expires before the subprocess completes, an exception will be raised:

```python
import suby

suby('python', '-c', 'import time; time.sleep(10_000)', timeout=1)
# > cantok.errors.TimeoutCancellationError: The timeout of 1 seconds has expired.
```

To count the timeout, "under the hood" `suby` uses [`TimeoutToken`](https://cantok.readthedocs.io/en/latest/types_of_tokens/TimeoutToken/) from the [`cantok`](https://github.com/pomponchik/cantok) library.

The exception corresponding to this token was be reimported to `suby`:

```python
try:
    suby('python', '-c', 'import time; time.sleep(10_000)', timeout=1)
except suby.TimeoutCancellationError as e:  # As you can see, TimeoutCancellationError is available in the suby module.
    print(e)
    # > The timeout of 1 seconds has expired.
```

Just as with [regular cancellation tokens](#working-with-cancellation-tokens), you can prevent exceptions from being raised using the `catch_exceptions=True` argument:

```python
print(suby('python', '-c', 'import time; time.sleep(10_000)', timeout=1, catch_exceptions=True))
# > SubprocessResult(id='ea88c518d25011eeb25e320319d7541c', stdout='', stderr='', returncode=-9, killed_by_token=True)
```
