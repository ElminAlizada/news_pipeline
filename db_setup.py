from datetime import datetime
import psycopg2

az_to_en_months = {
    'yanvar': 'January',
    'fevral': 'February',
    'mart': 'March',
    'aprel': 'April',
    'may': 'May',
    'iyun': 'June',
    'iyul': 'July',
    'avqust': 'August',
    'sentyabr': 'September',
    'oktyabr': 'October',
    'noyabr': 'November',
    'dekabr': 'December'
}

def convert_az_date_to_timestamp(date_string):
    day, month, year, time = date_string.split()
    month = az_to_en_months[month.lower()]
    date = datetime.strptime(f"{day} {month} {year} {time}", "%d %B %Y %H:%M")
    return date

def connect_to_db():
    conn = psycopg2.connect(
        dbname='news',
        user='postgres',
        password='#',
        host='localhost',
        port='5432'
    )
    return conn

def insert_data(news_data):
    conn = connect_to_db()
    cur = conn.cursor()
    insert_query = '''
    INSERT INTO news_articles (url, title, content, published_date, image_url, category, tags) 
    VALUES (%s, %s, %s, %s, %s, %s, %s);
    '''

    for data in news_data:
        url, title, published_date, image_url, content, category, tags = data
        converted_date = convert_az_date_to_timestamp(published_date)

        if tags is None:
            tags_array = '{}'
        elif isinstance(tags, str):
            tags_array = '{' + f'"{tags}"' + '}'
        else:
            tags_array = '{' + ','.join(f'"{tag}"' for tag in tags) + '}'

        cur.execute(insert_query, (url, title, content, converted_date, image_url, category, tags_array))
    

    conn.commit()
    cur.close()
    conn.close()
