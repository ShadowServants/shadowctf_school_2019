import urllib.request

from bs4 import BeautifulSoup
from app.models import WebPage
import random


def full_url(url, link):
    return url + link if 'http' not in url else link


def crawl_url(url, timeout=3):
    headers = {'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:48.0) Gecko/20100101 Firefox/48.0"}
    try:
        request = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(request, timeout=timeout).read()
    except Exception:
        return '', []
    else:

        html = BeautifulSoup(response, 'html.parser')
        content = html.get_text()
        links = [link.get('href') for link in html.find_all('a', href=True)]
        urls = [full_url(url, link) for link in links]
        return content, urls


def crawl_site(url, user_id, level=3):
    if level <= 0:
        return
    content, urls = crawl_url(url)
    if len(urls) > 3:
        urls = random.choices(urls, k=3)
    WebPage(url=url, content=content, user_id=user_id).save()
    for new_url in urls:
        crawl_site(new_url, user_id, level=level - 1)
