from selenium import webdriver

webpage = r"https://www.bundesanzeiger.de/ebanzwww/wexsservlet" # edit me
searchterm = "innoscripta" # edit me

driver = webdriver.Chrome("C:\Users\Roshan\Downloads\Compressed\chromedriver.exe")
driver.get(webpage)

sbox = driver.find_element_by_id("genericsearch_param.fulltext")
sbox.send_keys(searchterm)

submit = driver.find_element_by_name("(page.navid=quicksearchdetailtoquicksearchnew)")
submit.click()
