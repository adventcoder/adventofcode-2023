from functools import wraps
import os
import warnings
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
    try:
        path = os.path.join(dirname, subpath)
        if os.path.exists(path):
            with open(path, 'r') as file:
                return file.read()
    except Exception:
        warnings.warn(f'cache read failed: {subpath}')

def write(subpath, text):
    try:
        path = os.path.join(dirname, subpath)
        os.makedirs(os.path.dirname(path))
        with open(path, 'w') as file:
            return file.write(text)
    except Exception:
        warnings.warn(f'cache write failed: {subpath}')
        delete(subpath)

def delete(subpath):
    try:
        path = os.path.join(dirname, subpath)
        if os.path.exists(path):
            os.remove(path)
    except Exception:
        warnings.warn(f'cache delete failed: {subpath}')
