from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox(executable_path='C:\Users\Roshan\PycharmProjects\\bundesanzeiger\driver\geckodriver.exe')
driver.get('https://www.bundesanzeiger.de/ebanzwww/wexsservlet')

sbox = driver.find_element_by_id("genericsearch_param.fulltext")
sbox.send_keys("innoscripta")


submit = driver.find_element_by_name("(page.navid=to_quicksearchlist)")
submit.click()

soup = BeautifulSoup(driver.page_source, 'lxml')

table_result = soup.findAll("table", {"summary" :"Trefferliste"})
td_results = [a.find_all("td", {"class": "info"}) for a in table_result]

for p in td_results:
    for t in p:
        for a in t:
            link = driver.find_element_by_link_text()
            link.click()
            link.send_keys(Keys.CONTROL + Keys.RETURN)

#
# for link in soup.find_all('a'):
#     print link.get('href', None), link.get_text()
