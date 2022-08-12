FROM python:3.10-alpine

ADD requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

WORKDIR /app
RUN chown nobody:nogroup /app

COPY --chown=nobody:nogroup . ./
USER nobody

ENTRYPOINT python bot.py ${BOT_TOKEN}