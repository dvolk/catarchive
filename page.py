import argh
import bs4
import mechanize

BR = mechanize.Browser()
BR.set_handle_robots(False)
BR.addheaders = [
    (
        "User-agent",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
    )
]


def tag_visible(element):
    if element.parent.name in [
        "style",
        "script",
        "head",
        "title",
        "meta",
        "[document]",
    ]:
        return False
    if isinstance(element, bs4.Comment):
        return False
    return True


def text_from_html(body):
    soup = bs4.BeautifulSoup(body, "html.parser")
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    text = u" ".join(t.strip() for t in visible_texts)
    return soup.title.get_text(), text


def get_page(url):
    r = BR.open(url).read()
    return r.title(), r


def get_url_text(url):
    title, body = get_page(url)
    title, body_text = text_from_html(body)
    return title, body_text, body


def get_html_file_text(filename):
    body = open(filename, "rb").read()
    title, body_text = text_from_html(body)
    return title, body_text, body


if __name__ == "__main__":
    argh.dispatch_commands([get_url_text, get_html_file_text])
