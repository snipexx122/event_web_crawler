# Event_Crawler

The project purpose is to crawl events from https://www.lucernefestival.ch/en/program/summer-festival-23 and extract (date,time,location,artists,works,imagelink)
before inserting them into a postgress database. The whole solution is to be 
docerized and run with a docker compose command.


## Tech Stack
**Databse:** Postgress

**Containerization:** Docker

**Program:** python,beautifulSoup,psycopg2

## Steps

1. Extract (date,time,location,artists,works,imagelink) from an event
2. Insert it into the postgresql database.
3. repeat till all events in the page were read.
4. scan the whole the database

## database table statement
event_date | event_time | event_location | event_title | event_artists | event_works | image_link
| :--- | ---: | :---: | :---: | :---: | :---: | :---:
date  | time | text | text | text[] | text[] | text

```javascript
         CREATE TABLE IF NOT EXISTS events
(
    event_date date,
    event_time time without time zone,
    event_location text ,
    event_title text ,
    event_artists text[] ,
    event_works text[] ,
    image_link text 
);
```

## Run Locally

Clone the project

```bash
  git clone https://github.com/snipexx122/event_web_crawler.git
```

Go to the project directory

```bash
  cd event_web_crawler

```

Run 

```bash
  docker-compose up --build
```


