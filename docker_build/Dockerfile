FROM python:3
ADD html_scraper.py /
ADD http_data.conf /
ADD out /out
RUN pip3 install requests
RUN pip3 install pandas
RUN pip3 install configparser

RUN pip3 install lxml
CMD ["python3", "html_scraper.py"]
