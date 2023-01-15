FROM python:3.12-rc-bullseye
ADD web_crawler.py .
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
# RUN pip3 install psycopg2
# RUN pip3 install beautifulsoup4
# RUN pip3 install requests
CMD ["python","./web_crawler.py"]