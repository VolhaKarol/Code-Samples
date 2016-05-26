from grab import Grab
from urllib.parse import urljoin
import pickle

page_count = 3
start_url = 'http://www.kp.by'


def execute_query(node, query, first_only=True):
    nodes = node.select(query)

    q_result = None

    if len(nodes) > 0:
        q_result = nodes[0].text().strip() if first_only else ' '.join(n.text().strip() for n in nodes)

    return q_result


def process_news_page(gra, page_url):
    resp = grab.go(page_url)
    article_page = grab.doc.select("//div[contains(@class, 'articlePage')]")

    if article_page:
        news_item = dict.fromkeys(['author', 'date', 'title', 'description', 'content', 'comments'])

        news_item['author'] = execute_query(article_page, ".//div[contains(@class, 'authors')]//a")
        news_item['comments'] = execute_query(article_page, ".//div[contains(@class, 'comments')]") or '0'
        news_item['title'] = execute_query(article_page, ".//h1")
        news_item['description'] = execute_query(article_page, ".//*[not(contains(@class, 'video'))]//h2")
        news_item['content'] = execute_query(
            article_page,
            ".//div[contains(@class, 'text')]/*[not(contains(@class, 'coverImg')) and not(contains(@class, 'video'))]",
            False)

        news_item['date'] = execute_query(article_page, ".//time")
        return news_item

    return None


def get_urls(grab, page_num):
    page_url = 'http://www.kp.by/daily/minsk?pages.number=' + str(page_num)
    resp = grab.go(page_url)

    articles_links = [article.attr('href') for article in grab.doc.select("//article[@class='digest']//a[@href]")]
    unique_articles = (article for article in set(articles_links) if article.startswith('/daily'))

    for article in unique_articles:
        url = urljoin(start_url, article)
        print(url)
        yield url


news_list = []
grab = Grab()
grab.setup(timeout=15, connect_timeout=10)

for i in reversed(range(1, page_count + 1)):
    urls = get_urls(grab, i)
    for url in urls:
        news_item = process_news_page(grab, url)
        if news_item:
            news_list.append(news_item)

with open('news_list.pickle', 'wb') as f:
    pickle.dump(news_list, f)