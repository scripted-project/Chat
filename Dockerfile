FROM python:3.8-slim-buster

WORKDIR /chat-site

COPY . .
RUN pip3 install -r flask flask-socketio gunicorn bidict schedule better_profanity

CMD [ "python3", "main.py"]