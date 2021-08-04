# Catarchive: Web archive/bookmarks with full text search

- Add web pages to archive
- Full text search over page content, title and URL
- Stores text stripped of html and full html in database

## Screenshots

<img src="https://i.imgur.com/7cL6WMV.png" width=400>

## Installation

You will need mongodb:

    apt install mongodb-server

No further database configuration is needed.

    git clone https://github.com/dvolk/catarchive
    cd catarchive
    virtualenv env
    source env/bin/activate
    pip3 install -r requirements.txt

## Running

    python3 webapp.py

## Integration with i3 WM

It is convenient to add pages without switching to the catarchive page. To do this catarchive provides a CLI command that takes the URL from the X11 clipboard.

This be bound to a key in your window manager, for example for i3:

   bindsym --release $mod+m exec "/home/dv/src/my/catarchive/env/bin/python /home/dv/src/my/catarchive/cli.py add-from-xclip"
