import bs4, requests, time, os, logging

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
logging.basicConfig(filename='errors.log', level=logging.ERROR)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


def get_html(url):
    """Returns bs4 object that you can iterate through based on html elements and attributes."""
    s = requests.Session()
    headers = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
        }
    html = s.get(url, timeout=60, headers=headers, allow_redirects=False)
    html.encoding = 'utf-8'
    html.raise_for_status()
    html = bs4.BeautifulSoup(html.text, 'html.parser')
    return html


def get_article(doi, base_url='http://sci-hub.tw/', folder=''):
    """Downloads a single article based on its DOI."""
    # gets the HTML on the page for the article
    url = base_url + doi
    # Does not attempt to scrape if redirected to other site
    # e.g. http://www.degruyter.com.https.sci-hub.mu/view/j/prbs.2015.27.issue-2/probus-2015-0004/probus-2015-0004.xml
    # with DOI 10.1515/probus-2015-0004

    html = get_html(url)


    time.sleep(1)
    # Finds the iframe containing the pdf
    iframe = html.find('iframe', {'id': 'pdf'})

    if iframe is not None:
        # Downloads the article when iframe#pdf exists by using the link in its src attribute
        pdf_url = iframe['src']
        # handles error where URL in iframe doesn't have http:// at beginning
        # (e.g. http://sci-hub.tw/10.3389/fnhum.2015.00563)
        if pdf_url.startswith('//'):
            pdf_url = 'http:' + pdf_url

        pdf = requests.get(pdf_url)
        pdf_fn = pdf_url.split('/')[-1].split('.pdf')[0]
        new_fn = '{0}_{1}.pdf'.format(pdf_fn, doi.replace('/', ' '))
        file_path = os.path.join(folder, new_fn)
        with open(file_path, 'wb') as f:
            f.write(pdf.content)
        logger.info(doi)
        time.sleep(1)
    else:
        # Logs DOI when there is no iframe#pdf on the page
        logger.error(doi)


def download_from_refs(txt_file, folder='', item_delimiter='\n', subitem_delimiter=' ', base_url='http://sci-hub.tw/',
                       txt_file_encoding='UTF-8', start_at=0):
    """
    Iterates through txt file of references with DOIs, calling get_article on each DOI. Assumes DOI is at end.

    Arguments:
        txt_file: path to the file containing references

    Keyword Arguments:
        folder: directory that files will be saved to. New directory is created if one does not exist.
        item_delimiter: string that references are delimited by
        subitem_delimiter: string separating DOI from other things in the reference
        base_url: url without the DOI at the end
        txt_file_encoding: character encoding of the txt file
        start_at: line in txt_file that the list of DOIs will start at

    Example code:
        Downloads articles in articles-with-DOIs.txt and saves them in the articles directory
        >>> from scraper import download_from_refs
        >>> download_from_refs('articles-with-DOIs.txt', 'articles')

    Example reference line formatted according to default kwargs:
        Amuzie, G. L. & Winke, P.  | 2009 | Changes in language learning beliefs as a result of study abroad |  System |  37 |  366-379 | 10.1016/j.system.2009.02.011


    """
    with open(txt_file, encoding=txt_file_encoding) as f:
        references = f.read().strip()

    dois = [line.split(subitem_delimiter)[-1] for line in references.split(item_delimiter)[start_at:] if line]

    if folder and not os.path.exists(folder):
        os.mkdir(folder)

    for doi in dois:
        get_article(doi, base_url=base_url, folder=folder)
