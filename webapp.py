import datetime as dt
import io
import logging
import time

import argh
import flask
import humanize

import page
from db import *

APP = flask.Flask(__name__)


def or_404(arg):
    if not arg:
        return flask.abort(404)
    return arg


def icon(name):
    return f'<i class="fa fa-{name} fa-fw"></i>'


try:
    cmd = "git describe --tags --always --dirty"
    version = subprocess.check_output(shlex.split(cmd)).decode().strip()
except:
    version = None


@APP.context_processor
def inject_globals():
    return {
        "icon": icon,
        "version": version,
    }


@APP.route("/", methods=["GET", "POST"])
def index():
    q = flask.request.args.get("q", "")
    time_now = int(time.time())

    if flask.request.method == "GET":
        if q:
            items = Item.objects.search_text(q).order_by("$text_score")
        else:
            items = Item.objects.order_by("-added_epochtime").limit(100)
        items_count = Item.objects.count()

        def nice_time(t2):
            return humanize.naturaltime(
                dt.timedelta(seconds=(time_now - t2))
            ).capitalize()

        return flask.render_template(
            "index.jinja2", items=items, nice_time=nice_time, q=q, items_count=items_count, title="Cat archive index",
        )
    if flask.request.method == "POST":
        if flask.request.form.get("Submit") == "Submit_add_url":
            unsafe_url = flask.request.form.get("new_url")
            title, body_text, body = page.get_url_text(unsafe_url)
            new_item = Item(
                title=title,
                url=unsafe_url,
                content=body_text,
                added_epochtime=int(time.time()),
            )
            new_item.content_html.put(body)
            new_item.save()
        return flask.redirect(flask.url_for("index"))


def main():
    APP.run(debug=True)


if __name__ == "__main__":
    argh.dispatch_command(main)
