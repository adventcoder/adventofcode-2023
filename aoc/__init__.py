from functools import wraps
import re
import os
import time
import traceback
import click
from . import server

@click.group()
def main():
    pass

def command(*args, **kwargs):
    return main.command(*args, **kwargs)

def puzzle(input=None):
    def wrap(func):
        @command()
        @pass_input(input)
        # @click.option('--submit')
        # @click.option('--check')
        @wraps(func)
        def new_func(*args, **kwargs):
            print(Answer(func, *args, **kwargs))
        return new_func
    return wrap

def pass_input(input=None):
    local_input = input
    def wrap(func):
        @click.option('--session', envvar='ADVENTOFCODE_SESSION')
        @click.option('--input')
        @click.option('--input-file', type=click.File('r'))
        # @click.option('--wait-for-input')
        @click.pass_context
        @wraps(func)
        def new_func(ctx, session, input, input_file, *args, **kwargs):
            if input is None:
                if input_file is not None:
                    input = input_file.read()
                else:
                    input = local_input or get_server_input(ctx, session)
            return ctx.invoke(func, input, *args, **kwargs)
        return new_func
    return wrap

def get_server_input(ctx, session):
    day = find_day(ctx)
    if day > server.last_available_day():
        ctx.fail(f'Input for day {day} is not available yet')
    if session is None:
        ctx.fail('Could not determine sesssion from environment')
    return server.fetch_input(day, session)


def find_day(ctx):
    root = ctx.find_root()
    script_name, _ = os.path.splitext(os.path.basename(root.info_name))
    if match := re.match(r'day(\d+)', script_name):
        return int(match.group(1))
    ctx.fail('Day could not be found')

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
