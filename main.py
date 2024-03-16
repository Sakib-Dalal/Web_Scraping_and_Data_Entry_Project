import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

ZILLOW_URL = 'https://appbrewery.github.io/Zillow-Clone/'
FORM_URL = 'https://docs.google.com/forms/d/e/1FAIpQLSda3ANolOQ-jM4OBS31TwBQ0sRwuYiDab6bQ97mfP0X4dHRfA/viewform?usp=sf_link'

response = requests.get(url=ZILLOW_URL)
soup = BeautifulSoup(response.text, 'html.parser')

address_lst = []
price_lst = []
link_lst = []

address = soup.find_all(name='address')
price = soup.find_all(name='div', class_='PropertyCardWrapper')
link = soup.find_all(name='div', class_='StyledPropertyCardDataWrapper')

for a in address:
    address_lst.append(a.text.strip())

for p in price:
    price_lst.append(p.text.strip())

for l in link:
    link_lst.append(l.find('a').get('href'))


chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('detach', True)

driver = webdriver.Chrome(options=chrome_options)
driver.get(url=FORM_URL)

for i in range(len(address_lst)):
    time.sleep(2)
    fill_address = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    fill_address.send_keys(f'{address_lst[i]}')

    fill_price = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    fill_price.send_keys(f'{price_lst[i]}')

    fill_link = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    fill_link.send_keys(f'{link_lst[i]}')

    submit_button = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
    submit_button.click()

    submit_button = driver.find_element(By.LINK_TEXT, 'Submit another response')
    submit_button.click()

driver.quit()

