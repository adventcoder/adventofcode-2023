from functools import wraps
from datetime import timezone, timedelta
import os
import re
import time
import traceback
import inspect

import click
import requests

import cache

server_url = 'http://adventofcode.com/2023'
server_tz = timezone(timedelta(hours = -5), 'EST')

@click.group()
def main():
    pass

def puzzle(*args, **kwargs):
    def wrap(solver):
        @main.command(*args, **kwargs)
        @click.option('--session', envvar='ADVENTOFCODE_SESSION')
        @click.option('--input')
        @click.option('--input-file', type=click.File('r'))
        @click.pass_context
        @wraps(solver)
        def subcommand(ctx, session, input, input_file, *args, **kwargs):
            if input is None and input_file is not None:
                input = input_file.read()
            if input is None:
                input = getattr(inspect.getmodule(solver), 'input', None)
            if input is None:
                if session is None:
                    ctx.fail('Fetching input from server requires --session parameter')
                input = fetch_input(session, get_day(solver))
            print(Answer(ctx.invoke, solver, input, *args, **kwargs))
        return subcommand
    return wrap

def get_day(solver):
    mod = inspect.getmodule(solver)
    day = getattr(mod, 'day', None)
    if day is None:
        day = guess_day(mod.__file__)
    return day

def guess_day(path):
    return int(re.search(r'\d+', os.path.basename(path)).group())

def fetch_input(session, day):
    def get_from_server():
        res = requests.get(f'{server_url}/day/{day}/input', cookies={ 'session': session })
        res.raise_for_status()
        return res.text
    return cache.cache(f'inputs/{session[:12]}/day{day}.txt', get_from_server)

class Answer:
    label = 'Answer:'

    def __init__(self, solver, *args, **kwargs):
        start_time = time.perf_counter()
        try:
            self.value = solver(*args, **kwargs)
            self.error = None
        except Exception as error:
            self.value = None
            self.error = error
        self.time = time.perf_counter() - start_time

    def __str__(self):
        lines = [self.answer_line() + '\n']
        if self.error is not None:
            lines.append('\n')
            lines.extend(traceback.format_exception(type(self.error), self.error, self.error.__traceback__))
        return ''.join(lines)

    def answer_line(self):
        chunks = [self.label]
        if self.value is None:
            chunks.append('N/A')
            if self.error is not None:
                chunks.append('(Error)')
        else:
            chunks.append(str(self.value))
        if self.time is not None:
            chunks.append(f'[{format_time(self.time)}]')
        return ' '.join(chunks)

def format_time(time):
    return '%.3f ms' % (time * 1000)
