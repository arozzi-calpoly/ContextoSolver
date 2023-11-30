from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import time

with open('words.txt') as f:
    wordlist = f.read().splitlines()

good_words_so_far = set(w.lower() for w in open('good_words_so_far.txt').read().splitlines())
bad_words_so_far = set(w.lower() for w in open('bad_words_so_far.txt').read().splitlines())
wordlist = {word.lower() for word in wordlist}

wordlist = wordlist - good_words_so_far - bad_words_so_far

url = 'https://contexto.me/'
# url = 'https://www.amazon.com/'
options = webdriver.ChromeOptions()
options.add_argument("--remote-allow-origins=*"); 
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome("chromedriver.exe", options=options)
# driver = webdriver.Firefox('.')
driver.get(url)

elem = driver.find_element(by=By.NAME, value='word')
message_elem = None

if elem is None:
    print("Entry box element not found!")
    exit(1)

print("Found element!")
f_good = open('good_words.txt', 'w+')
f_bad = open('bad_words.txt', 'w+')
bad_words = []
good_words = []
for word in wordlist:
    elem.clear()
    elem.send_keys(word)
    elem.send_keys(Keys.RETURN)

    time.sleep(0.1)

    try:
        message_elem = driver.find_element(by=By.CLASS_NAME, value='message-text')
        is_valid_guess = message_elem is None
    except Exception:
        is_valid_guess = True


    if not is_valid_guess:
        print(f"Bad word '{word}'")
        f_bad.write(word + '\n')
    else:
        print(f"Good word '{word}'")
        f_good.write(word + '\n')



# driver.close()