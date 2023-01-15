from bs4 import BeautifulSoup
import requests
import re
import psycopg2
import sys


def insert_into_sql_table(connection,cursor,date,time,location,title,artists,works,image_link):
    cursor.execute('''
    INSERT INTO events values(%s,%s,%s,%s,%s,%s,%s);
    
    
    ''',[date,time,location,title,artists,works,image_link])
    connection.commit()

def read_sql_table(cursor):
    cursor.execute('''
    select * from events;
    ''')
    print(cursor.fetchall())



def get_url_page_content(url):
    page = requests.get(url)
    
    soup = BeautifulSoup(page.content, 'html.parser')
    
    return soup


def get_date_time(soup):
    s = soup.find('div',class_="cell large-6 subtitle")
    
    text = s.text.split('\n')[2:][0]+s.text.split('\n')[2:][1]+s.text.split('\n')[2:][2] 
    
    text = re.sub(r'\t', '', text)
     
    date = text.split("|")[0].split(" ")[1]

    day = date.split(".")[0]
    month = date.split(".")[1]
    year = "2023"
    date = year + "-"+month+"-"+day
    
    time = text.split("|")[1]
    
    hour = time.replace(" ","").split(".")[0]
    minutes = time.replace(" ","").split(".")[1]
    time = hour+":"+minutes+":00"
    
    return date,time

def get_location_title_works(soup):
    
    s = soup.find_all('div',class_="cell medium-9")
    
    s2 = soup.find_all('div',class_="cell large-6 subtitle")
    
    items = s[0].find_all('div',class_="program-item")
    
    title = ""
    
    if len(s2)==2:
        title = re.sub(r'\n','',re.sub(r'\t','',s2[1].text))
        title = title.replace("Program",'').replace("“","").replace("”","")
    
    works = []
    
    for i in range(0,len(items)):
        if items[i].find("strong"):
            works.append(items[i].find("strong").text.replace("'","").replace('"',''))
    
    loc_area = s[1].find_all('p')
    
    location = re.sub(r'\s+',' ',loc_area[len(loc_area)-2].text)
    
    if len(works) == 0 :
        works.append("will be announced later")
    
    if title == "":
        title = "will be announced later"
    
    return location,title,works

def get_artists(soup):
    
    s = soup.find('ul',class_='performers-list grid-x grid-margin-x')
    
    performers = s.find_all('li',class_='cell medium-6 p')
    
    performers_list = []
    for i in range(0,len(performers)):
        
        performer = (re.sub(r'\n','',re.sub(r'\t','',performers[i].text))).replace("conductor","").replace("host","")
        
        performers_list.append(performer)
    return performers_list


def get_image_url(soup):
    s = soup.find('figure',class_="fullscreen-image")

    return s.find('source')['srcset']
    

def get_insert_page_info(cursor,connection,url,main_url):
    
    
    
    page = requests.get(url)
    
    soup  = BeautifulSoup(page.content,'html.parser')
    
    date,time = get_date_time(soup)
    
    location,title,works = get_location_title_works(soup)
    
    performers = get_artists(soup)
    
    image_url = main_url+get_image_url(soup)
    
    insert_into_sql_table(connection,cursor,date,time,location,title,performers,works,image_url)

def loop_href(user,password,host,port,database,main_url,soup):
    connection = psycopg2.connect(user=user,
                                  password=password,
                                  host=host,
                                  port=port,
                                  database=database)
    cursor = connection.cursor()
    
    s1 = soup.find('ul', class_='event-list')
    
    url_list = s1.find_all('li',class_='event-item')
    
    counter = 0 
    
    for i in range(0,len(url_list)):
        print("event number : " + str(counter) + " read and recorded in the db")
        counter+=1
        get_insert_page_info(cursor,connection,main_url + url_list[i].find('a',href = True)['href'],main_url)
    print("reading started:--------------------------------------")
    
    read_sql_table(cursor)



if  __name__ == "__main__" :

    user = "username"
    password = "secret"
    host = "db"
    port = "5432"
    database = "database"
    
    main_url = "http://lucernefestival.ch"
    
    url = main_url+"/en/program/summer-festival-23"
    
    soup = get_url_page_content(url)
    
    loop_href(user,password,host,port,database,main_url,soup)
    
    print("reading done------------------------------------")