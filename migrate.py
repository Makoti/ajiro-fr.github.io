#!/usr/bin/python

import os
import shutil
import string
import fnmatch

BASE='.'
TARGET='content'


def list_items(directory, pattern="*.md"):
    for root, dirs, files in os.walk(os.path.join(BASE, directory)):
        for f in files:
            if fnmatch.fnmatch(f, pattern):
                yield (f, os.path.join(root, f))


def nameof(filename):
    return os.path.splitext(filename)[0]


def extensionof(filename):
    return os.path.splitext(filename)[1]


def new_article_name(name):
    return name.replace('.', '_')


def ensure_directory(path):
    try:
        os.makedirs(path)
    except OSError:
        pass


def read_file(path):
    with open(path, 'r') as f:
        return f.read()


def write_file(path, content):
    with open(path, 'w') as f:
        f.write(str(content))


def no_translation(name, content):
    return content

def remove_lines(*lines):
    def process(name, content):
        result = []
        for line in content.split('\n'):
            if not line in lines:
                result.append(line)
        return string.join(result, '\n')
    return process


def copy_illustration(path, name):
    def process(item, source, target):
        shutil.copyfile(
            os.path.join(path, nameof(item) + '.jpg'),
            os.path.join(target, name + '.jpg'))
    return process


def process_file_content(translator):
    def process(item, source, target):
        write_file(
            os.path.join(target, 'index.md'),
            translator(
                nameof(item),
                read_file(source))
        )
    return process


def translate(items, destination, translators):
    for item, source in items:
        target = os.path.join(TARGET, destination, nameof(item))
        ensure_directory(target)
        for translator in translators:
            translator(item, source, target)


translate(
    items=list_items('_books'),
    destination='books',
    translators=[
        process_file_content(remove_lines('layout: book')),
        copy_illustration('assets/books', 'cover')])

translate(
    items=list_items('_games'),
    destination='games',
    translators=[
        process_file_content(remove_lines('layout: game'))])