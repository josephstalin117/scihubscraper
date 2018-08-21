# scihubscraper
Downloads pdfs of journal articles from Sci-Hub (sci-hub.tw) based on their DOI.

## Examples

Download articles from the txt file /articles-with-DOIs.txt with references on each line and DOIs at the end of each reference, saving the downloaded PDFs into the /articles directory:
```
from scraper import download_from_refs
download_from_refs('articles-with-DOIs.txt', 'articles')
```

Download the PDF of one article into the current directory based on its DOI:
```
from scraper import get_article
get_article('10.1016/j.system.2009.02.011')
```
