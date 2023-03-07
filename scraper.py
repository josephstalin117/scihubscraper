import bs4, requests, time, os, logging
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
logging.basicConfig(filename='errors.log', level=logging.ERROR)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


def get_html(url, proxies=None):
    """Returns bs4 object that you can iterate through based on html elements and attributes."""
    s = requests.Session()
    headers = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
        }
    html = s.get(url, timeout=60, headers=headers, allow_redirects=False, proxies=proxies)
    html.encoding = 'utf-8'
    html.raise_for_status()
    html = bs4.BeautifulSoup(html.text, 'html.parser')
    return html



def get_article(doi, base_url='https://sci-hub.hkvisa.net/', folder='', number=None):
    """Downloads a single article based on its DOI."""
    # gets the HTML on the page for the article
    url = base_url + doi
    # Does not attempt to scrape if redirected to other site
    # e.g. http://www.degruyter.com.https.sci-hub.mu/view/j/prbs.2015.27.issue-2/probus-2015-0004/probus-2015-0004.xml
    # with DOI 10.1515/probus-2015-0004
    proxies = {
        #"http": "http://172.18.10.204:7890",
        #"https": "http://172.18.10.204:7890",
        "http": "http://127.0.0.1:7890",
        "https": "http://127.0.0.1:7890",
    }

    html = get_html(url, proxies=proxies)

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

        headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1'}
        pdf = requests.get(pdf_url, proxies=proxies, headers=headers)
        pdf_fn = pdf_url.split('/')[-1].split('.pdf')[0]
        #new_fn = '{0}_{1}.pdf'.format(pdf_fn, doi.replace('/', ' '))
        if number is not None:
            logger.info(number)
            new_fn = '{0}_{1}_{2}.pdf'.format(number, doi.split('/')[0], pdf_fn)
        else:
            new_fn = '{0}_{1}.pdf'.format(doi.split('/')[0], pdf_fn)
        file_path = os.path.join(folder, new_fn)
        with open(file_path, 'wb') as f:
            f.write(pdf.content)
        logger.info(doi)
        time.sleep(2)
    else:
        # Logs DOI when there is no iframe#pdf on the page
        logger.error(doi)


def get_ieee(doi, number=None, folder=''):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:57.0) Gecko/20100101 Firefox/57.0'}

    browser = webdriver.Chrome('D:\Program Files\chromedriver_win32\chromedriver.exe')

    urlBase='https://ieeexplore.ieee.org/search/searchresult.jsp?action=search&newsearch=true&searchField=Search_All&matchBoolean=true&queryText="DOI":'

    url = urlBase+doi
    browser.get(url)
    time.sleep(3)
    #link_list = browser.find_element(by=By.XPATH, value = '//*[@class="fw-bold"]')
    link_list = browser.find_element(by=By.XPATH, value = '//*[@class="List-results-items"]')
    if link_list=='':
        print('Failed to download the {} paper'.format(doi))
        logger.error(doi)
    arcNum=link_list.get_attribute('id')
    print(arcNum)
    pdf_doc_url='http://ieeexplore.ieee.org/document/9681908'
    browser.get(pdf_doc_url)
    #pdfUrl='http://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=' + arcNum
    pdfUrl='http://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=' + '9681908'
    time.sleep(2)
    browser.get(pdfUrl)
    print(pdfUrl)
    browser.find_element(by=By.XPATH, value ='//div[@id="icon"]').click()
    exit()
    browser.get(pdfUrl)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    result = soup.body.find_all('iframe')
    browser.find_element(by=By.XPATH, value ='//*[@id="icon"]').click()
    print(arcNum, result)
    if result==[]:
        print('Failed to download the {} paper with article number {}'.format(doi,arcNum))
        logger.error(doi)
    downloadUrl = result[-1].attrs['src'].split('?')[0]
    response = requests.get(downloadUrl, timeout=80, headers=headers)

    if number is not None:
        fname = str(number)+'_'+downloadUrl[-12:]
    else:
        fname = downloadUrl[-12:]

    with open(fname,'ab+') as f:
        print('start download file ',fname)
        f.write(response.content)



def download_from_refs(txt_file, folder='', item_delimiter='\n', subitem_delimiter=' ', base_url='https://sci-hub.hkvisa.net/', txt_file_encoding='UTF-8', start_at=0):
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
        number, doi = doi.split(',')
        print(number, doi)
        get_article(doi, base_url=base_url, folder=folder, number=number)


if __name__ == '__main__':
    #get_article('10.1109/TII.2017.2734686')
    download_from_refs('DOIs2.txt', '172')
    #get_ieee('10.1109/HNICEM51456.2020.9400051', number=169)
