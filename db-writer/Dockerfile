FROM python:3.11

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./main.py /code/main.py

ADD ./start.sh /code/start.sh

ENV PYTHONUNBUFFERED=1

RUN ["chmod", "+x", "/code/start.sh"]

ENTRYPOINT ["./start.sh"]
