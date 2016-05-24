from grab import Grab
from urllib.parse import urljoin

page_count = 3
start_url = 'http://www.kp.by'

def execute_query(node, query):
    nodes = node.select(query)
    return nodes[0].text() if len(nodes) > 0 else None


def process_news_page(grab, url):
    resp = grab.go(url)
    article_page = grab.doc.select("//div[@class='articlePage pagePad boxOver']")

    if article_page:
        news_item = dict.fromkeys(['author', 'title', 'time', 'comments'])

        news_item['comments'] = execute_query(article_page, ".//div[@class='comments showCommentsJS']")
        news_item['author'] = execute_query(article_page, ".//div[@class='authors']//a")
        news_item['title'] = execute_query(article_page, ".//h1")

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
g = Grab()

for i in reversed(range(1, page_count + 1)):
    urls = get_urls(g, i)
    for url in urls:
        news_item = process_news_page(g, url)
        if news_item:
            news_list.append(news_item)

print(news_list)
