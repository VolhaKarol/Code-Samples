import pickle
from collections import defaultdict, Counter

with open('news_list.pickle', 'rb') as f:
    news_list = pickle.load(f)

news_by_authors = defaultdict(list)
for news_item in news_list:
    key = news_item['author']
    news_by_authors[key].append(news_item)

#for a in news_by_authors.items():
#    a[1].append({'count': len(a[1])})