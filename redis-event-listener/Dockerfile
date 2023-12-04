FROM python:3.11

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./main.py /code/main.py

ENV PYTHONUNBUFFERED=1

CMD ["python3", "/code/main.py"]
