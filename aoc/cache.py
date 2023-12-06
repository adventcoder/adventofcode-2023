from functools import wraps
import os
import logging
import inspect

dirname = '__cache__'

def cached(subpath_spec):
    def wrap(func):
        @wraps(func)
        def new_func(*args, **kwargs):
            subpath = subpath_spec.format(**inspect.getcallargs(func, *args, **kwargs))
            return cache(subpath, lambda: func(*args, **kwargs))
        return new_func
    return wrap

def cache(subpath, func):
    text = read(subpath)
    if text is None:
        text = func()
        write(subpath, text)
    return text

def read(subpath):
    path = os.path.join(dirname, subpath)
    try:
        if os.path.exists(path):
            with open(path, 'r') as file:
                return file.read()
    except Exception as err:
        logging.warning('cache read failed: %s', path, exc_info=err)

def write(subpath, text):
    path = os.path.join(dirname, subpath)
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as file:
            return file.write(text)
    except Exception as err:
        logging.warning('cache write failed: %s', path, exc_info=err)
        delete(path)

def delete(subpath):
    path = os.path.join(dirname, subpath)
    try:
        if os.path.exists(path):
            os.remove(path)
    except Exception as err:
        logging.warning('cache delete failed: %s', path, exc_info=err)
