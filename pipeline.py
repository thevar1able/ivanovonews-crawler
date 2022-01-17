from parse import IvanovoNews
from summarize import Summarizer
from tg import send
from db import submit_views, save_post

import logging

logger = logging.getLogger(__name__)

iv = IvanovoNews()

logger.info('Charging mah laserz, hold steady')
summarizer = Summarizer()


def run():
    logger.info('Crunching data, just for you')
    check_views()
    news = get_unread_news()

    logger.info(f'Got {len(news)} new news!')

    for n in news:
        title = n.title

        news_details = iv.get_detailed_news(post_id=n.id)

        text = ' '.join(news_details.text)
        sum_text = summarizer.run(text)

        logger.info("#%s\t%s\n%s\n%s" % (n.id, title, sum_text, news_details.images))
        send((n.id, title, sum_text, news_details.images))
        save_post(n.id, n.title, news_details.description, text, ' '.join(news_details.images), n.published)


def check_views():
    logger.info("Refreshing news view count")
    news = iv.get_news_page()
    detailed_news = [iv.get_detailed_news(post_id=n.id) for n in news]

    submit_views(detailed_news)
    logger.info("Updated views for %s articles", len(detailed_news))


def get_unread_news():
    news = iv.get_news_page()

    with open('data/position', 'r') as position:
        last_id = 0
        try:
            last_id = int(position.readline().strip())
        except:
            pass

        news.reverse()

        for idx, n in enumerate(news):
            _, _, post_id, _ = n.href.split('/')
            if int(post_id) == last_id:
                return news[1 + idx:]

        return news
