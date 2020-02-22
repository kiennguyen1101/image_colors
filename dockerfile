FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7 as intermediate
RUN apt-get update && apt-get install -yqq python-dev
WORKDIR /app
COPY ./requirements.txt .
RUN pip install -r ./requirements.txt
COPY . .
