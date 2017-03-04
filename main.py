import requests
from flask import Flask, render_template, redirect, request, url_for, session, send_from_directory
from flask_cors import CORS
from selenium import webdriver

from system.io import FileHandler
from system import crawler
from system.structure import ProcessQueue
from bs4 import BeautifulSoup
import urlparse

app = Flask(__name__)
CORS(app)

main_url = '/'

# Company list
company_list = []
company_list_updated = False

# Process queue
process_queue = ProcessQueue()

# Phantom
driver = webdriver.PhantomJS(executable_path='C:\Users\Roshan\Downloads\Compressed\phantomjs-2.1.1-windows\\bin\phantomjs.exe')


def updateCompany():
    global company_list, company_list_updated
    file_handler = FileHandler(file_name='company_list')
    company_list = file_handler.read()
    company_list_updated = True
    updateProcessQueue()


def updateProcessQueue():
    global process_queue, company_list
    if not isinstance(process_queue, ProcessQueue):
        return

    links = []
    for company in company_list:
        links.extend(crawler.getSearchUrls(company))

    process_queue.enqueue(links)


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
    if not isinstance(process_queue, ProcessQueue):
        return

    web_url = process_queue.dequeue()
    if not web_url:
        session['end'] = 'true'
        return

    captcha_url = crawler.getCaptchaSource(web_url)

    session['current_url'] = web_url
    session['current_captcha'] = captcha_url
    return redirect(main_url)


@app.route('/send_captcha', methods=['POST'])
def send_captcha():
    global main_url, driver
    if request.method == 'POST':
        ans_captcha = request.form.get('captcha_solution')
        driver.get(session['current_url'])

        print 'ans_captcha', ans_captcha
        print 'current_url', session['current_url']

        captcha_input = driver.find_element_by_id("captcha_data.solution")
        captcha_input.send_keys(ans_captcha)

        submit = driver.find_element_by_name("(page.navid=detailsearchdetailtodetailsearchdetailsolvecaptcha)")
        submit.click()

        soup = BeautifulSoup(driver.page_source, 'lxml')
        print soup.prettify()

    return redirect(main_url)


@app.route('/update_company')
def update_company():
    global company_list
    updateCompany()
    return redirect(main_url)

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.run(debug=True)


