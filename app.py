from flask import Flask, render_template, redirect, request, url_for, session, send_from_directory
from flask_cors import CORS
from bs4 import BeautifulSoup
from selenium import webdriver
import urllib2

app = Flask(__name__)
CORS(app)


def getSearchUrls(company_name="innoscripta"):
    '''
    Search for particular company name and get set of urls related to that company
    :param company_name: company name that needed to be searched
    :return: set of urls from the result
    '''

    search_url = 'https://www.bundesanzeiger.de/ebanzwww/wexsservlet?global_data.designmode=eb&genericsearch_param.fulltext=' \
                 + company_name + '&genericsearch_param.part_id=&%28page.navid%3Dto_quicksearchlist%29=Suchen'

    page = urllib2.urlopen(search_url)
    soup = BeautifulSoup(page, "lxml")
    table_result = soup.findAll("table", {"summary": "Trefferliste"})
    td_results = [a.find_all("td", {"class": "info"}) for a in table_result]

    if len(td_results) == 0:
        return

    available_links = []
    for p in td_results:
        for t in p:
            for a in t:
                result_url = 'https://www.bundesanzeiger.de/' + a['href']
                available_links.append(result_url)

    return available_links


def getCaptchaSource(url):
    '''
    Get URL of captcha image
    :param url: url for the page where captcha is located
    :return: image url for the captcha image
    '''

    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page, "lxml")
    captcha_result = soup.find_all("img", {"alt": "Captcha"})
    return 'https://www.bundesanzeiger.de/' + captcha_result[0]['src']


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        company_name = request.form.get("company_name")
        result_urls = getSearchUrls(company_name)
        captcha_urls = []
        for url in result_urls:
            captcha_urls.append(getCaptchaSource(url))
        session['captcha_urls'] = captcha_urls
        print captcha_urls
        print result_urls
        print result_urls[0] == result_urls[1]
    return render_template('index.html')


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.run(debug=True)



'''
References
==========

> Send input
http://stackoverflow.com/questions/13166395/fill-input-of-type-text-and-press-submit-using-python

> Search tag with attributes
http://stackoverflow.com/questions/8933863/how-to-find-tags-with-only-certain-attributes-beautifulsoup

http://stackoverflow.com/questions/13960326/how-can-i-parse-a-website-using-selenium-and-beautifulsoup-in-python

https://pypi.python.org/pypi/captcha-solver/0.0.3
'''
