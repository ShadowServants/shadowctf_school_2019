from app import celery
from app import crawl
from app.helpers import set_search_is_running, set_search_runned


@celery.task
def crawl_url(url, user_id):
    set_search_is_running(user_id)
    crawl.crawl_site(url, user_id)
    set_search_runned(user_id)
