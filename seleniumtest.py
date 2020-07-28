# import neccessary libraries
from selenium import webdriver
#from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import time

#path to webdriver
PATH = "chromedriver\chromedriver.exe"

#add options
options = Options()
options.headless = True
options.add_argument("--window-size=1920,9000")
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-certificate-errors-spki-list')
options.add_argument('--ignore-ssl-errors')

#create a driver
driver  = webdriver.Chrome(PATH, options=options)
# open a website
driver.get('https://lor.mobalytics.gg/stats/decks')
driver.implicitly_wait(0)
#click on select all checkbox to select all decks
for i in range(10):
    try:
        driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[4]/div').click()
        break
    except NoSuchElementException as e:
        print('retry in 1s.')
        time.sleep(1)
else:
    raise e

time.sleep(10)
#scroll down
for a in range(5):
    driver.execute_script("window.scrollTo(0, 9000)") 
    time.sleep(1)
    print("try #"+str(a))
time.sleep(5)

#get deck codes and details
deck_code = driver.find_elements_by_xpath('//*[@id="root"]/div/div[2]/div[1]/div[1]/div[2]/div[1]/div[2]/div[2]/section/a')
element = deck_code

#go through each deck, get playrate and code and add to dataframe
df = []
for deck in element:
    d = {
        'deck_code' : deck.get_attribute('href').replace('https://lor.mobalytics.gg/decks/code/', ''),
        'matches_played' : deck.find_element_by_xpath('.//td[8]/span').text
    }

    df.append(d)

#add all decks to the dataframe
all_decks = pd.DataFrame(df)

#print(df)
#df.to_csv('results.csv')

#close connection with the website
driver.quit()


