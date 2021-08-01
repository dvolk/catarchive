import subprocess
import shlex
import time

import argh

import page
from db import *


def add_item(url, title, body_text, body):
    new_item = Item(
        title=title, url=url, content=body_text, added_epochtime=int(time.time())
    )
    new_item.content_html.put(body)
    new_item.save()


def add_from_xclip():
    url = subprocess.check_output(shlex.split("xclip -o")).decode()
    title, body_text, body = page.get_url_text(url)
    add_item(url, title, body_text, body)


def add_from_file(filepath):
    title, body_text, body = page.get_html_file_text(filepath)
    add_item(filepath, title, body_text, body)


if __name__ == "__main__":
    argh.dispatch_commands([add_from_xclip, add_from_file])
