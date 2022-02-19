FROM python:2

WORKDIR /usr/src/app

RUN pip install beautifulsoup4
RUN pip install requests
RUN pip install selenium
RUN pip install webdriver-manager
RUN pip install flask-restful
RUN pip install flask_swagger_ui
RUN pip install flask-cors
RUN pip install python-dotenv

RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz
run tar -xvzf geckodriver*
RUN chmod +x geckodriver
RUN export PATH=$PATH:/path-to-extracted-file/.

COPY . .

EXPOSE 5000

CMD [ "python", "./server.py" ]
