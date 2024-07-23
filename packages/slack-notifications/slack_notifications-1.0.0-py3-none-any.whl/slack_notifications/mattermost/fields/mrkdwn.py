from typing import Iterable


def bold(text):
    return f'**{str(text)}**'


def italic(text):
    return f'*{str(text)}*'


def strike(text):
    return f'~~{str(text)}~~'


def code_block(text):
    return f'`{str(text)}`'


def multi_line_code_block(text, *, lang=''):
    return f'```{lang}\n{str(text)}\n```'


def block_quotes(text):
    return f'>{str(text)}'


def list_items(itr: Iterable):
    return ''.join([f'- {str(item)}' for item in itr]) + '\n'


def link(url, text):
    return f'[{str(text)}]({url})'


def user_mention(user_id):
    return f'@{user_id}'


def channel_mention(channel):
    return f'~{channel}'
