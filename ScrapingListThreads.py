import os
import re
import time

from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from urllib.parse import urlparse




def get_list_pathologie(count=1, keyword ='Asthme' ):
    
    options = Options()
    options.add_experimental_option("detach",True)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                              options=options)
    lettre = keyword[0]


    for page_nb in range(1, count+1):
            page_url = f"https://www.carenity.com/forum/index-forums/{lettre}?page={page_nb}"
            driver.get(page_url)
            time.sleep(12)   #to not get blocked
            links = driver.find_elements("xpath", 
                                        f"//div[contains(@class,'box-list')]//a[contains(text(),'{keyword}')]")
            
            if links is not None:
                for link in links:
                    print(link.get_attribute("href"))
                    link_pathologie = link.get_attribute("href")
                    link.click()
                break

    
    p_interests = driver.find_elements("xpath",
                                    "//div[contains(@class,'module-discussions box-list-thread')]//h2//a[contains(@class,'for-box-click')]")

    result_interest = pd.DataFrame(columns=['Title', 'Link'])
    
    url = link_pathologie
    parsed_url = urlparse(url)
    path = parsed_url.path
    last_part = path.rsplit('/', 1)[-1]

    result_interest.loc[len(result_interest)] = ["Fiche de la maladie ",f"https://www.carenity.com/infos-maladie/{last_part}"]

    for interest in p_interests:
        thread_href = interest.get_attribute("href")
        thread_title = interest.get_attribute("innerHTML")
        
        result_interest.loc[len(result_interest)] = [thread_title,thread_href]

        

    print(result_interest)
    
    return result_interest


    


def save_pages(pages):
    os.makedirs("data", exist_ok = True)
    for page_nb, page in enumerate(pages):
        with open(f"data/page_{page_nb}.html", "wb") as f_out:
            f_out.write(page)


def main():
    get_list_pathologie()

if __name__ == "__main__":
    main()


# links = driver.find_elements("xpath", "//div[]")
