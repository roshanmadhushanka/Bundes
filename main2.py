import requests
from flask import Flask, render_template, redirect, request, url_for, session, send_from_directory
from flask_cors import CORS
from system.io import FileHandler
from system import crawler
from system.structure import ProcessQueue, LinkQueue
from bs4 import BeautifulSoup
import urlparse

app = Flask(__name__)
CORS(app)

main_url = '/'

# Company list
company_list = []
company_list_updated = False

# Process queue
process_queue = LinkQueue()


def updateCompany():
    global company_list, company_list_updated
    file_handler = FileHandler(file_name='company_list')
    company_list = file_handler.read()
    company_list_updated = True
    updateProcessQueue()


def updateProcessQueue():
    global process_queue, company_list
    if not isinstance(process_queue, LinkQueue):
        return

    for company in company_list:
        process_queue.enqueue(company, crawler.getSearchUrls(company))


@app.route(main_url)
def index():
    global company_list
    if not company_list_updated:
        updateCompany()
    session['company_list'] = company_list
    return render_template('main.html')


@app.route('/get_captcha')
def get_captcha():
    global process_queue, main_url
    if not isinstance(process_queue, LinkQueue):
        return

    contetnt = process_queue.dequeue()
    captcha_url = crawler.getCaptchaSource(contetnt['link'])
    session['current_url'] = contetnt['link']
    session['current_company'] = contetnt['company']
    session['current_captcha'] = captcha_url
    return redirect(_main_url)


@app.route('/send_captcha', methods=['POST'])
def send_captcha():
    global main_url
    if request.method == 'POST':
        captcha_solution = request.form.get('captcha_solution')
        current_url = urlparse.urlparse(session['current_url'])
        parsed_url = urlparse.parse_qs(current_url.query)

        dict_to_send = {'session.sessionid': parsed_url['session.sessionid'][0],
                        'genericsearch_param.fulltext': session['current_company'],
                        'genericsearch_param.part_id': None,
                        'captcha_data.solution': captcha_solution,
                        'page.navid': parsed_url['page.navid'][0],
                        '(page.navid=detailsearchdetailtodetailsearchdetailsolvecaptcha)': 'OK'}

        print 'captcha_data.solution', captcha_solution
        print 'session.sessionid', parsed_url['session.sessionid'][0]
        print 'page.navid', parsed_url['page.navid'][0]
        print 'genericsearch_param.fulltext', session['current_company']
        print '(page.navid=detailsearchdetailtodetailsearchdetailsolvecaptcha)', 'OK'

        res = requests.post('https://www.bundesanzeiger.de/ebanzwww/wexsservlet', json=dict_to_send)
        page = res.text
        soup = BeautifulSoup(page, "lxml")
        print soup.prettify()
        table_result = soup.findAll("div", {"id": "preview_data"})

    return redirect(_main_url)


@app.route('/update_company')
def update_company():
    global company_list
    updateCompany()
    return redirect(main_url)

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.run(debug=True)


