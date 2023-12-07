FROM python:3.8-slim-buster

WORKDIR /chat-site

COPY . .
RUN pip3 install flask flask-socketio gunicorn better_profanity schedule

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]