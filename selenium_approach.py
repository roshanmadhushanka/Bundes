from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys


def getSearchUrls(page):
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

company_name = 'innoscripta'
driver = webdriver.PhantomJS(executable_path='C:\Users\Roshan\Downloads\Compressed\phantomjs-2.1.1-windows\\bin\phantomjs.exe')
driver.get('https://www.bundesanzeiger.de/ebanzwww/wexsservlet')

sbox = driver.find_element_by_id("genericsearch_param.fulltext")
sbox.send_keys(company_name)

submit = driver.find_element_by_name("(page.navid=to_quicksearchlist)")
submit.click()

links = getSearchUrls(driver.page_source)
for link in links:
    print link



