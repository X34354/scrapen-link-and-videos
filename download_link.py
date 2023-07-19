
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time
import json

class TikTokScraper:
    def __init__(self, url, file_path):
        self.url = url
        self.file_path = file_path
        self.driver = None

    def open_profile(self):
        self.driver = webdriver.Chrome()
        self.driver.get(self.url)
        time.sleep(10)

    def close_profile(self):
        self.driver.quit()

    def scroll_page(self):
        action = ActionChains(self.driver)
        firstLevelMenu = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div/div[2]/div/p[3]/span')
        l = firstLevelMenu.location
        s = firstLevelMenu.size
        time.sleep(5)
        action.move_by_offset(l['x'], l['y'])
        action.click()
        action.perform()
        time.sleep(1)

        scroll_pause_time = 1
        screen_height = self.driver.execute_script("return window.screen.height;")
        i = 1

        while True:
            self.driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
            i += 1
            time.sleep(scroll_pause_time)
            scroll_height = self.driver.execute_script("return document.body.scrollHeight;")
            if 1 > 0:
                break

    def extract_video_urls(self):
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        videos = soup.find_all("div", {"class": "tiktok-c83ctf-DivWrapper"})
        dataframe = {}
        links = []
        indexs = []

        for index, video in enumerate(videos):
            links.append(video.a["href"])
            indexs.append(index)

        dataframe['URL'] = links
        df = pd.DataFrame(dataframe)
        return df

    def load_existing_data(self):
        try:
            data_antigua = pd.read_csv(self.file_path)
            try: 
                data_antigua = data_antigua.drop("Unnamed: 0", axis=1)
            except:
                pass
        except FileNotFoundError:
            data_antigua = pd.DataFrame()

        return data_antigua

    def save_data(self, df):
        df = df.drop_duplicates()
        df.to_csv(self.file_path, index=False)
        print("Data saved successfully!")

    def scrape(self):
        self.open_profile()
        self.scroll_page()
        df = self.extract_video_urls()
        self.close_profile()

        existing_data = self.load_existing_data()
        df =pd.concat([ existing_data , df ], 0)

        self.save_data(df)


# Main execution
def link(data):

    profile_url =data['profile_url']
    file_path = data['file_path']

    scraper = TikTokScraper(profile_url, file_path)
    scraper.scrape()


if __name__ == "__main__":
    # Open the JSON file
    with open('configuration.json', 'r') as file:
        data = json.load(file)

    link(data)