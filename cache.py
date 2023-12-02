from functools import wraps
import os
import warnings
import inspect

root = '.'

def cached(subpath_spec, func=None):
    if func is None:
        return lambda func: cached(subpath_spec, func)
    @wraps(func)
    def cached_func(*args, **kwargs):
        subpath = subpath_spec.format(**inspect.getcallargs(func, *args, **kwargs))
        return cache(subpath, lambda: func(*args, **kwargs))
    return cached_func

def cache(subpath, func):
    text = read(subpath)
    if text is None:
        text = func()
        write(subpath, text)
    return text

def read(subpath):
    try:
        path = os.path.join(root, subpath)
        if os.path.exists(path):
            with open(path, 'r') as file:
                return file.read()
    except Exception:
        warnings.warn(f'cache read failed: {subpath}')

def write(subpath, text):
    try:
        make_dirs(os.path.dirname(subpath))
        path = os.path.join(root, subpath)
        with open(path, 'w') as file:
            return file.write(text)
    except Exception:
        warnings.warn(f'cache write failed: {subpath}')
        delete(subpath)

def make_dirs(subpath):
    if subpath:
        path = os.path.join(root, subpath)
        if not os.path.exists(path):
            make_dirs(os.path.dirname(subpath))
            os.mkdir(path)

def delete(subpath):
    try:
        path = os.path.join(root, subpath)
        if os.path.exists(path):
            os.remove(path)
    except Exception:
        warnings.warn(f'cache delete failed: {subpath}')
