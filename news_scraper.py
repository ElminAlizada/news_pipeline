import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


def news_form_apa():
    url = "https://apa.az/all-news"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    links_list = []
    for data in soup.find("div", class_="four_columns_block").find_all("a"):
        links = data["href"]
        date_div = data.find("div", class_="date")
        time_span = date_div.find("span").text.strip()
        day = date_div.find_all("span")[1].text.strip()
    
        published_datetime = datetime.strptime(time_span, "%H:%M")
        now = datetime.now()
        published_datetime = published_datetime.replace(year=now.year, month=now.month, day=now.day)
        time_difference = now - published_datetime
        
        if time_difference <= timedelta(hours=1):
            links_list.append(links)

   

    news_data = []
    for link in links_list:
  

        response = requests.get(link)
        apa_news_soup = BeautifulSoup(response.text, 'html.parser')

        for news_data_item in apa_news_soup.find_all("main"):
            title = news_data_item.find("h2", class_="title_news").text.strip()

            published_date_div = news_data_item.find("div", class_="date")
            published_date = published_date_div.find("span").text.strip().split(" (")[0]

            image_url = news_data_item.find("div", class_="main_img").find("img")["src"].strip()
            paragraphs = news_data_item.find("div", class_="texts").find_all("p")
            content = ''.join(paragraph.text.strip() for paragraph in paragraphs)
            category = news_data_item.find("h1").text.strip()

            tags_div = news_data_item.find("div", class_="tags")
            tags = []
            if tags_div:
                tag_links = tags_div.find_all("a")
                tags = [tag.text for tag in tag_links]

            news_data.append([link, title, published_date, image_url, content, category, tags])
    print(f"Scraped {len(news_data)} news articles")
    return news_data




def news_form_milli():
  
    url = "https://news.milli.az/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links_list = []
    for data in soup.find("ul",class_="post-list2").find_all("li"):
        link = data.find("a")["href"]
        time_span = data.find("div", class_="info-block").find("span", class_="time").text.strip()
        published_datetime = datetime.strptime(time_span, "%H:%M")
        now = datetime.now()
        published_datetime = published_datetime.replace(year=now.year, month=now.month, day=now.day)
        time_difference = now - published_datetime

        if time_difference <= timedelta(hours=1):
            links_list.append(link)
    news_data = []
   
    for link in links_list:
  
        response = requests.get(link)
        milli_news_soup = BeautifulSoup(response.text, 'html.parser')
        for news_data_item in milli_news_soup.find_all("div",id="main"):

            title = news_data_item.find("h1").text.strip()
            category = news_data_item.find("span",class_="category").text.strip()
            published_date = news_data_item.find("div",class_="date-info").text.strip()
            image_url = news_data_item.find("div",class_="quiz-holder").find("img",class_="content-img")["src"]
            paragraphs = news_data_item.find("div",class_="quiz-holder").find("div",class_="article_text").find_all("p")
            content = ''.join(paragraph.text.strip() for paragraph in paragraphs)
            tags = [] 

            news_data.append([link, title, published_date, image_url, content, category, tags])
    print(f"Scraped {len(news_data)} news articles")
    return news_data


