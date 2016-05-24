from grab import Grab
from urllib.parse import urljoin

page_count = 3
news_list = []
start_url = 'http://www.kp.by'

def process_news_page(grab, url):
    resp = grab.go(url)

    article_page = grab.doc.select("//div[@class='articlePage pagePad boxOver']")
    if article_page:
        ditem = dict.fromkeys(['author', 'title', 'time', 'comments'])
        ditem['comments'] = article_page.select(".//div[@class='comments showCommentsJS']").text()
        author = article_page.select(".//div[@class='authors']//a")
        if len(author) > 0:
            ditem['author'] = author.text()
        ditem['title'] = article_page.select(".//h1").text()
        news_list.append(ditem)

def get_url(grab, page_num):
    page_url = 'http://www.kp.by/daily/minsk?pages.number=' + str(page_num)
    resp = grab.go(page_url)

    articles_links = [article.attr('href') for article in grab.doc.select("//article[@class='digest']//a[@href]")]

    for article in set(articles_links):
        href = article

        if href.startswith('/daily'):
            url = urljoin(start_url, href)
            print(url)
            process_news_page(grab, url)

g = Grab()
for i in reversed(range(1,page_count + 1)):
    get_url(g, i)

print(news_list)
