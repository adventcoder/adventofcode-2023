from functools import wraps
from datetime import timezone, timedelta
import os
import re
import time
import traceback
import click
import requests
import cache

server_url = 'http://adventofcode.com/2023'
server_tz = timezone(timedelta(hours = -5), 'EST')

@cache.cached('inputs/{session}/day{day}.txt')
def fetch_input(day, session):
    res = requests.get(f'{server_url}/day/{day}/input', cookies={ 'session': session })
    res.raise_for_status()
    return res.text

@click.group()
def main():
    pass

def puzzle(*args, **kwargs):
    return lambda solver: make_puzzle_command(solver, *args, **kwargs)

def make_puzzle_command(solver, default_input=None):
    @main.command()
    @click.option('--session', envvar='ADVENTOFCODE_SESSION')
    @click.option('--input')
    @click.option('--input-file', type=click.File('r'))
    @click.pass_context
    @wraps(solver)
    def command(ctx, session, input, input_file, *args, **kwargs):
        if input is None:
            if input_file is not None:
                input = input_file.read()
            else:
                input = default_input or get_default_input(ctx, session)
        print(Answer(ctx.invoke, solver, input, *args, **kwargs))
    return command

def get_default_input(ctx, session):
    if session is None:
        ctx.fail('Fetching input from server requires --session parameter')
    return fetch_input(get_day(ctx), session)

def get_day(ctx):
    name, _ = os.path.splitext(os.path.basename(ctx.find_root().info_name))
    if match := re.match(r'day(\d+)', name):
        return int(match.group(1))
    ctx.fail('The module must be named like "dayN"')

class Answer:
    label = 'Answer:'

    def __init__(self, func, *args, **kwargs):
        start_time = time.perf_counter()
        try:
            self.value = func(*args, **kwargs)
            self.error = None
        except Exception as error:
            self.value = None
            self.error = error
        self.time = time.perf_counter() - start_time

    def __str__(self):
        text = self.answer_text()
        if self.error is not None:
            text = ''.join([text, '\n\n', *traceback.format_exception(type(self.error), self.error, self.error.__traceback__)])
        return text

    def answer_text(self):
        chunks = []
        if self.label is not None:
            chunks.append(self.label)
        chunks.append('N/A' if self.value is None else str(self.value))
        if self.time is not None:
            chunks.append(f'[{format_time(self.time)}]')
        return ' '.join(chunks)

def format_time(time):
    return '%.3f ms' % (time * 1000)
