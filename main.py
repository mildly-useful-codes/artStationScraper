import requests
from bs4 import BeautifulSoup
import argparse as ap
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from tqdm import tqdm
import urllib.request
import os
import time

# Command Line argument
args = ap.ArgumentParser("Enter account name: ")
args.add_argument("n", type=str)
args = args.parse_args()

# Selenium options
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
# options.add_argument('--headless')

# Open, scroll to end a few times, return page source
def open_and_scroll(URL):
    driver = webdriver.Chrome("/usr/lib/chromium/chromedriver", chrome_options=options)
    driver.get(URL)
    actions = ActionChains(driver)
    for i in range(3):
        actions.send_keys(u'\ue010')
        actions.perform()
    time.sleep(0.5)
    return driver.page_source

# Arguments

URL = f"https://www.artstation.com/{args.n}"
try:
    page = requests.get(URL)
    print("Loaded user :)")
except:
    print(f"Invalid user, try again. Current link : {URL}")

# Front page -> Links to all images
page_source = open_and_scroll(URL)
soup = BeautifulSoup(page_source, 'html.parser')
s = soup.findAll("a", {"class": "project-image"})
sources = [f"https://www.artstation.com{link['href']}" for link in s]
print(sources[0])

# Individual pages
try:
    os.mkdir(args.n)
except FileExistsError:
    pass

to_download = []
print("Getting links. Dont touch anything.")
for i in tqdm(sources):
    page_source = open_and_scroll(i)
    # print(page_source)
    soup = BeautifulSoup(page_source, 'html.parser')
    s = soup.findAll("img", {"class":"img"})
    # print(len(s))
    sources = [link["src"] for link in s]
    to_download.extend(sources)
    # break

to_download = [x.split("?")[0] for x in to_download]
print(len(to_download), to_download[0])

# Backup links just in case
with open("./links.txt","w+") as f:
    for i in to_download:
        f.write(f"\n{i}")

# Download images
print("Downloading images")
name_counter = 0
for i in tqdm(to_download):
    with open(f"./{args.n}/{str(name_counter)}.jpg","wb+") as f:
        f.write(requests.get(i).content)
    name_counter+=1


