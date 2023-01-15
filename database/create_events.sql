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