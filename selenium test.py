from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

options = Options()
#options.headless = True
options.add_argument("--window-size=1920,1200")
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')

driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
driver.get('https://lor.mobalytics.gg/stats/decks')
driver.implicitly_wait(30)
driver.execute_script("window.scrollTo(0, 1080)") 
driver.implicitly_wait(15)
deck_code = driver.find_elements_by_xpath('//*[@id="root"]/div/div[2]/div[1]/div[1]/div[2]/div[1]/div[2]/div[2]/section/a')
element = deck_code

for deck in element:
    print("deck code: " + deck.get_attribute('href'))
    print("matches_played: " + deck.find_element_by_xpath('.//td[8]/span').text)
print(len(element))
driver.quit()

