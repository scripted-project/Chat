FROM python:3.8-slim-buster

WORKDIR /chat-site

COPY . .
RUN pip3 install -r static/requirements.txt

CMD [ "python3", "main.py"]