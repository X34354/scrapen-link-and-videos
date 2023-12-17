
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import pandas as pd
import time
import json

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

class TikTokScraper:
    def __init__(self, url, file_path):
        self.url = url
        self.file_path = file_path
        self.driver = None

    def open_profile(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.get(self.url)
        time.sleep(20)

    def close_profile(self):
        self.driver.quit()

    def scroll_page(self):
        action = ActionChains(self.driver)
        firstLevelMenu = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div/div/div[2]/div/p[3]')
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
            if (screen_height) * i > scroll_height:
                break
    def extract_video_urls(self):
        #print(self.driver.page_source)
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        videos = soup.find_all("div", {"class": "css-vi46v1-DivDesContainer eih2qak4"})
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
        print(data_antigua)
        return data_antigua

    def save_data(self, df):
        df = df.drop_duplicates()
        df.to_csv(self.file_path, index=False)
        print("Data saved successfully!")

    def scrape(self):
        self.open_profile()
        self.scroll_page()
        df = self.extract_video_urls()
        print(df)
        self.close_profile()

        existing_data = self.load_existing_data()
        #df =pd.concat([ existing_data , df ], 0)
        print(df)
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
