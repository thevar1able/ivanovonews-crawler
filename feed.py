
def formatFeed():
    latestHtml = getLatestPostsHtml()
    news = parseHtmlPosts(latestHtml)

    news.extend(parseHtmlPosts(getLatestPostsHtml(nextPage=2)))

    items = []
    for item in news:
        items.append(
            rfeed.Item(
                title=item['title'],
                link=f"https://ivanovonews.ru{item['href']}",
                guid=rfeed.Guid(item['href']),
                pubDate=item['published'],
            )
        )

    feed = rfeed.Feed(
        title="Ivanovonews RSS Feed",
        description="PoC for later programmatic access",
        link="https://ivanovonews.ru/",
        language="ru-RU",
        lastBuildDate=datetime.now(),

        items=items,
    )

    return feed