import schedule
import time
from db_setup import  insert_data
from news_scraper import news_form_apa, news_form_milli

def job():
    apa_news = news_form_apa()
    insert_data(apa_news)
    milli_news = news_form_milli()
    insert_data(milli_news)
    apa_news = news_form_apa()
    milli_news = news_form_milli()

    all_news = apa_news + milli_news

    if all_news:
        insert_data(all_news)
    else:
        print("No news data to insert.")
        

def main():
    schedule.every().hour.do(job)
    job()

    while True:
        schedule.run_pending()  
        time.sleep(1)  

if __name__ == "__main__":
    main() 