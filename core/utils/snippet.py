# _*_ coding:UTF-8 _*_
import os
import sys
import threading
import time
from functools import wraps
from six import string_types
from six.moves import queue

def split_cmd(cmds):
    """
    Split the commands to the list for subprocess

    Args:
        cmds: command(s)

    Returns:
        array commands

    """
    # cmds = shlex.split(cmds)  # disable auto removing \ on windows
    return cmds.split() if isinstance(cmds, string_types) else list(cmds)


def get_std_encoding(stream):
    """
    Get encoding of the stream

    Args:
        stream: stream

    Returns:
        encoding or file system encoding

    """
    return getattr(stream, "encoding", None) or sys.getfilesystemencoding()


CLEANUP_CALLS = queue.Queue()
IS_EXITING = False


def reg_cleanup(func, *args, **kwargs):
    """
    Clean the register for given function

    Args:
        func: function name
        *args: optional argument
        **kwargs: optional arguments

    Returns:
        None

    """
    CLEANUP_CALLS.put((func, args, kwargs))


def _cleanup():
    # cleanup together to prevent atexit thread issue
    while not CLEANUP_CALLS.empty():
        (func, args, kwargs) = CLEANUP_CALLS.get()
        func(*args, **kwargs)


# atexit.register(_cleanup)

_shutdown = threading._shutdown


def exitfunc():
    global IS_EXITING
    IS_EXITING = True
    _cleanup()
    _shutdown()


def is_exiting():
    return IS_EXITING


# use threading._shutdown to exec cleanup when main thread exit
# atexit exec after all thread exit, which needs to cooperate with daemon thread.
# daemon thread is evil, which abruptly exit causing unexpected error
threading._shutdown = exitfunc


def on_method_ready(method_name):
    """
    Wrapper for lazy initialization of some instance methods

    Args:
        method_name: instance method name

    Returns:
        wrapper

    """
    def wrapper(func):
        @wraps(func)
        def ready_func(inst, *args, **kwargs):
            key = "_%s_ready" % method_name
            if not getattr(inst, key, None):
                method = getattr(inst, method_name)
                method()
                setattr(inst, key, True)
            return func(inst, *args, **kwargs)
        return ready_func
    return wrapper


def ready_method(func):
    @wraps(func)
    def wrapper(inst, *args, **kwargs):
        ret = func(inst, *args, **kwargs)
        key = "_%s_ready" % func.__name__
        if not getattr(inst, key, None):
            setattr(inst, key, True)
        return ret
    return wrapper

def retries(max_tries, delay=1, backoff=2, exceptions=(Exception,), hook=None):
    """
    Function decorator implementing logic to recover from fatal errors. If a function fails to call due to any
    fatal error, the decoration tries to call it again after given delay time.

    The call delay time is counted as follows:
    delay * backoff * number of attempts to call the function after its failure

    It is possible to specify the custom tuple of exception classes within the 'exceptions' parameter. Only if such
    exception is detected, the function retries to call itself again.

    It is also possible to specify a hook function (with number of remaining re-tries and exception instance) which
    will be called prior the retrying attempt. Using the hook function gives the possibility to log the failure.
    Hook function is not called after failures or when no attempts left.

    Args:
        max_tries: maximum number of attempts to call the function, the decorator will call the function up
                   to max_tries, if all attempts fails, then the exception is risen
        delay: parameter to count the sleep time
        backoff: parameter to count the sleep time
        exceptions: A tuple of exception classes; default (Exception,)
        hook: A function with the signature myhook(tries_remaining, exception);
              default value is None

    Raises:
        Exception class and subclasses by default

    Returns:
        wrapper

    """
    def dec(func):
        def f2(*args, **kwargs):
            mydelay = delay
            tries = range(max_tries)
            # support Python conver range obj to list obj
            tries = list(tries)

            tries.reverse()
            for tries_remaining in tries:
                try:
                   return func(*args, **kwargs)
                except exceptions as e:
                    if tries_remaining > 0:
                        if hook is not None:
                            hook(tries_remaining, e, mydelay)
                        time.sleep(mydelay)
                        mydelay = mydelay * backoff
                    else:
                        raise
                else:
                    break
        return f2
    return dec
