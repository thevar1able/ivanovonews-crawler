import requests
from lxml import etree
from datetime import datetime
from collections import namedtuple

NewsCard = namedtuple("NewsCard", ["id", "title", "href", "published", "preview", "views"])
NewsDetails = namedtuple("NewsDetails", ["id", "description", "text", "images", "views"])


class IvanovoNews:
    BASE_URL = 'https://ivanovonews.ru/'

    def __init__(self):
        pass

    def load_news_page(self, page_number=1):
        latest = requests.post(
            url="https://www.ivanovonews.ru/local/ajax/",
            headers={
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "X-Requested-With": "XMLHttpRequest",
                # "User-Agent": self.ua.random,
            },
            data=f'sortBy=last&ajaxCallback=CheckNextPage&jsaction=append&target=newsList&newsRegion=all&newsDate=all'
                 f'&action=getNewsPageNextPage&nextPage={page_number}&blurTarget=Y '
        )

        return latest.json()['newsList']

    def load_news_details(self, post_id):
        # post = requests.post(
        #     url="https://www.ivanovonews.ru/local/ajax/",
        #     headers={
        #         "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        #         "X-Requested-With": "XMLHttpRequest"
        #     },
        #     data=f'ajaxCallback=AfterLoadNews&jsaction=append&id={post_id}&target=newsDetailBlock&action=loadNextNews'
        # )

        post = requests.get(
            url=f'https://www.ivanovonews.ru/news/{post_id}/',
            # headers={
            #     "User-Agent": self.ua.random,
            # }
        )

        # return post.json()['newsDetailBlock']
        return post.text

    def parse_news_details(self, post_id, html_data):
        data = etree.HTML(html_data)
        text = data.xpath('//div[@class="news-detail-content"]//text()')
        images = data.xpath('//div[@class="news-content-wrap"]//img[@data-lazy]/@data-lazy')

        description = data.xpath('//div[@class="news-detail__description"]/text()')
        description = ''.join(description).strip()

        views = 0
        try:
            views = int(data.xpath('//div[@class="news-detail-main"]//span[@class="news-stat__views"]/text()')[0])
        except:
            pass

        text = [line.strip() for line in text if line.strip()]

        return NewsDetails(
            id=post_id,
            text=text,
            images=images,
            description=description,
            views=views,
        )

    def parse_news(self, html_data):
        data = etree.HTML(html_data)

        news_objects = data.xpath('//div[@class="news-list__item"]')
        news = []
        for obj in news_objects:
            title = obj.xpath('a//div[@class="news-card__name"]')[0].text
            href = obj.xpath('a[@class="news-card"]')[0].get('href')
            published = obj.xpath('a//span[@class="news-info__date"]')[0].text
            published_date = datetime.strptime(published, '%d.%m.%Y, %H:%M')

            _, _, post_id, _ = href.split('/')

            [img] = obj.xpath('a[@class="news-card"]//img') or [None]
            image = None

            if img is not None:
                image = img.get('data-original')

            views = 0
            try:
                views = int(obj.xpath('a//span[@class="news-stat__views"]/text()')[0])
            except:
                pass

            news.append(NewsCard(
                id=post_id,
                title=title,
                href=href,
                published=published_date,
                preview=image,
                views=views,
            ))

        return news

    def get_news_page(self):
        pages = [
            self.load_news_page(page_number=1),
            self.load_news_page(page_number=2),
        ]

        news_cards = [card for page in pages for card in self.parse_news(page)]

        return news_cards

    def get_detailed_news(self, post_id):
        details_data = self.load_news_details(post_id)

        return self.parse_news_details(post_id, details_data)
