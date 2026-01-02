from scraper.parser import parse_page

urls = [
    "https://ekantipur.com/news/"
]

all_articles = []
for url in urls:
    articles = parse_page(url)
    all_articles.extend(articles)

for a in all_articles:
    print(f"title: {a['title']}\nlink: {a['link']}\n")