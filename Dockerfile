FROM python:3.9

ENV DB_URL=

WORKDIR /

COPY ./requirements.txt /requirements.txt

RUN pip install --no-cache-dir --upgrade -r /requirements.txt

COPY ./src /megadados
COPY .env /

CMD ["python", "-m", "uvicorn", "megadados.main:app", "--host", "0.0.0.0", "--port", "8000"]


