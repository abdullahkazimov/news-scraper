import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime

def news_to_excel(news_list, file_path):
    df = pd.DataFrame(news_list)
    df.to_csv(file_path)
    return

def get_news_data(driver, news_url):
    content = {}
    driver.get(news_url)
    url = driver.current_url
    
    content['id'] = url.split('/')[-1]
    content['url'] = url
    
    title_xpath = "//div[@class='news-container']//h1[@class='medium-up']"
    content['title'] = driver.find_elements(By.XPATH, title_xpath)[0].text
    
    content_xpath = "//div[@class='news-inner']"
    content['content'] = driver.find_elements(By.XPATH, content_xpath)[0].text
    
    date_xpath = "//div[@class='date-block']"
    content['date'] = driver.find_elements(By.XPATH, date_xpath)[0].text
    
    time_xpath = "//div[@class='time-block']"
    content['time'] = driver.find_elements(By.XPATH, time_xpath)[0].text
    
    stats_xpath = "//div[@class='actions-block']//span[@class='stats-i']"
    content['views'] = driver.find_elements(By.XPATH, stats_xpath)[0].text
    content['likes'] = driver.find_elements(By.XPATH, stats_xpath)[1].text
    content['dislikes'] = driver.find_elements(By.XPATH, stats_xpath)[2].text
    
    content['category'] = content['url'].split('/')[3]
    
    img_xpath = "//img[@class='news-img medium-up']"
    content['image'] = driver.find_elements(By.XPATH, img_xpath)[0].get_attribute('src')
    
    content['scrape_datetime'] = datetime.now().strftime("%d-%b-%Y %H:%M:%S")
    
    return content

def get_news_url_list(driver, n):
    driver.get("https://oxu.az/")
    news_url_xpath = "//div[@class='news-i']/a"
    news_url_list = driver.find_elements(By.XPATH, news_url_xpath)
    news_url_list = [news_url.get_attribute('href') for news_url in news_url_list]
    return news_url_list[:n]

def run():
    n = int(input("How many news you want to scrape? "))
    driver = webdriver.Chrome()
    news_url_list = get_news_url_list(driver, n)
    news_data = []
    for news_url in news_url_list:
        news_data.append(get_news_data(driver, news_url))
    news_to_excel(news_data, 'news.xlsx')
    driver.quit()
    print("News scraped successfully!")
    
if __name__ == '__main__':
    run()
