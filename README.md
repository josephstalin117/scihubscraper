# scihubscraper
Downloads pdfs of journal articles from Sci-Hub (sci-hub.tw) based on their DOI.

## Examples

### download_from_refs()

This function uses DOIs in a txt file to download a PDF for each DOI. DOIs can be at the end of a reference
like in the articles-with-DOIs.txt example, or they can just be a list of DOIs, like in the just-DOIs.txt example.


In this example, DOIs are taken from articles-with-DOIs.txt and downloaded into the articles directory, which will
be created in the parent directory if it does not exist.
```
from scraper import download_from_refs
download_from_refs('articles-with-DOIs.txt', 'articles')
```

###get_article()

This function downloads a single article's PDF based on its DOI.

```
from scraper import get_article
get_article('10.1016/j.system.2009.02.011')
```
